"""
Agentic AI Insurance Agent - Pure Google Gemini
No LangChain needed - uses native Gemini function calling
"""

import google.generativeai as genai
import os
from typing import Dict, Any
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ============================================================================
# TOOL DEFINITIONS (Google's Native Format)
# ============================================================================

calculate_auto_premium_declaration = {
    "name": "calculate_auto_premium",
    "description": "Calculate auto insurance premium based on comprehensive driver profile and vehicle details. Use this when you have gathered enough information about the driver and their vehicle.",
    "parameters": {
        "type": "object",
        "properties": {
            "age": {
                "type": "integer",
                "description": "Driver's age in years"
            },
            "vehicle_year": {
                "type": "integer",
                "description": "Year the vehicle was manufactured"
            },
            "vehicle_make": {
                "type": "string",
                "description": "Vehicle manufacturer (e.g., Toyota, Honda, Ford)"
            },
            "vehicle_model": {
                "type": "string",
                "description": "Vehicle model name (e.g., Camry, Civic, F-150)"
            },
            "years_licensed": {
                "type": "integer",
                "description": "Number of years the driver has been licensed"
            },
            "accidents": {
                "type": "integer",
                "description": "Number of at-fault accidents in the last 3 years"
            },
            "violations": {
                "type": "integer",
                "description": "Number of traffic violations in the last 3 years"
            },
            "liability_limit": {
                "type": "string",
                "description": "Desired liability coverage limit",
                "enum": ["50000/100000", "100000/300000", "250000/500000", "500000/1000000"]
            },
            "collision": {
                "type": "boolean",
                "description": "Whether to include collision coverage"
            },
            "comprehensive": {
                "type": "boolean",
                "description": "Whether to include comprehensive coverage"
            },
            "deductible": {
                "type": "integer",
                "description": "Deductible amount in dollars",
                "enum": [250, 500, 1000, 2500]
            }
        },
        "required": ["age", "vehicle_year", "years_licensed", "accidents", "violations"]
    }
}

calculate_home_premium_declaration = {
    "name": "calculate_home_premium",
    "description": "Calculate home insurance premium based on property characteristics and coverage needs. Use this when you have gathered enough information about the property.",
    "parameters": {
        "type": "object",
        "properties": {
            "year_built": {
                "type": "integer",
                "description": "Year the home was built"
            },
            "square_footage": {
                "type": "integer",
                "description": "Total square footage of the home"
            },
            "construction_type": {
                "type": "string",
                "description": "Primary construction material",
                "enum": ["frame", "brick", "stone", "concrete"]
            },
            "roof_type": {
                "type": "string",
                "description": "Type of roofing material",
                "enum": ["asphalt_shingle", "metal", "tile", "slate"]
            },
            "dwelling_coverage": {
                "type": "integer",
                "description": "Desired dwelling coverage amount in dollars"
            },
            "stories": {
                "type": "integer",
                "description": "Number of stories",
                "enum": [1, 2, 3]
            },
            "security_system": {
                "type": "boolean",
                "description": "Whether the home has a security system"
            },
            "fire_alarm": {
                "type": "boolean",
                "description": "Whether the home has a fire/smoke alarm system"
            },
            "has_pool": {
                "type": "boolean",
                "description": "Whether the property has a swimming pool"
            }
        },
        "required": ["year_built", "square_footage", "construction_type", "dwelling_coverage"]
    }
}

# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def calculate_auto_premium(**kwargs) -> Dict[str, Any]:
    """Calculate auto insurance premium with detailed breakdown"""
    
    # Extract parameters with defaults
    age = kwargs.get('age', 30)
    vehicle_year = kwargs.get('vehicle_year', 2020)
    vehicle_make = kwargs.get('vehicle_make', 'Unknown')
    vehicle_model = kwargs.get('vehicle_model', 'Unknown')
    years_licensed = kwargs.get('years_licensed', 10)
    accidents = kwargs.get('accidents', 0)
    violations = kwargs.get('violations', 0)
    liability_limit = kwargs.get('liability_limit', '100000/300000')
    collision = kwargs.get('collision', True)
    comprehensive = kwargs.get('comprehensive', True)
    deductible = kwargs.get('deductible', 500)
    
    # Base rate
    base_rate = 800
    
    # Age factor (younger drivers pay more)
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
    
    # Vehicle age factor
    current_year = 2025
    vehicle_age = current_year - vehicle_year
    if vehicle_age > 10:
        vehicle_factor = -100
        vehicle_explanation = "Older vehicle discount"
    elif vehicle_age < 3:
        vehicle_factor = 200
        vehicle_explanation = "New vehicle premium"
    else:
        vehicle_factor = 0
        vehicle_explanation = "Standard vehicle age"
    
    # Coverage factors
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
    
    # Calculate total
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

def calculate_home_premium(**kwargs) -> Dict[str, Any]:
    """Calculate home insurance premium with detailed breakdown"""
    
    # Extract parameters
    year_built = kwargs.get('year_built', 2000)
    square_footage = kwargs.get('square_footage', 2000)
    construction_type = kwargs.get('construction_type', 'frame')
    roof_type = kwargs.get('roof_type', 'asphalt_shingle')
    dwelling_coverage = kwargs.get('dwelling_coverage', 250000)
    stories = kwargs.get('stories', 1)
    security_system = kwargs.get('security_system', False)
    fire_alarm = kwargs.get('fire_alarm', False)
    has_pool = kwargs.get('has_pool', False)
    
    # Base rate
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
    
    # Construction type
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
    
    # Calculate total
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

# Function mapping
AVAILABLE_FUNCTIONS = {
    "calculate_auto_premium": calculate_auto_premium,
    "calculate_home_premium": calculate_home_premium
}

# ============================================================================
# GEMINI AGENT
# ============================================================================

# Initialize model with function calling
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[calculate_auto_premium_declaration, calculate_home_premium_declaration]
)

# Chat session storage (in-memory for demo)
chat_sessions = {}

SYSTEM_INSTRUCTION = """You are an expert insurance agent powered by AI. Your name is AgenticInsure Assistant.

Your role is to:
1. **Understand Customer Needs**: Have natural conversations to understand what type of insurance they need (auto or home)
2. **Gather Information**: Ask clarifying questions to collect necessary details
3. **Use Your Tools**: Call calculate_auto_premium or calculate_home_premium when you have enough information
4. **Explain Clearly**: Break down how premiums are calculated, explain the breakdown
5. **Be Proactive**: Suggest coverage options, explain trade-offs, help them make informed decisions

Guidelines:
- Be conversational and friendly
- Ask one or two questions at a time (don't overwhelm)
- When you have enough info, use your calculation tools
- After calculating, explain the quote clearly with the breakdown
- Suggest ways to lower premiums if appropriate
- Be transparent about how you arrived at the quote

Example conversation flow:
User: "I need car insurance"
You: "I'd be happy to help you get an auto insurance quote! To give you an accurate estimate, I need some information. Let's start with:
- How old are you?
- What vehicle do you drive (year, make, and model)?"

User: "I'm 28 and drive a 2020 Honda Civic"
You: "Great! The Honda Civic is a reliable choice. A few more questions:
- How many years have you been licensed to drive?
- Have you had any at-fault accidents or traffic violations in the last 3 years?"

[Continue gathering info, then call calculate_auto_premium]

You: "Based on your profile, I've calculated your quote. Your monthly premium would be $X. Here's how I arrived at that number: [explain breakdown]. Would you like me to explore options to potentially lower this?"

Be helpful, transparent, and guide them through the process naturally."""

def chat_with_agent(message: str, session_id: str) -> str:
    """
    Chat with the Gemini agent using native function calling.
    Gemini handles all orchestration automatically!
    """
    
    # Get or create chat session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])
        # Send system instruction as first message
        chat_sessions[session_id].send_message(SYSTEM_INSTRUCTION)
    
    chat = chat_sessions[session_id]
    
    # Send user message
    response = chat.send_message(message)
    
    # Handle function calls (Gemini's native orchestration)
    while response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        function_args = dict(function_call.args)
        
        print(f"[Agent] Calling function: {function_name}")
        print(f"[Agent] Arguments: {json.dumps(function_args, indent=2)}")
        
        # Execute the function
        if function_name in AVAILABLE_FUNCTIONS:
            function_result = AVAILABLE_FUNCTIONS[function_name](**function_args)
            print(f"[Agent] Result: {json.dumps(function_result, indent=2)}")
            
            # Send result back to Gemini
            response = chat.send_message(
                genai.protos.Content(
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": function_result}
                        )
                    )]
                )
            )
        else:
            break
    
    # Return final text response
    return response.text

def reset_session(session_id: str):
    """Reset a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
