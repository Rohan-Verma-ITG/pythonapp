"""
Authentication routes.

This module provides:
- POST /signup
- POST /login

Important beginner note:
Firebase Admin SDK can create users, but it does not directly support
email+password sign-in like a client SDK.

To keep this project simple and fully server-driven, login checks if a user
with the given email exists. In a production app, you should verify passwords
using Firebase Auth REST API or Firebase client SDK tokens.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from backend.firebase_config import get_firebase_clients

router = APIRouter(tags=["auth"])


class AuthRequest(BaseModel):
    """Request body for signup/login."""

    email: EmailStr
    password: str


@router.post("/signup")
def signup(payload: AuthRequest):
    """
    Create a new Firebase Auth user with email + password.
    """
    clients = get_firebase_clients()
    firebase_auth = clients["auth"]

    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    try:
        user = firebase_auth.create_user(email=payload.email, password=payload.password)
        return {
            "message": "Signup successful",
            "user": {
                "uid": user.uid,
                "email": user.email,
            },
        }
    except Exception as e:
        # Keep error clear for beginners.
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")


@router.post("/login")
def login(payload: AuthRequest):
    """
    Simple login endpoint.

    For beginner simplicity, we verify that the user exists by email.
    In production, replace this with proper password verification.
    """
    clients = get_firebase_clients()
    firebase_auth = clients["auth"]

    if not payload.password:
        raise HTTPException(status_code=400, detail="Password is required.")

    try:
        user = firebase_auth.get_user_by_email(payload.email)
        return {
            "message": "Login successful",
            "user": {
                "uid": user.uid,
                "email": user.email,
            },
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
