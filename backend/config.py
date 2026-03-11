import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

class GeminiConfig:
    """Configuration class for Gemini API settings"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.temperature = float(os.getenv('GEMINI_TEMPERATURE', '0.1'))
        self.max_tokens = int(os.getenv('GEMINI_MAX_TOKENS', '8192'))
        self.enable_ai_parsing = os.getenv('ENABLE_AI_PARSING', 'true').lower() == 'true'
        self.fallback_to_traditional = os.getenv('FALLBACK_TO_TRADITIONAL', 'true').lower() == 'true'
        
        # Initialize Gemini if API key is available
        if self.api_key and self.api_key != 'your_gemini_api_key_here':
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
        else:
            self.model = None
            print("⚠️  Gemini API key not configured. Using traditional parsing only.")
            print("   Set GEMINI_API_KEY in .env file to enable AI parsing.")
    
    def is_available(self) -> bool:
        """Check if Gemini API is properly configured"""
        return self.model is not None

# Global configuration instance
config = GeminiConfig()

# Invoice extraction prompt template
INVOICE_EXTRACTION_PROMPT = """
You are an expert invoice data extraction system. Analyze the provided document and extract the following information in JSON format:

{
  "customer": "Customer/Company name",
  "date": "Invoice date (YYYY-MM-DD format if possible)",
  "item": "Product/Service description", 
  "amount": "Total amount (numbers only, no currency symbols)",
  "currency": "Currency symbol or code if visible",
  "invoice_number": "Invoice/Reference number if available",
  "confidence": "High/Medium/Low based on data clarity"
}

Important guidelines:
1. Extract ONLY information that is clearly visible in the document
2. Use "N/A" for fields that are not found or unclear
3. For amount, extract only numbers (e.g., "50000" not "₹50,000")
4. Be precise and don't make assumptions
5. If multiple items exist, focus on the main/total amount
6. Ensure JSON format is valid

Document to analyze:
"""

BATCH_EXTRACTION_PROMPT = """
You are processing multiple invoices or a document with multiple invoice entries. Extract data for each separate invoice found and return as a JSON array:

[
  {
    "customer": "Customer 1",
    "date": "Date 1", 
    "item": "Item 1",
    "amount": "Amount 1",
    "currency": "Currency 1",
    "invoice_number": "Invoice 1",
    "confidence": "High/Medium/Low"
  },
  {
    "customer": "Customer 2", 
    "date": "Date 2",
    "item": "Item 2", 
    "amount": "Amount 2",
    "currency": "Currency 2",
    "invoice_number": "Invoice 2",
    "confidence": "High/Medium/Low"
  }
]

Guidelines:
- Extract each separate invoice as a distinct entry
- Use "N/A" for missing information
- Ensure valid JSON array format
- For amounts, use numbers only (no currency symbols)
- Focus on clear, visible data only

Document to analyze:
"""