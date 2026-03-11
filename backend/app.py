from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_invoice
import shutil
import os
import asyncio
from typing import List
from config import config

app = FastAPI(
    title="Invoice Data Extractor API",
    description="AI-powered invoice extraction using Gemini 2.5 API",
    version="2.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.csv', '.txt',  # Documents
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'  # Images
}

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    """
    Upload and process multiple invoice files using AI-enhanced extraction.
    Supports: PDF, Word (.docx), Excel (.xlsx/.xls), Images (PNG, JPG, etc.)
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    results = []
    processing_stats = {
        "total_files": len(files),
        "successful": 0,
        "failed": 0,
        "ai_processed": 0,
        "traditional_processed": 0
    }

    for file in files:
        file_result = {
            "filename": file.filename,
            "status": "processing",
            "data": None,
            "error": None
        }
        
        try:
            # Validate file type
            if not is_supported_file(file.filename):
                file_result["status"] = "error"
                file_result["error"] = f"Unsupported file type: {file.filename}"
                results.append(file_result)
                processing_stats["failed"] += 1
                continue
            
            # Save uploaded file temporarily
            temp_path = f"temp/{file.filename}"
            
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract data using AI-enhanced extractor
            extracted_data = await extract_invoice(temp_path)
            
            if extracted_data:
                # Handle both single and multiple results
                if isinstance(extracted_data, list):
                    # Multiple invoices found
                    for data in extracted_data:
                        result_entry = file_result.copy()
                        result_entry["data"] = data
                        result_entry["status"] = "success"
                        results.append(result_entry)
                        processing_stats["successful"] += 1
                else:
                    # Single invoice
                    file_result["data"] = extracted_data
                    file_result["status"] = "success"
                    results.append(file_result)
                    processing_stats["successful"] += 1
                
                # Track AI vs traditional processing
                if isinstance(extracted_data, list):
                    # Handle list of results
                    for data in extracted_data:
                        if data.get("confidence") in ["High", "Medium"]:
                            processing_stats["ai_processed"] += 1
                        else:
                            processing_stats["traditional_processed"] += 1
                else:
                    # Handle single result
                    if extracted_data.get("confidence") in ["High", "Medium"]:
                        processing_stats["ai_processed"] += 1
                    else:
                        processing_stats["traditional_processed"] += 1
            else:
                file_result["status"] = "error"
                file_result["error"] = "No data could be extracted"
                results.append(file_result)
                processing_stats["failed"] += 1
        
        except Exception as e:
            file_result["status"] = "error"
            file_result["error"] = str(e)
            results.append(file_result)
            processing_stats["failed"] += 1
            print(f"Error processing {file.filename}: {e}")
        
        finally:
            # Clean up temporary file
            temp_path = f"temp/{file.filename}"
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass  # Continue if file cleanup fails

    return {
        "data": [r["data"] for r in results if r["data"]],
        "results": results,
        "stats": processing_stats,
        "gemini_status": "available" if config.is_available() else "not_configured"
    }

def is_supported_file(filename: str) -> bool:
    """Check if file extension is supported"""
    if not filename:
        return False
    
    file_ext = os.path.splitext(filename.lower())[1]
    return file_ext in SUPPORTED_EXTENSIONS

@app.get("/")
async def root():
    """
    API health check and configuration status
    """
    return {
        "message": "Invoice Parser API v2.0 is running",
        "features": {
            "ai_parsing": config.is_available(),
            "supported_formats": list(SUPPORTED_EXTENSIONS),
            "model": config.model_name if config.is_available() else "N/A"
        },
        "status": "healthy"
    }

@app.get("/config")
async def get_config():
    """
    Get current configuration status
    """
    return {
        "gemini_configured": config.is_available(),
        "model": config.model_name if config.is_available() else None,
        "fallback_enabled": config.fallback_to_traditional,
        "supported_formats": list(SUPPORTED_EXTENSIONS)
    }

@app.post("/test-gemini")
async def test_gemini():
    """
    Test Gemini API connection
    """
    if not config.is_available():
        raise HTTPException(status_code=503, detail="Gemini API not configured")
    
    try:
        # Simple test prompt
        response = config.model.generate_content("Test: Extract from this text: Customer: Test Company, Amount: 1000")
        return {
            "status": "success",
            "model": config.model_name,
            "response_preview": response.text[:200] + "..." if len(response.text) > 200 else response.text
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Gemini API error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Invoice Parser API v2.0 with Gemini AI...")
    print(f"🤖 Gemini Status: {'✅ Available' if config.is_available() else '⚠️  Not Configured'}")
    print(f"📁 Supported Formats: {', '.join(SUPPORTED_EXTENSIONS)}")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)