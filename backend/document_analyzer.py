"""
Document Analysis System
Uses Gemini's multimodal capabilities to analyze uploaded insurance documents
"""

import os
import base64
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini Pro Vision for document analysis
vision_model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_insurance_document(file_content: bytes, mime_type: str) -> Dict[str, Any]:
    """
    Analyze an uploaded insurance document using Gemini's vision capabilities
    
    Args:
        file_content: Raw file bytes
        mime_type: MIME type (e.g., 'application/pdf', 'image/png')
    
    Returns:
        Extracted insurance information
    """
    
    # Prepare the prompt for extraction
    extraction_prompt = """Analyze this insurance document and extract the following information:

1. **Insurance Provider**: Company name
2. **Policy Type**: Auto, Home, or Other
3. **Policy Number**: If visible
4. **Current Premium**: Monthly or annual amount
5. **Coverage Details**:
   - For Auto: Liability limits, collision, comprehensive, deductible
   - For Home: Dwelling coverage, personal property, liability, deductible
6. **Policyholder Information**: Name, address if visible
7. **Policy Period**: Start and end dates if visible
8. **Additional Coverage**: Any extra coverages or riders

Please format the response as a structured summary. If any information is not visible or unclear, indicate "Not found" for that field.

Be specific about dollar amounts and coverage limits."""

    try:
        # For inline data (simpler and more reliable)
        if mime_type.startswith('image/'):
            # For images, use PIL
            try:
                import PIL.Image
                import io
                image = PIL.Image.open(io.BytesIO(file_content))
                
                response = vision_model.generate_content([
                    extraction_prompt,
                    image
                ])
            except Exception as img_error:
                print(f"❌ Image processing error: {img_error}")
                return {
                    "success": False,
                    "error": str(img_error),
                    "message": "Could not process image. Please ensure it's a valid image file."
                }
        elif mime_type == 'application/pdf':
            # For PDFs, use base64 inline
            try:
                # Ensure we have valid base64
                base64_data = base64.b64encode(file_content).decode('utf-8')
                
                # Create the content part for PDF
                pdf_part = {
                    "mime_type": "application/pdf",
                    "data": base64_data
                }
                
                response = vision_model.generate_content([
                    extraction_prompt,
                    pdf_part
                ])
            except Exception as pdf_error:
                print(f"❌ PDF processing error: {pdf_error}")
                return {
                    "success": False,
                    "error": str(pdf_error),
                    "message": "Could not process PDF. Please try uploading an image (PNG/JPG) of your policy instead."
                }
        else:
            return {
                "success": False,
                "error": "Unsupported file type",
                "message": f"Unsupported file type: {mime_type}. Please upload a PDF, PNG, or JPG."
            }
        
        extracted_text = response.text
        
        # Parse the response to structure it
        structured_data = parse_extraction_response(extracted_text)
        
        return {
            "success": True,
            "extracted_data": structured_data,
            "raw_analysis": extracted_text
        }
        
    except Exception as e:
        print(f"❌ General analysis error: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Could not analyze document: {str(e)}. Please ensure it's a valid insurance document."
        }

def parse_extraction_response(text: str) -> Dict[str, Any]:
    """Parse Gemini's response into structured data"""
    
    # Simple parsing - in production you'd use more robust extraction
    data = {
        "provider": extract_field(text, ["provider", "company", "insurer"]),
        "policy_type": extract_field(text, ["policy type", "insurance type"]),
        "policy_number": extract_field(text, ["policy number", "policy #"]),
        "current_premium": extract_field(text, ["premium", "monthly payment", "annual premium"]),
        "coverage_details": extract_coverage(text),
        "policyholder": extract_field(text, ["policyholder", "insured", "name"]),
        "policy_period": extract_field(text, ["policy period", "effective dates", "coverage period"])
    }
    
    return data

def extract_field(text: str, keywords: list) -> str:
    """Extract a specific field from text"""
    text_lower = text.lower()
    
    for keyword in keywords:
        # Find the keyword and extract the value after it
        if keyword in text_lower:
            # Simple extraction - get the line containing the keyword
            lines = text.split('\n')
            for line in lines:
                if keyword in line.lower():
                    # Extract value after colon or keyword
                    if ':' in line:
                        value = line.split(':', 1)[1].strip()
                        if value and value != "Not found":
                            return value
    
    return "Not found"

def extract_coverage(text: str) -> Dict[str, Any]:
    """Extract coverage details from text"""
    coverage = {}
    
    # Look for common coverage terms
    coverage_terms = {
        "liability": ["liability", "bodily injury", "property damage"],
        "collision": ["collision"],
        "comprehensive": ["comprehensive", "comp"],
        "deductible": ["deductible"],
        "dwelling": ["dwelling", "coverage a"],
        "personal_property": ["personal property", "contents", "coverage c"]
    }
    
    for coverage_type, keywords in coverage_terms.items():
        value = extract_field(text, keywords)
        if value != "Not found":
            coverage[coverage_type] = value
    
    return coverage

def generate_comparison_quote(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a comparison quote based on extracted data
    
    This simulates analyzing the current policy and offering a better rate
    """
    
    # Extract current premium
    current_premium_str = extracted_data.get("current_premium", "Not found")
    
    # Try to extract numeric value
    import re
    numbers = re.findall(r'\d+\.?\d*', current_premium_str)
    current_premium = float(numbers[0]) if numbers else 150.0
    
    # Determine if it's monthly or annual
    is_monthly = "month" in current_premium_str.lower()
    if not is_monthly and current_premium > 500:
        # Likely annual
        current_premium = current_premium / 12
    
    # Generate a competitive quote (10-20% lower)
    import random
    discount_percent = random.uniform(0.10, 0.20)
    our_premium = round(current_premium * (1 - discount_percent), 2)
    savings = round(current_premium - our_premium, 2)
    
    policy_type = extracted_data.get("policy_type", "Unknown")
    
    return {
        "current_provider": extracted_data.get("provider", "Current Provider"),
        "current_monthly_premium": round(current_premium, 2),
        "our_monthly_premium": our_premium,
        "monthly_savings": savings,
        "annual_savings": round(savings * 12, 2),
        "savings_percent": round(discount_percent * 100, 1),
        "policy_type": policy_type,
        "coverage_comparison": {
            "current": extracted_data.get("coverage_details", {}),
            "our_recommendation": "Similar or better coverage with additional benefits"
        },
        "recommendation": f"We can save you ${savings}/month (${round(savings * 12, 2)}/year) with comparable or better coverage!"
    }
