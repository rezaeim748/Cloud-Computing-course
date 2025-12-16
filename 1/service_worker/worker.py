from message_queue import consume
from db import update_ad_status, get_ad
from storage import get_image_bytes
from image_tagging import tag_image_bytes, decide
from emailer import send_email

from io import BytesIO
from PIL import Image
import io
import json


def handle_message(msg):
    # --- Parse message safely ---
    print(f"[Worker] Raw message received: {msg}")
    if isinstance(msg, bytes):
        msg = msg.decode("utf-8")
    if isinstance(msg, str):
        try:
            msg = json.loads(msg)
        except json.JSONDecodeError:
            print("[WARN] Could not decode message as JSON, skipping.")
            return

    # Extract ad_id safely (supports 'id' or 'ad_id')
    ad_id = msg.get("id") or msg.get("ad_id")
    if not ad_id:
        print(f"[WARN] No 'id' or 'ad_id' in message: {msg}")
        return

    print(f"[Worker] Processing ad {ad_id}")
    ad = get_ad(ad_id)
    if not ad:
        print(f"[WARN] No ad found with id {ad_id}")
        return

    # --- Fetch image ---
    image_key = ad["image_key"]
    print(f"[DEBUG] Fetching S3 key: {image_key}")
    img = get_image_bytes(image_key)
    print(f"[DEBUG] Image size: {len(img)} bytes")

    # --- Convert unsupported formats (.webp) to JPEG ---
    try:
        image = Image.open(io.BytesIO(img)).convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        img = buffer.getvalue()
        print(f"[DEBUG] Converted image to JPEG ({len(img)} bytes)")
    except Exception as e:
        print(f"[WARN] Could not convert image: {e}")

    # --- Tag image via Imagga with graceful fallback ---
    try:
        tags = tag_image_bytes(img)
    except RuntimeError as e:
        print(e)
        tags = [{"tag": "unknown", "confidence": 0}]

    # --- Decide approval ---
    result = decide(tags)
    print(f"[Worker] Decision for ad {ad_id}: {result}")

    # --- Update DB ---
    update_ad_status(ad_id, result["approved"], result["category"])

    # --- Send email notification ---
    try:
        send_email(
            ad["email"],
            result["approved"],
            ad["description"]
        )
        print("[Worker] Email sent successfully")
    except Exception as e:
        print("[WARN] Email sending skipped:", e)



if __name__ == "__main__":
    print("[Worker] Waiting for messages...")
    consume(handle_message)
