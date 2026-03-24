"""
Post routes.

This module provides:
- POST /posts (create a post)
- GET /posts (list all posts, latest first)
"""

from datetime import datetime, timezone
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.firebase_config import get_firebase_clients

router = APIRouter(tags=["posts"])


class CreatePostRequest(BaseModel):
    """Request body for creating a post."""

    uid: str
    email: str
    caption: str
    image_base64: str | None = None


@router.post("/posts")
def create_post(payload: CreatePostRequest):
    """
    Create a post in Firestore.

    If image_base64 is provided and Firebase Storage is configured,
    upload image to Storage and save the public URL.
    """
    clients = get_firebase_clients()
    db = clients["db"]
    bucket = clients["bucket"]

    if not payload.caption.strip():
        raise HTTPException(status_code=400, detail="Caption cannot be empty.")

    image_url = None

    # Upload optional image if sent.
    if payload.image_base64 and bucket:
        try:
            image_name = f"posts/{payload.uid}/{uuid.uuid4().hex}.txt"
            blob = bucket.blob(image_name)

            # To keep the app beginner-friendly, we store base64 text as a file.
            # Streamlit can still display data URLs from base64 directly.
            blob.upload_from_string(payload.image_base64, content_type="text/plain")
            blob.make_public()
            image_url = blob.public_url
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image upload failed: {str(e)}")

    post_data = {
        "uid": payload.uid,
        "email": payload.email,
        "caption": payload.caption.strip(),
        "image_base64": payload.image_base64,
        "image_url": image_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        doc_ref = db.collection("posts").document()
        doc_ref.set(post_data)
        return {"message": "Post created", "post_id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create post: {str(e)}")


@router.get("/posts")
def get_posts():
    """
    Fetch all posts from Firestore and return newest first.
    """
    clients = get_firebase_clients()
    db = clients["db"]

    try:
        docs = db.collection("posts").stream()
        posts = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            posts.append(data)

        # Sort in descending order by created_at (latest first).
        posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch posts: {str(e)}")
