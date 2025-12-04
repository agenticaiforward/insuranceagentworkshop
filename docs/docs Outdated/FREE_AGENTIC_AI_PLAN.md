# FREE Agentic AI Insurance Agent - Google Stack

## 100% Free Implementation Plan

### Free Google Services (Within Limits)

| Service | Free Tier | What We'll Use It For |
|---------|-----------|----------------------|
| **Gemini API** | 15 requests/min, 1500/day | LLM reasoning & chat |
| **Google AI Studio** | Free forever | API key generation |
| **Firebase Hosting** | 10GB storage, 360MB/day | Frontend hosting |
| **Firestore** | 1GB storage, 50K reads/day | Session storage |
| **Cloud Run** | 2M requests/month | Backend hosting |
| **Cloud Storage** | 5GB storage | Document uploads |

**Total Cost: $0/month** (within free tier limits)

---

## Architecture (Free Version)

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Web Browser)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         FRONTEND (Firebase Hosting - FREE)                  │
│  React Chat Interface + Document Upload                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│      BACKEND (Cloud Run - FREE 2M requests/month)           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LangChain + Gemini 1.5 Flash (FREE API)             │  │
│  │  - Conversational AI                                 │  │
│  │  - Function calling                                  │  │
│  │  - Document understanding (multimodal)              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Tools:                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐        │
│  │ Calculate    │  │ Analyze      │  │ Search     │        │
│  │ Premium      │  │ Document     │  │ Data       │        │
│  └──────────────┘  └──────────────┘  └────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Firestore (FREE 1GB storage)                      │
│  - Conversation history                                     │
│  - User sessions                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation

### Step 1: Get Free Gemini API Key

1. Go to **Google AI Studio**: https://aistudio.google.com/
2. Click "Get API Key"
3. Create a new API key (FREE, no credit card required)
4. Copy the key

**Free Limits:**
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per day
- **Perfect for development and demos!**

---

### Step 2: Setup Local Development (FREE)

```bash
# Backend setup
cd insurance_agent/backend
pip install \
  google-generativeai \
  langchain-google-genai \
  langchain \
  fastapi \
  uvicorn

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

---

### Step 3: Implement Agentic Backend (FREE)

**backend/agent.py:**
```python
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import google.generativeai as genai

# Configure Gemini (FREE API)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini 1.5 Flash (FREE)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Define Tools
@tool
def calculate_auto_premium(
    age: int,
    vehicle_year: int,
    years_licensed: int,
    accidents: int,
    violations: int,
    liability_limit: str,
    collision: bool,
    comprehensive: bool,
    deductible: int
) -> dict:
    """Calculate auto insurance premium based on comprehensive driver profile."""
    base_rate = 800
    
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
    current_year = 2025
    vehicle_age = current_year - vehicle_year
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
    
    # Calculate
    annual_premium = (base_rate + age_factor + vehicle_factor + 
                     liability_factor + coverage_factor + deductible_factor + 
                     experience_factor + accident_factor + violation_factor)
    
    monthly_premium = round(annual_premium / 12, 2)
    
    return {
        "monthly_premium": monthly_premium,
        "annual_premium": round(annual_premium, 2),
        "breakdown": {
            "base": base_rate,
            "age_adjustment": age_factor,
            "vehicle_age": vehicle_factor,
            "coverage": coverage_factor + liability_factor,
            "driver_history": experience_factor + accident_factor + violation_factor
        }
    }

@tool
def calculate_home_premium(
    year_built: int,
    square_footage: int,
    construction_type: str,
    roof_type: str,
    dwelling_coverage: int,
    stories: int,
    security_system: bool,
    fire_alarm: bool,
    has_pool: bool
) -> dict:
    """Calculate home insurance premium based on property characteristics."""
    base_rate = 1200
    coverage_factor = dwelling_coverage / 1000
    
    # Property age
    property_age = 2025 - year_built
    if property_age > 50:
        age_factor = 400
    elif property_age > 30:
        age_factor = 200
    elif property_age < 10:
        age_factor = -100
    else:
        age_factor = 0
    
    # Construction
    construction_factors = {
        "frame": 200,
        "brick": 0,
        "stone": -100,
        "concrete": -150
    }
    construction_factor = construction_factors.get(construction_type, 0)
    
    # Other factors
    size_factor = (square_footage - 2000) / 10
    stories_factor = (stories - 1) * 100
    safety_discount = (-100 if security_system else 0) + (-75 if fire_alarm else 0)
    pool_factor = 150 if has_pool else 0
    
    annual_premium = (base_rate + coverage_factor + age_factor + 
                     construction_factor + size_factor + stories_factor + 
                     safety_discount + pool_factor)
    
    monthly_premium = round(annual_premium / 12, 2)
    
    return {
        "monthly_premium": monthly_premium,
        "annual_premium": round(annual_premium, 2),
        "breakdown": {
            "base": base_rate,
            "coverage": coverage_factor,
            "property_age": age_factor,
            "construction": construction_factor,
            "safety_features": safety_discount
        }
    }

@tool
def analyze_uploaded_document(file_content: str) -> dict:
    """Analyze uploaded insurance document using Gemini's multimodal capabilities."""
    # Use Gemini's vision capabilities (FREE)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """Analyze this insurance document and extract:
    1. Insurance provider name
    2. Current monthly premium
    3. Coverage amounts
    4. Deductibles
    5. Policy type (auto/home)
    
    Return as structured JSON."""
    
    response = model.generate_content([prompt, file_content])
    
    # Parse response (simplified)
    return {
        "provider": "Extracted Provider",
        "current_premium": 150.00,
        "coverage_type": "auto",
        "extracted_data": response.text
    }

# Create Agent
tools = [calculate_auto_premium, calculate_home_premium, analyze_uploaded_document]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert insurance agent powered by AI. Your role is to:

1. **Understand Customer Needs**: Ask clarifying questions naturally
2. **Use Your Tools**: Call calculate_auto_premium or calculate_home_premium when you have enough info
3. **Explain Clearly**: Break down how premiums are calculated
4. **Be Proactive**: Suggest coverage options, explain trade-offs
5. **Handle Documents**: If user uploads a document, use analyze_uploaded_document

Example conversation flow:
- User: "I need car insurance"
- You: "I'd be happy to help! To give you an accurate quote, I need some information:
       - What's your age?
       - What vehicle do you drive (year, make, model)?
       - How long have you been licensed?
       - Any accidents or violations in the last 3 years?"
- User provides info
- You: [Use calculate_auto_premium tool]
- You: "Based on your profile, I calculated a quote of $X/month. Here's how I arrived at that..."

Be conversational, helpful, and transparent about your reasoning."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True
)

def chat_with_agent(message: str, history: list = None) -> str:
    """Main chat function"""
    try:
        response = agent_executor.invoke({
            "input": message,
            "chat_history": history or []
        })
        return response["output"]
    except Exception as e:
        return f"I encountered an error: {str(e)}. Could you rephrase that?"
```

**backend/main.py:**
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import chat_with_agent
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

# In-memory session storage (use Firestore for production)
sessions = {}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    
    # Get or create session history
    if session_id not in sessions:
        sessions[session_id] = []
    
    history = sessions[session_id]
    
    # Chat with agent
    response = chat_with_agent(request.message, history)
    
    # Update history
    sessions[session_id].append({"human": request.message, "ai": response})
    
    return {"response": response}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    # Read file
    content = await file.read()
    base64_content = base64.b64encode(content).decode()
    
    # Analyze with Gemini
    response = chat_with_agent(
        f"I'm uploading an insurance document. Please analyze it: {base64_content[:100]}..."
    )
    
    return {"analysis": response}
```

---

### Step 4: Create Chat Frontend (FREE)

**frontend/src/components/ChatInterface.jsx:**
```javascript
import React, { useState, useEffect, useRef } from 'react';
import { Send, Upload } from 'lucide-react';

function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hi! I\'m your AI insurance agent. I can help you get quotes for auto or home insurance. What would you like to know?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substr(2, 9));
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          session_id: sessionId
        })
      });

      const data = await response.json();
      const agentMessage = { role: 'agent', content: data.response };
      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'agent', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] rounded-2xl px-4 py-3 ${
              msg.role === 'user' 
                ? 'bg-accent text-white' 
                : 'bg-slate-100 text-slate-900'
            }`}>
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-2xl px-4 py-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
          placeholder="Ask me about insurance..."
          className="flex-1 rounded-full border border-slate-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent"
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          className="bg-accent text-white rounded-full p-3 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Send className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;
```

---

## Deployment (100% FREE)

### Deploy Backend to Cloud Run (FREE)
```bash
# Install Google Cloud SDK
gcloud init

# Deploy (within free tier: 2M requests/month)
gcloud run deploy insurance-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

### Deploy Frontend to Firebase (FREE)
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and init
firebase login
firebase init hosting

# Deploy (10GB storage, 360MB/day transfer - FREE)
npm run build
firebase deploy
```

---

## Free Tier Limits Summary

✅ **Gemini API**: 1,500 requests/day (FREE forever)
✅ **Cloud Run**: 2M requests/month (FREE)
✅ **Firebase Hosting**: 10GB storage (FREE)
✅ **Firestore**: 1GB storage, 50K reads/day (FREE)

**Perfect for:**
- Development
- Demos
- Workshops
- Small-scale production (< 1500 users/day)

---

## Next Steps

1. Get Gemini API key from AI Studio (FREE)
2. Install dependencies
3. Implement agent backend
4. Create chat frontend
5. Test locally
6. Deploy to Cloud Run + Firebase (FREE)

**Ready to build this FREE Agentic AI system?**
