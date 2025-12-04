# FREE Agentic AI with Pure Google Stack (No LangChain)

## 100% Google Native Solution

Google now provides **native function calling** and **multi-turn conversations** directly in the Gemini API - no need for LangChain!

---

## Pure Google Stack

| Component | Google Service | Cost |
|-----------|---------------|------|
| **LLM & Orchestration** | Gemini 1.5 Flash API | FREE (1500/day) |
| **Function Calling** | Built into Gemini | FREE |
| **Multi-turn Chat** | Gemini Chat Sessions | FREE |
| **Document Analysis** | Gemini Multimodal | FREE |
| **Backend** | Cloud Run | FREE (2M req/month) |
| **Frontend** | Firebase Hosting | FREE (10GB) |
| **Storage** | Firestore | FREE (1GB) |

**Total: $0/month**

---

## Implementation (Pure Google - No LangChain)

### Step 1: Install Only Google SDK

```bash
pip install google-generativeai fastapi uvicorn python-dotenv
```

That's it! No LangChain needed.

---

### Step 2: Backend with Native Gemini Function Calling

**backend/agent.py:**
```python
import google.generativeai as genai
import os
from typing import Dict, List
import json

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define function declarations (Google's native format)
calculate_auto_premium_func = {
    "name": "calculate_auto_premium",
    "description": "Calculate auto insurance premium based on driver profile and vehicle details",
    "parameters": {
        "type": "object",
        "properties": {
            "age": {
                "type": "integer",
                "description": "Driver's age"
            },
            "vehicle_year": {
                "type": "integer",
                "description": "Year the vehicle was manufactured"
            },
            "years_licensed": {
                "type": "integer",
                "description": "Number of years the driver has been licensed"
            },
            "accidents": {
                "type": "integer",
                "description": "Number of accidents in last 3 years"
            },
            "violations": {
                "type": "integer",
                "description": "Number of traffic violations in last 3 years"
            },
            "liability_limit": {
                "type": "string",
                "description": "Liability coverage limit (e.g., '100000/300000')"
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
                "description": "Deductible amount in dollars"
            }
        },
        "required": ["age", "vehicle_year", "years_licensed", "accidents", "violations"]
    }
}

calculate_home_premium_func = {
    "name": "calculate_home_premium",
    "description": "Calculate home insurance premium based on property characteristics",
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
                "description": "Type of construction (frame, brick, stone, concrete)"
            },
            "dwelling_coverage": {
                "type": "integer",
                "description": "Desired dwelling coverage amount in dollars"
            },
            "stories": {
                "type": "integer",
                "description": "Number of stories"
            },
            "security_system": {
                "type": "boolean",
                "description": "Whether home has security system"
            },
            "fire_alarm": {
                "type": "boolean",
                "description": "Whether home has fire alarm"
            },
            "has_pool": {
                "type": "boolean",
                "description": "Whether property has a pool"
            }
        },
        "required": ["year_built", "square_footage", "construction_type", "dwelling_coverage"]
    }
}

# Tool implementations
def calculate_auto_premium(**kwargs):
    """Calculate auto insurance premium"""
    base_rate = 800
    age = kwargs.get('age', 30)
    vehicle_year = kwargs.get('vehicle_year', 2020)
    years_licensed = kwargs.get('years_licensed', 10)
    accidents = kwargs.get('accidents', 0)
    violations = kwargs.get('violations', 0)
    liability_limit = kwargs.get('liability_limit', '100000/300000')
    collision = kwargs.get('collision', True)
    comprehensive = kwargs.get('comprehensive', True)
    deductible = kwargs.get('deductible', 500)
    
    # Age factor
    if age < 25:
        age_factor = 400
    elif age < 30:
        age_factor = 200
    elif age > 65:
        age_factor = 150
    else:
        age_factor = 0
    
    # Vehicle age
    vehicle_age = 2025 - vehicle_year
    if vehicle_age > 10:
        vehicle_factor = -100
    elif vehicle_age < 3:
        vehicle_factor = 200
    else:
        vehicle_factor = 0
    
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
        "breakdown": {
            "base_rate": base_rate,
            "age_adjustment": age_factor,
            "vehicle_age_adjustment": vehicle_factor,
            "coverage_cost": coverage_factor + liability_factor,
            "driver_history_impact": experience_factor + accident_factor + violation_factor
        }
    }

def calculate_home_premium(**kwargs):
    """Calculate home insurance premium"""
    base_rate = 1200
    year_built = kwargs.get('year_built', 2000)
    square_footage = kwargs.get('square_footage', 2000)
    construction_type = kwargs.get('construction_type', 'frame')
    dwelling_coverage = kwargs.get('dwelling_coverage', 250000)
    stories = kwargs.get('stories', 1)
    security_system = kwargs.get('security_system', False)
    fire_alarm = kwargs.get('fire_alarm', False)
    has_pool = kwargs.get('has_pool', False)
    
    coverage_factor = dwelling_coverage / 1000
    property_age = 2025 - year_built
    
    if property_age > 50:
        age_factor = 400
    elif property_age > 30:
        age_factor = 200
    elif property_age < 10:
        age_factor = -100
    else:
        age_factor = 0
    
    construction_factors = {"frame": 200, "brick": 0, "stone": -100, "concrete": -150}
    construction_factor = construction_factors.get(construction_type, 0)
    
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
        "breakdown": {
            "base_rate": base_rate,
            "coverage_cost": coverage_factor,
            "property_age_adjustment": age_factor,
            "construction_adjustment": construction_factor,
            "safety_discount": safety_discount
        }
    }

# Function mapping
available_functions = {
    "calculate_auto_premium": calculate_auto_premium,
    "calculate_home_premium": calculate_home_premium
}

# Initialize model with function calling
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[calculate_auto_premium_func, calculate_home_premium_func]
)

# Chat session storage (in-memory for demo, use Firestore in production)
chat_sessions = {}

def chat_with_agent(message: str, session_id: str) -> str:
    """
    Chat with the Gemini agent using native function calling.
    Google handles all the orchestration automatically!
    """
    
    # Get or create chat session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])
    
    chat = chat_sessions[session_id]
    
    # System instruction (set once at start)
    if len(chat.history) == 0:
        system_message = """You are an expert insurance agent. Your role is to:

1. Have natural conversations to understand customer needs
2. Ask clarifying questions to gather necessary information
3. Use your calculate_auto_premium and calculate_home_premium functions when you have enough data
4. Explain quotes clearly, breaking down how premiums are calculated
5. Be proactive in suggesting coverage options

Example flow:
- User: "I need car insurance"
- You: "I'd be happy to help! To give you an accurate quote, I need:
       - Your age?
       - What vehicle do you drive (year, make, model)?
       - How many years have you been licensed?
       - Any accidents or violations in the last 3 years?"
- User provides info
- You: [Call calculate_auto_premium function]
- You: "Based on your profile, your quote is $X/month. Here's the breakdown..."

Be conversational, helpful, and transparent."""
        
        # Send system instruction
        chat.send_message(system_message)
    
    # Send user message
    response = chat.send_message(message)
    
    # Handle function calls (Google's native orchestration)
    while response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        function_args = dict(function_call.args)
        
        # Execute the function
        if function_name in available_functions:
            function_result = available_functions[function_name](**function_args)
            
            # Send result back to model
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
    
    # Return final text response
    return response.text
```

**backend/main.py:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import chat_with_agent
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Chat with Gemini agent (Google handles all orchestration!)
    response = chat_with_agent(request.message, session_id)
    
    return {
        "response": response,
        "session_id": session_id
    }

@app.get("/")
def read_root():
    return {"message": "Agentic Insurance Agent - Powered by Google Gemini"}
```

---

## Key Advantages of Pure Google Stack

✅ **No LangChain dependency** - simpler, fewer packages
✅ **Native function calling** - Google handles orchestration automatically
✅ **Built-in chat sessions** - conversation memory included
✅ **Multimodal support** - can analyze images/PDFs natively
✅ **Faster** - direct API calls, no middleware
✅ **100% FREE** - within Gemini API free tier

---

## How Google's Native Orchestration Works

```python
# 1. You define functions in Google's format
tools = [calculate_auto_premium_func, calculate_home_premium_func]

# 2. Create model with tools
model = genai.GenerativeModel('gemini-1.5-flash', tools=tools)

# 3. Start chat
chat = model.start_chat()

# 4. Send message - Gemini decides if it needs to call a function
response = chat.send_message("I need car insurance for my 2020 Honda")

# 5. If Gemini calls a function, you execute it and send result back
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    result = execute_function(function_call.name, function_call.args)
    response = chat.send_message(function_response=result)

# 6. Get final answer
print(response.text)
```

**Google handles:**
- ✅ Deciding when to call functions
- ✅ Extracting parameters from conversation
- ✅ Multi-step reasoning
- ✅ Conversation memory
- ✅ Error handling

---

## Comparison: LangChain vs Pure Google

| Feature | LangChain | Pure Google |
|---------|-----------|-------------|
| Dependencies | 10+ packages | 1 package |
| Lines of code | ~200 | ~100 |
| Orchestration | LangChain handles | Gemini handles |
| Function calling | Via LangChain tools | Native Gemini |
| Chat memory | LangChain memory | Native chat sessions |
| Learning curve | Medium | Easy |
| Performance | Good | Faster (direct API) |

---

## Next Steps

1. **Get Gemini API key** from https://aistudio.google.com/
2. **Install**: `pip install google-generativeai fastapi uvicorn`
3. **Copy the code above**
4. **Run**: `uvicorn main:app --reload`
5. **Test**: Send messages to `/api/chat`

**Ready to implement this pure Google solution?**
