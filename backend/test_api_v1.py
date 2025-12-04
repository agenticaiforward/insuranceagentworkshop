"""
Test with explicit API version configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:20]}...")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
    
    print("\n✅ Imports successful")
    
    # Try with explicit client_options
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0.7,
        client_options={"api_endpoint": "generativelanguage.googleapis.com"}
    )
    
    print("✅ LLM initialized")
    
    # Test simple message
    print("\n🧪 Testing Gemini API...")
    response = llm.invoke([HumanMessage(content="Say 'Hello' in one word")])
    
    print(f"✅ Response received: {response.content}")
    print("\n🎉 API key is working!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
