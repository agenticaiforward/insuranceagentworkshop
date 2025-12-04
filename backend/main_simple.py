"""
Simple working backend for the insurance agent
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
from dotenv import load_dotenv

# Import LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

app = FastAPI(title="Insurance Agent")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Session storage
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.get("/health")
def health():
    return {"status": "healthy", "llm": "gemini-1.5-flash"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        if session_id not in sessions:
            sessions[session_id] = {"messages": []}
        
        session = sessions[session_id]
        
        # Add user message
        session["messages"].append(HumanMessage(content=request.message))
        
        # System prompt
        system_msg = HumanMessage(content="""You are a friendly insurance agent. 
Help customers with auto and home insurance quotes. Ask relevant questions and be helpful.""")
        
        # Get response from Gemini
        messages = [system_msg] + session["messages"]
        response = llm.invoke(messages)
        
        # Add AI response to session
        session["messages"].append(AIMessage(content=response.content))
        
        return ChatResponse(
            response=response.content,
            session_id=session_id
        )
    
    except Exception as e:
        print(f"Error: {e}")
        return ChatResponse(
            response=f"Error: {str(e)}",
            session_id=request.session_id or str(uuid.uuid4())
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
