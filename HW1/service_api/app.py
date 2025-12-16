import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import init_db, SessionLocal, Ad
from storage import put_image, presign_get
from message_queue import publish_ad
import uuid
from fastapi import BackgroundTasks
from fastapi.concurrency import run_in_threadpool


app = FastAPI(title="Cloud Ads API")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/ads")
async def create_ad(
    description: str = Form(...),
    email: str = Form(...),
    image: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    # Persist record
    db: Session = SessionLocal()
    ad = Ad(description=description, email=email, state="pending")
    db.add(ad)
    db.commit()
    db.refresh(ad)

    # Store image
    ext = (image.filename or "img").split(".")[-1]
    key = f"ads/{ad.id}/{uuid.uuid4()}.{ext}"
    content = await image.read()
    await run_in_threadpool(
        put_image,
        key,
        content,
        image.content_type or "application/octet-stream"
    )

    # Save key, enqueue
    ad.image_key = key
    db.add(ad)
    db.commit()

    background_tasks.add_task(publish_ad, ad.id)
    return JSONResponse({"message": f"Ad registered", "id": ad.id})

@app.get("/ads/{ad_id}")
def get_ad(ad_id: int):
    db: Session = SessionLocal()
    ad = db.get(Ad, ad_id)
    if not ad:
        raise HTTPException(404, "Ad not found")
    if ad.state == "pending":
        return {"status": "pending", "message": "Your ad is under review."}
    if ad.state == "rejected":
        return {"status": "rejected", "message": "Your ad was not approved."}
    # approved
    presigned = presign_get(ad.image_key) if ad.image_key else None
    return {
        "status": "approved",
        "id": ad.id,
        "description": ad.description,
        "email": ad.email,
        "category": ad.category,
        "image_url": presigned
    }
