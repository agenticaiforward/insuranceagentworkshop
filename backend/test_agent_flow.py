from gemini_agent import chat_with_agent, reset_session
import time

def test_auto_insurance_flow():
    session_id = "test_user_123"
    reset_session(session_id)
    
    print("\n Testing Auto Insurance Flow...")
    
    # 1. Initial greeting
    msg = "Hi, I need car insurance"
    print(f"\nUser: {msg}")
    response = chat_with_agent(msg, session_id)
    print(f"Agent: {response}")
    
    # 2. Provide basic info
    msg = "I am 30 years old and I drive a 2022 Toyota Camry"
    print(f"\nUser: {msg}")
    response = chat_with_agent(msg, session_id)
    print(f"Agent: {response}")
    
    # 3. Provide history
    msg = "I've been driving for 12 years, no accidents or tickets"
    print(f"\nUser: {msg}")
    response = chat_with_agent(msg, session_id)
    print(f"Agent: {response}")
    
    if "$" in response:
        print("\n✅ Quote received!")
    else:
        print("\n⚠️ No quote yet, continuing...")
        
        # 4. Provide coverage details if asked
        msg = "I want 100/300 liability and yes to collision and comprehensive with $500 deductible"
        print(f"\nUser: {msg}")
        response = chat_with_agent(msg, session_id)
        print(f"Agent: {response}")

def test_home_insurance_flow():
    session_id = "test_user_456"
    reset_session(session_id)
    
    print("\n🏠 Testing Home Insurance Flow...")
    
    # 1. Initial greeting
    msg = "I need home insurance for my new house"
    print(f"\nUser: {msg}")
    response = chat_with_agent(msg, session_id)
    print(f"Agent: {response}")
    
    # 2. Provide property info
    msg = "It was built in 2015, 2500 sq ft, frame construction"
    print(f"\nUser: {msg}")
    response = chat_with_agent(msg, session_id)
    print(f"Agent: {response}")
    
    # 3. Provide coverage info
    msg = "I need $300,000 coverage. It has 2 stories, a security system, but no pool"
    print(f"\nUser: {msg}")
    response = chat_with_agent(msg, session_id)
    print(f"Agent: {response}")

if __name__ == "__main__":
    try:
        test_auto_insurance_flow()
        test_home_insurance_flow()
        print("\n✅ All flows completed successfully")
    except Exception as e:
        print(f"\n❌ Flow failed: {e}")
        import traceback
        traceback.print_exc()
