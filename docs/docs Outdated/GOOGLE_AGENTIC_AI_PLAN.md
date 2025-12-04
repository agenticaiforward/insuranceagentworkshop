# Google-Powered Agentic AI Insurance Agent - Architecture

## Recommended Google Stack

### 1. **LLM & AI Foundation**
- **Gemini 2.0 Flash** (via Vertex AI)
  - Latest model with function calling
  - Multimodal (text, images, PDFs)
  - Fast and cost-effective
  - Native tool/function calling support

### 2. **Agent Framework**
- **LangChain with Gemini**
  - Industry-standard agent framework
  - Built-in support for Google Gemini
  - Tool orchestration and memory
  
### 3. **Document Intelligence**
- **Google Document AI**
  - OCR for uploaded insurance documents
  - Structured data extraction
  - Pre-trained insurance document processors

### 4. **Vector Database & Memory**
- **Google Cloud Firestore** (for session data)
- **Vertex AI Vector Search** (for semantic memory)
  - Store conversation history
  - Retrieve relevant context

### 5. **Backend**
- **Google Cloud Run** (Python FastAPI)
  - Serverless, auto-scaling
  - Easy deployment
  - Integrated with Vertex AI

### 6. **Frontend**
- **Firebase Hosting** (React app)
  - Fast CDN
  - Free SSL
  - Easy deployment

### 7. **Additional Google Services**
- **Cloud Storage**: Store uploaded documents
- **Cloud Functions**: Event-driven processing
- **Secret Manager**: API keys
- **Cloud Logging**: Monitor agent behavior

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                    (Web Browser)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND (Firebase Hosting)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React Chat Interface                                │  │
│  │  - Natural language input                            │  │
│  │  - Streaming responses                               │  │
│  │  - Document upload                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │ WebSocket / REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           BACKEND (Cloud Run - FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LangChain Agent Orchestrator                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Gemini 2.0 Flash (Vertex AI)                  │  │  │
│  │  │  - Conversational reasoning                    │  │  │
│  │  │  - Function calling                            │  │  │
│  │  │  - Multi-step planning                         │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                        │  │
│  │  Agent Tools:                                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ Calculate    │  │ Document     │  │ Search     │  │  │
│  │  │ Premium      │  │ Analysis     │  │ Database   │  │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌─────────────────┐
│ Document AI  │ │Firestore │ │ Vertex Vector   │
│ (OCR/Extract)│ │(Sessions)│ │ Search (Memory) │
└──────────────┘ └──────────┘ └─────────────────┘
```

---

## Implementation Plan

### Phase 1: Setup Google Cloud
```bash
# Install Google Cloud SDK
gcloud init

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  documentai.googleapis.com \
  run.googleapis.com \
  firestore.googleapis.com

# Set up authentication
gcloud auth application-default login
```

### Phase 2: Backend with Gemini Agent

**Install Dependencies:**
```bash
pip install \
  google-cloud-aiplatform \
  google-cloud-documentai \
  google-cloud-firestore \
  langchain-google-vertexai \
  fastapi \
  uvicorn
```

**Agent Implementation:**
```python
from langchain_google_vertexai import ChatVertexAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from google.cloud import documentai_v1 as documentai
from google.cloud import firestore

# Initialize Gemini
llm = ChatVertexAI(
    model_name="gemini-2.0-flash-exp",
    project="your-project-id",
    location="us-central1",
    temperature=0.7,
)

# Define Tools
@tool
def calculate_auto_premium(
    age: int,
    vehicle_year: int,
    accidents: int,
    violations: int
) -> dict:
    """Calculate auto insurance premium based on driver profile."""
    # Your calculation logic
    return {"monthly_premium": 125.50, "reasoning": "..."}

@tool
def analyze_insurance_document(file_path: str) -> dict:
    """Extract data from uploaded insurance document using Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    # Process document
    # Extract: provider, premium, coverage, etc.
    return {"provider": "State Farm", "current_premium": 150}

@tool
def search_vehicle_database(make: str, model: str, year: int) -> dict:
    """Look up vehicle safety ratings and value."""
    # Call external API or database
    return {"safety_rating": 5, "avg_value": 25000}

# Create Agent
tools = [calculate_auto_premium, analyze_insurance_document, search_vehicle_database]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert insurance agent. Your goal is to:
    1. Have a natural conversation to understand the customer's needs
    2. Use your tools to gather accurate information
    3. Provide personalized quotes with clear explanations
    4. Be proactive - suggest coverage options they might not know about
    
    Always explain your reasoning and be transparent about how you calculate quotes."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# FastAPI Endpoint
@app.post("/api/chat")
async def chat(message: str, session_id: str):
    # Get conversation history from Firestore
    db = firestore.Client()
    history = get_conversation_history(db, session_id)
    
    # Run agent
    response = agent_executor.invoke({
        "input": message,
        "chat_history": history
    })
    
    # Save to Firestore
    save_message(db, session_id, message, response)
    
    return {"response": response["output"]}
```

### Phase 3: Document Intelligence

```python
from google.cloud import documentai

def process_insurance_document(file_content: bytes, mime_type: str):
    client = documentai.DocumentProcessorServiceClient()
    
    # Use pre-trained insurance processor
    processor_name = "projects/PROJECT/locations/us/processors/PROCESSOR_ID"
    
    document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type
    )
    
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=document
    )
    
    result = client.process_document(request=request)
    
    # Extract structured data
    extracted = {
        "provider": None,
        "policy_number": None,
        "premium": None,
        "coverage": {}
    }
    
    for entity in result.document.entities:
        if entity.type_ == "provider":
            extracted["provider"] = entity.mention_text
        elif entity.type_ == "premium":
            extracted["premium"] = float(entity.mention_text.replace("$", ""))
    
    return extracted
```

### Phase 4: Frontend Chat Interface

```javascript
// React component with streaming
import { useState } from 'react';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    
    // Call backend
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: input,
        session_id: sessionStorage.getItem('session_id')
      })
    });
    
    const data = await response.json();
    const agentMessage = { role: 'agent', content: data.response };
    setMessages([...messages, userMessage, agentMessage]);
    setInput('');
  };
  
  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Ask me about insurance..."
      />
    </div>
  );
}
```

---

## Cost Estimate (Google Cloud)

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| Gemini 2.0 Flash | 1M tokens | ~$0.50 |
| Document AI | 1000 docs | ~$15 |
| Cloud Run | 100K requests | ~$5 |
| Firestore | 10GB storage | ~$2 |
| Vector Search | 1M queries | ~$10 |
| **Total** | | **~$32.50/month** |

---

## Key Advantages of Google Stack

1. **Gemini 2.0 Flash**: Latest model, multimodal, fast
2. **Document AI**: Pre-trained for insurance documents
3. **Integrated**: All services work seamlessly together
4. **Vertex AI**: Enterprise-grade ML platform
5. **Cost-Effective**: Competitive pricing
6. **Scalable**: Auto-scaling with Cloud Run

---

## Next Steps

1. **Set up Google Cloud Project**
2. **Enable Vertex AI and Document AI**
3. **Rebuild backend with LangChain + Gemini**
4. **Replace forms with chat interface**
5. **Add document processing**
6. **Deploy to Cloud Run**

**Should I proceed with rebuilding this as a TRUE Agentic AI system using the Google stack?**
