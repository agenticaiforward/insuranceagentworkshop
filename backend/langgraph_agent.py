"""
LangGraph Agent - Complete Agentic AI with Visual Orchestration
Demonstrates: Nodes, Edges, State Management, Tool Calling, RAG
"""

import os
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import tool
from dotenv import load_dotenv
import operator
from rag_system import get_relevant_context

load_dotenv()

# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """State that flows through the graph"""
    messages: Annotated[Sequence[HumanMessage | AIMessage], operator.add]
    user_info: dict
    insurance_type: str  # 'auto' or 'home'
    quote_result: dict
    knowledge_context: str
    next_action: str

# ============================================================================
# TOOLS (Functions the agent can call)
# ============================================================================

@tool
def calculate_auto_premium(
    age: int,
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    years_licensed: int,
    accidents: int,
    violations: int,
    liability_limit: str = "100000/300000",
    collision: bool = True,
    comprehensive: bool = True,
    deductible: int = 500
) -> dict:
    """Calculate auto insurance premium based on driver profile"""
    
    base_rate = 800
    
    # Age factor
    if age < 25:
        age_factor = 400
        age_explanation = "Young driver surcharge"
    elif age < 30:
        age_factor = 200
        age_explanation = "Moderate age adjustment"
    elif age > 65:
        age_factor = 150
        age_explanation = "Senior driver adjustment"
    else:
        age_factor = 0
        age_explanation = "Optimal age range"
    
    # Vehicle age
    vehicle_age = 2025 - vehicle_year
    if vehicle_age > 10:
        vehicle_factor = -100
        vehicle_explanation = "Older vehicle discount"
    elif vehicle_age < 3:
        vehicle_factor = 200
        vehicle_explanation = "New vehicle premium"
    else:
        vehicle_factor = 0
        vehicle_explanation = "Standard vehicle age"
    
    # Coverage
    liability_factors = {
        "50000/100000": 0,
        "100000/300000": 150,
        "250000/500000": 300,
        "500000/1000000": 500
    }
    liability_factor = liability_factors.get(liability_limit, 150)
    coverage_factor = (200 if collision else 0) + (150 if comprehensive else 0)
    deductible_factor = -50 if deductible >= 1000 else 0
    
    # Driver history
    experience_factor = -100 if years_licensed > 10 else 0
    accident_factor = accidents * 300
    violation_factor = violations * 200
    
    annual_premium = (base_rate + age_factor + vehicle_factor + liability_factor + 
                     coverage_factor + deductible_factor + experience_factor + 
                     accident_factor + violation_factor)
    
    monthly_premium = round(annual_premium / 12, 2)
    
    return {
        "monthly_premium": monthly_premium,
        "annual_premium": round(annual_premium, 2),
        "vehicle": f"{vehicle_year} {vehicle_make} {vehicle_model}",
        "coverage_summary": {
            "liability": liability_limit,
            "collision": collision,
            "comprehensive": comprehensive,
            "deductible": f"${deductible}"
        },
        "breakdown": {
            "base_rate": base_rate,
            "age_adjustment": {"amount": age_factor, "reason": age_explanation},
            "vehicle_age": {"amount": vehicle_factor, "reason": vehicle_explanation},
            "coverage_cost": coverage_factor + liability_factor,
            "driver_history": experience_factor + accident_factor + violation_factor,
            "deductible_discount": deductible_factor
        }
    }

@tool
def calculate_home_premium(
    year_built: int,
    square_footage: int,
    construction_type: str,
    roof_type: str,
    dwelling_coverage: int,
    stories: int = 1,
    security_system: bool = False,
    fire_alarm: bool = False,
    has_pool: bool = False
) -> dict:
    """Calculate home insurance premium based on property characteristics"""
    
    base_rate = 1200
    coverage_factor = dwelling_coverage / 1000
    
    # Property age
    property_age = 2025 - year_built
    if property_age > 50:
        age_factor = 400
        age_explanation = "Older home surcharge"
    elif property_age > 30:
        age_factor = 200
        age_explanation = "Mature home adjustment"
    elif property_age < 10:
        age_factor = -100
        age_explanation = "New home discount"
    else:
        age_factor = 0
        age_explanation = "Standard age"
    
    # Construction
    construction_factors = {
        "frame": (200, "Wood frame construction"),
        "brick": (0, "Brick construction"),
        "stone": (-100, "Stone construction discount"),
        "concrete": (-150, "Concrete construction discount")
    }
    construction_factor, construction_explanation = construction_factors.get(
        construction_type, (0, "Standard construction")
    )
    
    # Other factors
    size_factor = (square_footage - 2000) / 10
    stories_factor = (stories - 1) * 100
    safety_discount = (-100 if security_system else 0) + (-75 if fire_alarm else 0)
    pool_factor = 150 if has_pool else 0
    
    annual_premium = (base_rate + coverage_factor + age_factor + construction_factor + 
                     size_factor + stories_factor + safety_discount + pool_factor)
    
    monthly_premium = round(annual_premium / 12, 2)
    
    return {
        "monthly_premium": monthly_premium,
        "annual_premium": round(annual_premium, 2),
        "property_info": {
            "year_built": year_built,
            "square_footage": square_footage,
            "construction": construction_type,
            "stories": stories
        },
        "coverage_summary": {
            "dwelling": f"${dwelling_coverage:,}",
            "features": {
                "security_system": security_system,
                "fire_alarm": fire_alarm,
                "pool": has_pool
            }
        },
        "breakdown": {
            "base_rate": base_rate,
            "coverage_cost": coverage_factor,
            "property_age": {"amount": age_factor, "reason": age_explanation},
            "construction": {"amount": construction_factor, "reason": construction_explanation},
            "size_adjustment": size_factor,
            "safety_discounts": safety_discount,
            "pool_surcharge": pool_factor
        }
    }

# ============================================================================
# GRAPH NODES
# ============================================================================

def gather_info_node(state: AgentState) -> AgentState:
    """Node: Gather information from user through conversation"""
    print("\n🔵 NODE: gather_info")
    
    # This node uses the LLM to have a conversation
    # The actual conversation happens in the chat endpoint
    # This node just marks that we're in info-gathering mode
    
    state["next_action"] = "check_if_ready"
    return state

def search_knowledge_node(state: AgentState) -> AgentState:
    """Node: Search knowledge base for relevant information"""
    print("\n🔵 NODE: search_knowledge")
    
    # Get the last user message
    last_message = state["messages"][-1].content if state["messages"] else ""
    insurance_type = state.get("insurance_type")
    
    # Search RAG system
    context = get_relevant_context(last_message, insurance_type)
    state["knowledge_context"] = context
    
    print(f"   📚 Found relevant context ({len(context)} chars)")
    
    state["next_action"] = "respond_with_context"
    return state

def calculate_quote_node(state: AgentState) -> AgentState:
    """Node: Calculate insurance quote using tools"""
    print("\n🔵 NODE: calculate_quote")
    
    # Extract user info from state
    user_info = state.get("user_info", {})
    insurance_type = state.get("insurance_type")
    
    if insurance_type == "auto":
        result = calculate_auto_premium.invoke(user_info)
    elif insurance_type == "home":
        result = calculate_home_premium.invoke(user_info)
    else:
        result = {"error": "Unknown insurance type"}
    
    state["quote_result"] = result
    state["next_action"] = "explain_quote"
    
    print(f"   💰 Calculated premium: ${result.get('monthly_premium', 0)}/month")
    
    return state

def explain_results_node(state: AgentState) -> AgentState:
    """Node: Explain the quote results to the user"""
    print("\n🔵 NODE: explain_results")
    
    # This node prepares the explanation
    # The actual response is generated by the LLM
    
    state["next_action"] = "complete"
    return state

# ============================================================================
# CONDITIONAL EDGES (Decision Logic)
# ============================================================================

def should_search_knowledge(state: AgentState) -> str:
    """Decide if we should search the knowledge base"""
    last_message = state["messages"][-1].content.lower() if state["messages"] else ""
    
    # Search if user asks questions about coverage, discounts, etc.
    search_keywords = ["what is", "explain", "tell me about", "how does", "difference between"]
    
    if any(keyword in last_message for keyword in search_keywords):
        return "search"
    
    # Check if we have enough info to calculate
    user_info = state.get("user_info", {})
    insurance_type = state.get("insurance_type")
    
    if insurance_type == "auto" and all(k in user_info for k in ["age", "vehicle_year", "years_licensed"]):
        return "calculate"
    elif insurance_type == "home" and all(k in user_info for k in ["year_built", "square_footage", "dwelling_coverage"]):
        return "calculate"
    
    return "gather_more"

# ============================================================================
# BUILD THE GRAPH
# ============================================================================

def create_agent_graph():
    """Create the LangGraph workflow"""
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("gather_info", gather_info_node)
    workflow.add_node("search_knowledge", search_knowledge_node)
    workflow.add_node("calculate_quote", calculate_quote_node)
    workflow.add_node("explain_results", explain_results_node)
    
    # Set entry point
    workflow.set_entry_point("gather_info")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "gather_info",
        should_search_knowledge,
        {
            "search": "search_knowledge",
            "calculate": "calculate_quote",
            "gather_more": "gather_info"  # Loop back
        }
    )
    
    # Add regular edges
    workflow.add_edge("search_knowledge", "gather_info")
    workflow.add_edge("calculate_quote", "explain_results")
    workflow.add_edge("explain_results", END)
    
    # Compile
    app = workflow.compile()
    
    return app

# Create the graph
agent_graph = create_agent_graph()

# ============================================================================
# VISUALIZATION
# ============================================================================

def generate_graph_visualization():
    """Generate Mermaid diagram of the agent graph"""
    try:
        # Save as PNG
        agent_graph.get_graph().draw_mermaid_png(output_file_path="agent_graph.png")
        print("✅ Graph visualization saved to agent_graph.png")
        
        # Also return Mermaid code
        mermaid_code = agent_graph.get_graph().draw_mermaid()
        return mermaid_code
    except Exception as e:
        print(f"⚠️  Could not generate visualization: {e}")
        return None

# Generate visualization on import
try:
    mermaid_diagram = generate_graph_visualization()
except Exception as e:
    print(f"⚠️  Visualization will be generated on first run: {e}")
