"""
Test using Google's native SDK instead of LangChain
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:20]}...")

try:
    import google.generativeai as genai
    
    print("\n✅ Google GenAI imported")
    
    # Configure with API key
    genai.configure(api_key=api_key)
    
    print("✅ API configured")
    
    # List available models
    print("\n📋 Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
    # Test with gemini-pro
    print("\n🧪 Testing with gemini-pro...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello' in one word")
    
    print(f"✅ Response: {response.text}")
    print("\n🎉 API key is working with native SDK!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
