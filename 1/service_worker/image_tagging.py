import os
import requests

# Load API keys and confidence threshold
IMAGGA_API_KEY = os.getenv("IMAGGA_API_KEY")
IMAGGA_API_SECRET = os.getenv("IMAGGA_API_SECRET")
IMAGGA_MIN_CONF = float(os.getenv("IMAGGA_MIN_CONFIDENCE", "50"))


def tag_image_bytes(image_bytes: bytes):
    """Send an image to Imagga for tagging and return a list of tags with confidence."""

    if not IMAGGA_API_KEY or not IMAGGA_API_SECRET:
        raise RuntimeError("[Imagga] Missing IMAGGA_API_KEY or IMAGGA_API_SECRET in environment variables.")

    if not image_bytes:
        raise ValueError("[Imagga] Empty image payload. Check storage/get_image_bytes and S3 object key.")

    print(f"[DEBUG] Imagga upload size: {len(image_bytes)} bytes")

    url = "https://api.imagga.com/v2/tags"
    files = {"image": ("upload.jpg", image_bytes, "application/octet-stream")}

    try:
        resp = requests.post(
            url,
            auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET),
            files=files,
            timeout=30,
        )
    except requests.RequestException as e:
        raise RuntimeError(f"[Imagga] Network error: {e!r}")

    if resp.status_code >= 400:
        raise RuntimeError(f"[Imagga] {resp.status_code} response: {resp.text}")

    data = resp.json()
    tags = data.get("result", {}).get("tags", [])
    out = []
    for t in tags:
        tagname = (t.get("tag") or {}).get("en") or ""
        conf = float(t.get("confidence") or 0)
        out.append({"tag": tagname.lower(), "confidence": conf})
    return out


def decide(tags):
    """Decide approval based on detected tags and confidence."""
    vehicle_words = {"vehicle", "car", "automobile", "motorcycle", "motorbike", "bike"}
    has_vehicle = any(
        (t["tag"] in vehicle_words) and (t["confidence"] >= IMAGGA_MIN_CONF)
        for t in tags
    )
    if not has_vehicle:
        return {"approved": False, "category": None}

    top = max(tags, key=lambda x: x["confidence"]) if tags else {"tag": None}
    return {"approved": True, "category": top["tag"]}
