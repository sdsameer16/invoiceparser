# Quick Command Reference

## Local Development

### Backend (Python/FastAPI)
```bash
# Install dependencies (first time)
pip install -r requirements.txt

# Run development server (with auto-reload when you change code)
uvicorn backend.app:app --reload

# Runs at: http://localhost:8000
# API docs available at: http://localhost:8000/docs
```

### Frontend (Static HTML/JS)
```bash
# Simply open in browser
# Option 1: Open directly
start frontend/index.html

# Option 2: Use Python's built-in server
python -m http.server 3000 --directory frontend

# Runs at: http://localhost:3000
```

---

## Production Deployment

### Backend on Render (Python)
**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

**What this means:**
- `uvicorn` = Server that runs your FastAPI application
- `--host 0.0.0.0` = Listen on all network interfaces
- `--port $PORT` = Use the port Render assigns

**Environment variables needed:**
- `GEMINI_API_KEY` = Your Google Gemini API key (required for AI)

---

### Frontend on Vercel (Static Files)
**Build Command:**
```bash
echo 'Frontend only - static files'
```

**Output Directory:**
```
frontend/
```

**No environment variables needed** (but update backend URL in script.js)

---

## Why These Commands?

**Python Requirements:**
- Your project uses Python with FastAPI framework
- All dependencies are listed in `requirements.txt`
- `pip install` is Python's package manager

**Uvicorn Server:**
- FastAPI apps need an ASGI server (like uvicorn)
- `--reload` flag only works during development (restarts on file changes)
- Production uses fixed port `$PORT` provided by Render

**Frontend:**
- Pure HTML/CSS/JavaScript files
- No build process needed
- Vercel serves files directly from `frontend/` folder

---

## Testing Your Commands Locally

### 1. Test Backend
```bash
# In your project root:
pip install -r requirements.txt
uvicorn backend.app:app --reload

# In browser: http://localhost:8000/docs
# Try uploading a file at the /upload endpoint
```

### 2. Test Frontend
```bash
# In new terminal (keep backend running):
python -m http.server 3000 --directory frontend

# In browser: http://localhost:3000
# Update the API URL in script.js to http://localhost:8000
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing packages | Run `pip install -r requirements.txt` |
| `Port already in use` | Another process using port | Kill the process or use different port |
| `API key not found` | GEMINI_API_KEY not set | Set it in Render environment variables |
| `Frontend can't reach backend` | Wrong URL in script.js | Update to your Render backend URL |
| `Permission denied` on .sh file | Shell script not executable | Run `chmod +x start_backend_prod.sh` |

---

## File Structure for Deployment

```
invoiceParser/
├── backend/              ← Python FastAPI app
│   ├── app.py           ← Main application (Render runs this)
│   ├── config.py        ← Configuration
│   └── extractor.py     ← Core logic
│
├── frontend/            ← Static HTML/JS (Vercel serves this)
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── requirements.txt     ← Python dependencies (for Render)
├── render.yaml          ← Render deployment config
├── vercel.json          ← Vercel deployment config
└── .env.example         ← Template for environment variables
```

---

## Summary

**You need to know:**
- **Backend**: Python project → uses `pip install` for dependencies → runs with `uvicorn` command
- **Frontend**: Plain HTML/JS → no build needed → just served as static files
- **Render**: Runs Python backend with the commands in `render.yaml`
- **Vercel**: Serves HTML frontend from the `frontend/` folder
