"""
Streamlit frontend for the Instagram Feed Clone.

Run with:
streamlit run frontend/app.py
"""

import base64

import streamlit as st

from api_client import create_post, get_posts, login, signup

st.set_page_config(page_title="Instagram Feed Clone", page_icon="📸", layout="centered")


# --------------------------
# Session state setup
# --------------------------
if "user" not in st.session_state:
    st.session_state.user = None


# --------------------------
# Helper functions
# --------------------------
def file_to_base64(uploaded_file):
    """
    Convert uploaded file bytes to base64 string.
    Returns None if no file uploaded.
    """
    if not uploaded_file:
        return None
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


def show_auth_page():
    """Show login/signup UI when user is not logged in."""
    st.title("📸 Instagram Feed Clone")
    st.subheader("Login or Signup")

    auth_mode = st.radio("Choose action", ["Login", "Signup"], horizontal=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(auth_mode):
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        with st.spinner(f"{auth_mode} in progress..."):
            try:
                if auth_mode == "Signup":
                    response = signup(email, password)
                else:
                    response = login(email, password)

                data = response.json()

                if response.status_code == 200:
                    st.success(data.get("message", "Success"))

                    # On login, save user in session for persistence.
                    if auth_mode == "Login":
                        st.session_state.user = data["user"]
                        st.rerun()
                else:
                    st.error(data.get("detail", "Something went wrong."))
            except Exception as e:
                st.error(f"Cannot connect to backend: {str(e)}")


def show_feed_page():
    """Show create-post area + feed when user is logged in."""
    user = st.session_state.user

    st.title("🏠 Your Feed")
    st.caption(f"Logged in as: {user['email']}")

    # Optional, simple profile section.
    with st.expander("👤 Profile"):
        st.write(f"Email: {user['email']}")
        st.write(f"User ID: {user['uid']}")
        st.info("Basic profile view only for this beginner project.")

    if st.button("Logout"):
        st.session_state.user = None
        st.success("Logged out successfully.")
        st.rerun()

    st.divider()
    st.subheader("Create a Post")

    caption = st.text_area("Caption", placeholder="Write something...")
    uploaded_file = st.file_uploader("Optional image", type=["png", "jpg", "jpeg"])

    if st.button("Post"):
        if not caption.strip():
            st.error("Caption cannot be empty.")
        else:
            image_base64 = file_to_base64(uploaded_file)
            with st.spinner("Creating post..."):
                try:
                    response = create_post(
                        uid=user["uid"],
                        email=user["email"],
                        caption=caption,
                        image_base64=image_base64,
                    )
                    data = response.json()

                    if response.status_code == 200:
                        st.success("Post created successfully!")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Failed to create post."))
                except Exception as e:
                    st.error(f"Cannot connect to backend: {str(e)}")

    st.divider()
    st.subheader("Latest Posts")

    with st.spinner("Loading feed..."):
        try:
            response = get_posts()
            data = response.json()

            if response.status_code != 200:
                st.error(data.get("detail", "Failed to load posts."))
                return

            posts = data.get("posts", [])
            if not posts:
                st.info("No posts yet. Create your first post!")
                return

            for post in posts:
                st.markdown("---")
                st.text(f"👤 {post.get('email', 'Unknown user')}")
                st.text(post.get("caption", ""))

                # If we have base64 image, display with data URL.
                image_base64 = post.get("image_base64")
                if image_base64:
                    st.image(f"data:image/png;base64,{image_base64}", use_container_width=True)

                st.caption(f"🕒 {post.get('created_at', '')}")

        except Exception as e:
            st.error(f"Cannot connect to backend: {str(e)}")


# --------------------------
# Main app flow
# --------------------------
if st.session_state.user is None:
    show_auth_page()
else:
    show_feed_page()
