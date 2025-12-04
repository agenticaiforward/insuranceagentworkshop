import os
import sys
from unittest.mock import MagicMock

# Ensure backend is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# MOCK rag_system BEFORE importing langgraph_agent
# This avoids the "pydantic[dotenv]" error caused by langchain_google_genai/rag_system
sys.modules["rag_system"] = MagicMock()
sys.modules["rag_system"].get_relevant_context.return_value = "Mocked context for testing"

def test_langgraph_brain():
    """
    Test the LangGraph 'brain' directly.
    This demonstrates the state machine logic:
    Input -> Gather Info -> (Decision) -> Calculate Quote -> Explain Results
    """
    print("\n🧠 TESTING LANGGRAPH BRAIN")
    print("===========================")
    
    try:
        from langgraph_agent import agent_graph
        from langchain_core.messages import HumanMessage
        print("✅ Successfully imported agent_graph (with mocked rag_system)")
    except ImportError as e:
        print(f"❌ Failed to import agent_graph: {e}")
        return

    # Test Case: Auto Insurance Quote Flow
    print("\n🧪 Test Case: Auto Insurance Quote")
    print("   User Input: 'I am 30 years old, drive a 2020 Toyota Camry, have been licensed for 10 years'")
    
    initial_state = {
        "messages": [HumanMessage(content="I need auto insurance. I am 30 years old, drive a 2020 Toyota Camry, and have been licensed for 10 years.")],
        "user_info": {
            "age": 30,
            "vehicle_year": 2020,
            "vehicle_make": "Toyota",
            "vehicle_model": "Camry",
            "years_licensed": 10,
            "accidents": 0,
            "violations": 0
        },
        "insurance_type": "auto",
        "quote_result": None,
        "knowledge_context": "",
        "next_action": "gather_info"
    }
    
    print("\n🔄 Running Graph...")
    try:
        # Run the graph
        final_state = agent_graph.invoke(initial_state)
        
        print("\n✅ Graph Execution Complete!")
        print(f"   Final Node: {final_state.get('next_action')}")
        
        # Verify Quote Calculation
        quote = final_state.get("quote_result")
        if quote and "monthly_premium" in quote:
            print(f"   💰 Premium Calculated: ${quote['monthly_premium']}/month")
            print("   ✅ SUCCESS: Graph correctly transitioned to 'calculate_quote' and produced a result.")
        else:
            print("   ❌ FAILURE: Quote was not calculated.")
            print(f"   Final State Quote Result: {quote}")
            
    except Exception as e:
        print(f"   ❌ Graph Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_langgraph_brain()
