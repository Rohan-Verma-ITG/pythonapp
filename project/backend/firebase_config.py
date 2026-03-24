"""
Firebase configuration helper.

This file creates and returns shared Firebase clients:
- Firestore (database)
- Firebase Auth (for creating/verifying users)
- Firebase Storage bucket (for optional image upload)

Beginner note:
You must set the environment variable GOOGLE_APPLICATION_CREDENTIALS
with the path to your Firebase service account JSON file.
"""

import os
from functools import lru_cache

import firebase_admin
from firebase_admin import auth, credentials, firestore, storage


@lru_cache(maxsize=1)
def get_firebase_clients():
    """
    Initialize Firebase Admin SDK once and reuse the clients.

    Why lru_cache?
    - FastAPI can import this file multiple times.
    - We only want one Firebase app instance.
    """
    # Optional: set your bucket in environment variable for easier config.
    # Example: export FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"
    bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")

    # If no Firebase app exists yet, create one.
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        if bucket_name:
            firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})
        else:
            firebase_admin.initialize_app(cred)

    db = firestore.client()

    # storage.bucket() works only if a bucket is configured.
    # If not, we keep it as None and image upload can be skipped.
    bucket = None
    try:
        bucket = storage.bucket()
    except Exception:
        bucket = None

    return {
        "db": db,
        "auth": auth,
        "bucket": bucket,
    }
