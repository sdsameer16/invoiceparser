# 🚀 Quick Usage Guide

## Step 1: Start the System

### Option A: Windows
1. Double-click `start_backend.bat`
2. Wait for "Application startup complete" message
3. Open `frontend/index.html` in your web browser

### Option B: Manual Start
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Start backend
cd backend
uvicorn app:app --reload

# Open frontend/index.html in browser
```

## Step 2: Test with Sample Files

1. Use files from `sample_files/` folder:
   - `sample_invoices.txt` - Text format with multiple invoices
   - `sample_invoices.csv` - Excel/CSV format

2. Upload files using the web interface
3. Click "Extract Data" 
4. Review results in the table

## Step 3: Process Your Own Files

### Supported Formats:
- **PDF**: `.pdf` files with text content
- **Excel**: `.xlsx`, `.xls` files with structured data  
- **Word**: `.docx` files with invoice text

### Expected Data Format:
For best results, ensure your files contain:
```
Customer: [Company Name]
Date: [Invoice Date]  
Item: [Product/Service Description]
Total: [Amount] or Amount: [Value]
```

## Step 4: Export Results

1. After processing, click "📥 Export CSV" 
2. Save the consolidated data file
3. Use "🗑️ Clear" to reset for new batch

## 🔧 Troubleshooting

### Backend Won't Start:
- Check if Python is installed: `python --version`
- Install missing packages: `pip install -r requirements.txt`
- Try a different port: `uvicorn app:app --port 8001`

### Frontend Can't Connect:
- Ensure backend is running at http://127.0.0.1:8000
- Check browser console for CORS errors
- Try using `python -m http.server` in frontend folder

### No Data Extracted:
- Verify file contains readable text (not scanned images)
- Check if keywords match: "customer", "date", "item", "total"
- Try different file formats

## 🎯 Next Steps

Once basic system works, consider:

1. **AI Enhancement**: Integrate Gemini API for better accuracy
2. **OCR Support**: Add image/scanned document processing  
3. **Custom Templates**: Create extraction patterns for specific formats
4. **Database Storage**: Persist extracted data
5. **Advanced UI**: Add filtering, sorting, batch operations

---

**Need Help?** Check the full README.md for detailed documentation.