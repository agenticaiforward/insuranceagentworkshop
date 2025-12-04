from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from gemini_agent import chat_with_agent, reset_session

app = FastAPI(title="Agentic Insurance Agent - Powered by Google Gemini")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.get("/")
def read_root():
    return {
        "message": "Agentic Insurance Agent - Powered by Google Gemini",
        "version": "2.0 - TRUE Agentic AI",
        "features": [
            "Natural language conversation",
            "AI-powered reasoning",
            "Function calling for premium calculations",
            "Multi-turn dialogue with memory"
        ]
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the Agentic AI Insurance Agent.
    Gemini handles all orchestration, function calling, and reasoning.
    """
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        # Chat with Gemini agent (all orchestration handled by Gemini!)
        response = chat_with_agent(request.message, session_id)
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
    except Exception as e:
        # Handle errors gracefully
        error_message = f"I apologize, but I encountered an error: {str(e)}. Could you please rephrase your question?"
        return ChatResponse(
            response=error_message,
            session_id=session_id
        )

@app.post("/api/reset")
async def reset(session_id: str):
    """Reset a chat session"""
    reset_session(session_id)
    return {"message": "Session reset successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "agent": "gemini-1.5-flash"}
