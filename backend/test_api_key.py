"""
Quick test to verify Gemini API key is working
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:20]}...")

# Try multiple models
models_to_try = [
    "gemini-1.5-pro",
    "gemini-1.5-flash-latest", 
    "gemini-pro",
    "gemini-2.0-flash-exp"
]

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
    
    print("\n✅ Imports successful")
    
    for model_name in models_to_try:
        print(f"\n🧪 Testing {model_name}...")
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.7,
                timeout=15,
                max_retries=1
            )
            
            response = llm.invoke([HumanMessage(content="Say 'Hello' in one word")])
            print(f"✅ {model_name} works! Response: {response.content}")
            print(f"\n🎉 Use this model: {model_name}")
            break
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"⚠️ {model_name}: Quota exceeded (but model is accessible)")
            elif "404" in error_msg:
                print(f"❌ {model_name}: Not found (404)")
            else:
                print(f"❌ {model_name}: {error_msg[:100]}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
