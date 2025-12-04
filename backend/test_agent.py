"""
Quick test script to verify the agent works.
Run this before the workshop to ensure everything is set up correctly.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    try:
        import langchain
        print("✅ langchain")
    except ImportError:
        print("❌ langchain - run: pip install langchain")
        return False
    
    try:
        import langgraph
        print("✅ langgraph")
    except ImportError:
        print("❌ langgraph - run: pip install langgraph")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain-google-genai")
    except ImportError:
        print("❌ langchain-google-genai - run: pip install langchain-google-genai")
        return False
    
    try:
        import chromadb
        print("✅ chromadb")
    except ImportError:
        print("❌ chromadb - run: pip install chromadb")
        return False
    
    return True


def test_api_key():
    """Test that Gemini API key is set"""
    print("\nTesting API key...")
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("   Create a .env file with: GEMINI_API_KEY=your_key_here")
        return False
    
    if not api_key.startswith("AIza"):
        print("⚠️  API key doesn't start with 'AIza' - might be invalid")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    return True


def test_llm():
    """Test that Gemini LLM works"""
    print("\nTesting Gemini LLM...")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.schema import HumanMessage
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        response = llm.invoke([HumanMessage(content="Say 'Hello Workshop!'")])
        print(f"✅ LLM response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False


def test_tools():
    """Test that tools work"""
    print("\nTesting tools...")
    try:
        from tools import calculate_auto_premium
        
        result = calculate_auto_premium.invoke({
            "age": 28,
            "vehicle_year": 2020,
            "years_licensed": 10,
            "accidents": 0,
            "violations": 0
        })
        
        print(f"✅ Tool result: ${result['monthly_premium']}/month")
        return True
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        return False


def test_rag():
    """Test that RAG system works"""
    print("\nTesting RAG system...")
    try:
        from rag_system import search_knowledge
        
        results = search_knowledge("What is collision coverage?", k=1)
        if results:
            print(f"✅ RAG search returned {len(results)} results")
            print(f"   Sample: {results[0].page_content[:100]}...")
            return True
        else:
            print("⚠️  RAG search returned no results")
            return False
    except Exception as e:
        print(f"❌ RAG test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Testing Workshop Setup")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("API Key", test_api_key),
        ("Gemini LLM", test_llm),
        ("Tools", test_tools),
        ("RAG System", test_rag)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results[name] = False
    
    print("\n" + "="*60)
    print("📊 Test Results")
    print("="*60)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Ready for workshop!")
    else:
        print("\n⚠️  Some tests failed. Fix issues before workshop.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
