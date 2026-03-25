# Deployment Guide

## Backend Deployment (Render)

### Prerequisites
- Render.com account
- Your backend code on GitHub

### Environment Variables Required
- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `GEMINI_MODEL` - Model name (default: gemini-2.0-flash-exp)
- `GEMINI_TEMPERATURE` - Temperature for AI (default: 0.1)
- `GEMINI_MAX_TOKENS` - Max tokens (default: 8192)
- `ENABLE_AI_PARSING` - Enable AI parsing (default: true)
- `FALLBACK_TO_TRADITIONAL` - Fallback if AI fails (default: true)

### Steps to Deploy Backend on Render:

1. **Connect Repository**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - Name: `invoice-parser-backend`
   - Environment: `Python 3.11`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
   - Instance Type: Free or Starter (as needed)

3. **Add Environment Variables**
   - Go to Service Settings → Environment
   - Add all variables from `.env.example`
   - Especially: `GEMINI_API_KEY` (required for AI functionality)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment to complete
   - Note your backend URL (e.g., `https://invoice-parser-backend.onrender.com`)

### Backend Commands Reference:
```bash
# Local development
pip install -r requirements.txt
uvicorn backend.app:app --reload

# Production (as used by Render)
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

---

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account
- Frontend code on GitHub

### Steps to Deploy Frontend on Vercel:

1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository

2. **Configure Project**
   - Framework Preset: `Other` (static files)
   - Build Command: Leave as is (no build needed)
   - Output Directory: `frontend`
   - Environment Variables: None needed

3. **Update Backend URL**
   - In your frontend code ([script.js](frontend/script.js)), update the API URL:
     ```javascript
     const API_URL = 'https://invoice-parser-backend.onrender.com'; // Your Render backend URL
     ```

4. **Deploy**
   - Click "Deploy"
   - Your frontend will be live at a Vercel URL (e.g., `https://yourapp.vercel.app`)

### Frontend Deployment Options:
```
Option 1: Static hosting (recommended)
- No build step needed
- All files in `frontend/` folder served as-is

Option 2: Build process (if you add build tools later)
- Build Command: `npm run build` (if you add npm)
- Output Directory: `dist` or `build`
```

---

## Final Configuration Checklist

- [ ] Backend environment variables set in Render
- [ ] GEMINI_API_KEY configured (required)
- [ ] Frontend script.js points to correct backend URL
- [ ] CORS is configured in backend (currently allows all origins)
- [ ] Test upload file to verify both services work together

## Testing After Deployment

1. Visit your Vercel frontend URL
2. Upload an invoice file
3. Verify extraction works with backend on Render

## Troubleshooting

**Backend won't start**
- Check Python version is 3.11+
- Verify all requirements.txt packages install
- Check GEMINI_API_KEY is set

**Frontend can't reach backend**
- Verify backend URL in script.js is correct
- Check CORS settings in backend/app.py
- Test API directly: `curl https://your-backend-url/docs`

**AI extraction not working**
- Verify GEMINI_API_KEY is valid
- Check API key has Gemini API access enabled
- See backend logs in Render dashboard
