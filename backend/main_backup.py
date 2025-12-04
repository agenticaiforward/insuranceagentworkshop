# main_backup.py – backup version of the FastAPI entry point
# This file mirrors the original ``main.py`` but adds a **toggle** that lets you
# decide at runtime whether the chat endpoint should go through the LangGraph
# workflow (the "brain") or use the simple direct Gemini LLM call.
#
# Usage:
#   * Set the environment variable ``USE_LANGGRAPH`` to ``yes`` or ``no``.
#   * Run the server as usual: ``uvicorn main_backup:app --host 0.0.0.0 --port 8001``.
#   * The toggle is checked on each request, so you can change it without
#     restarting the server (just update the env var).

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid

# ---------------------------------------------------------------------------
# Imports – optional LangGraph components (may be missing in some environments)
# ---------------------------------------------------------------------------
try:
    from langgraph_agent import agent_graph  # The LangGraph workflow
    HAS_LANGGRAPH = True
except Exception:
    HAS_LANGGRAPH = False
    # The backend will still work; the toggle will simply fall back to the LLM.

# Gemini LLM (used when LangGraph is disabled)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, AIMessage
    HAS_LANGCHAIN = True
except Exception:
    HAS_LANGCHAIN = False

# RAG system – optional but used by both paths
try:
    from rag_system import search_knowledge
    HAS_RAG = True
except Exception:
    HAS_RAG = False

# Load environment variables (including the toggle)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Insurance Agent – Backup",
    description="FastAPI backend with optional LangGraph integration",
    version="2.0",
)

# CORS – same as original
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In‑memory session store (same structure as the original app)
sessions = {}

# ---------------------------------------------------------------------------
# Helper – decide whether to use LangGraph for this request
# ---------------------------------------------------------------------------
def use_langgraph() -> bool:
    """Return ``True`` if the ``USE_LANGGRAPH`` env var is set to ``yes``
    **and** the LangGraph components are available.
    """
    toggle = os.getenv("USE_LANGGRAPH", "no").lower()
    return toggle == "yes" and HAS_LANGGRAPH

# ---------------------------------------------------------------------------
# Request / response models (identical to the original app)
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_state: dict | None = None

# ---------------------------------------------------------------------------
# /api/chat endpoint – now supports the toggle
# ---------------------------------------------------------------------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Basic validation – we need the Gemini LLM for both paths
    if not HAS_LANGCHAIN:
        raise HTTPException(status_code=503, detail="LangChain not available")

    # Initialise Gemini LLM (same as original)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7,
        max_retries=2,
    )

    # -------------------------------------------------------------------
    # Session handling (unchanged from the original implementation)
    # -------------------------------------------------------------------
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "user_info": {},
            "insurance_type": None,
            "quote_result": None,
            "knowledge_context": "",
            "next_action": "gather_info",
        }
    session = sessions[session_id]
    session["messages"].append(HumanMessage(content=request.message))

    # -------------------------------------------------------------------
    # 1️⃣  Toggle = YES → run through LangGraph (the "brain")
    # -------------------------------------------------------------------
    if use_langgraph():
        # Build the initial AgentState expected by the graph
        state = {
            "messages": session["messages"],
            "user_info": session["user_info"],
            "insurance_type": session["insurance_type"],
            "quote_result": session["quote_result"],
            "knowledge_context": session["knowledge_context"],
            "next_action": session["next_action"],
        }
        try:
            final_state = agent_graph.invoke(state)
            # The graph should return a dict with at least ``agent_response``
            response_text = final_state.get("agent_response", "[No response from graph]")
            # Update the session with whatever the graph produced
            session.update({
                "messages": final_state.get("messages", session["messages"]),
                "user_info": final_state.get("user_info", session["user_info"]),
                "insurance_type": final_state.get("insurance_type", session["insurance_type"]),
                "quote_result": final_state.get("quote_result", session["quote_result"]),
                "knowledge_context": final_state.get("knowledge_context", session["knowledge_context"]),
                "next_action": final_state.get("next_action", session["next_action"]),
            })
        except Exception as e:
            # If the graph crashes we fall back to the simple LLM path
            response_text = f"⚠️ LangGraph error: {e}. Falling back to direct LLM."
    else:
        # -------------------------------------------------------------------
        # 2️⃣  Toggle = NO → original simple LLM flow (with optional RAG)
        # -------------------------------------------------------------------
        system_instruction = """You are an expert insurance agent powered by AI. ..."""
        messages = [HumanMessage(content=system_instruction)] + session["messages"]
        # Optional RAG before the LLM call
        if HAS_RAG and any(kw in request.message.lower() for kw in ["what is", "explain", "tell me about", "how does", "difference"]):
            try:
                results = search_knowledge(request.message, k=2)
                if results:
                    context = "\n\n".join([doc.page_content for doc in results])
                    session["knowledge_context"] = context
                    messages.append(HumanMessage(content=f"**Relevant Knowledge Base Info:**\n{context}\n\nPlease use this information to answer the user's question accurately."))
            except Exception as rag_err:
                pass  # Silently ignore RAG failures
        # Call Gemini
        response = llm.invoke(messages)
        response_text = response.content

    # Store the assistant reply
    session["messages"].append(AIMessage(content=response_text))

    # Simple extraction of insurance type (same as original)
    lower_msg = request.message.lower()
    if "auto" in lower_msg or "car" in lower_msg or "vehicle" in lower_msg:
        session["insurance_type"] = "auto"
    elif "home" in lower_msg or "house" in lower_msg or "property" in lower_msg:
        session["insurance_type"] = "home"

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        agent_state={
            "insurance_type": session.get("insurance_type"),
            "has_quote": session.get("quote_result") is not None,
            "message_count": len(session["messages"]),
        },
    )

# ---------------------------------------------------------------------------
# Additional endpoints (reset, health, etc.) – copied from the original app
# ---------------------------------------------------------------------------
@app.post("/api/reset")
async def reset_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session reset successfully"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "llm": "gemini-1.5-flash",
        "orchestration": "langgraph" if HAS_LANGGRAPH else "direct",
        "sessions": len(sessions),
    }

# The file ends here – you can start the server with:
#   uvicorn main_backup:app --host 0.0.0.0 --port 8001
