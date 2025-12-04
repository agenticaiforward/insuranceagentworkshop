try:
    import langchain_google_genai
    print("✅ langchain_google_genai found!")
    print(langchain_google_genai.__file__)
except ImportError as e:
    print(f"❌ ImportError: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
