# Beginner Instagram Feed Clone (FastAPI + Streamlit + Firebase)

This is a simple beginner-friendly project with:
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Auth + Database**: Firebase (Auth + Firestore)

---

## 1) Project Structure

```bash
project/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── firebase_config.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       └── posts.py
├── frontend/
│   ├── app.py
│   └── api_client.py
├── requirements.txt
└── README.md
```

---

## 2) Firebase Setup (Step by Step)

1. Create a Firebase project at <https://console.firebase.google.com/>.
2. In Firebase, enable **Authentication** and choose **Email/Password** provider.
3. In Firebase, create a **Firestore Database** (start in test mode for learning).
4. (Optional) Enable **Storage** if you want to save image text files in bucket.
5. Open **Project Settings** → **Service Accounts** → Generate a new private key.
6. Save this JSON key file on your computer.
7. Set environment variable:

### Linux/macOS
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/serviceAccountKey.json"
export FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"
```

### Windows (PowerShell)
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\full\path\to\serviceAccountKey.json"
$env:FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"
```

> `FIREBASE_STORAGE_BUCKET` is optional. If missing, post creation still works (without storage upload URL).

---

## 3) Install Dependencies

From inside the `project/` folder:

```bash
pip install -r requirements.txt
```

---

## 4) Run Backend (FastAPI)

From inside `project/`:

```bash
uvicorn backend.main:app --reload
```

Backend runs at: <http://127.0.0.1:8000>

---

## 5) Run Frontend (Streamlit)

Open a second terminal, go to `project/`, then run:

```bash
streamlit run frontend/app.py
```

Frontend usually runs at: <http://localhost:8501>

---

## 6) How the App Flow Works

1. User opens Streamlit app.
2. If not logged in → show Login/Signup screen.
3. After login → show feed + create post + logout button.
4. User creates post (caption + optional image).
5. Backend saves post in Firestore.
6. Feed shows all posts sorted with newest first.

---

## 7) Beginner Notes

- Login route is intentionally simple for learning.
- For real production auth, use Firebase client tokens or Firebase Auth REST sign-in endpoint.
- Code includes comments in each file for easy understanding.
