# main_with_toggle.py – backup FastAPI entry point with LangChain & LangGraph toggle
#
# This file demonstrates how to route the `/api/chat` endpoint either through the
# simple Gemini LLM call (LangChain) **or** through the LangGraph workflow (the
# "brain") based on an environment variable ``USE_LANGGRAPH`` set to ``yes`` or
# ``no``.
#
# Usage examples:
#   $env:USE_LANGGRAPH="yes"   # route through LangGraph
#   $env:USE_LANGGRAPH="no"    # use direct LLM (default)
#   uvicorn main_with_toggle:app --host 0.0.0.0 --port 8001

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, uuid

# ------------------------------------------------------------
# Optional imports – may be missing in some environments
# ------------------------------------------------------------
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, AIMessage
    HAS_LANGCHAIN = True
except Exception:
    HAS_LANGCHAIN = False

try:
    from langgraph_agent import agent_graph  # LangGraph workflow
    HAS_LANGGRAPH = True
except Exception:
    HAS_LANGGRAPH = False

try:
    from rag_system import search_knowledge
    HAS_RAG = True
except Exception:
    HAS_RAG = False

# Load .env (including GEMINI_API_KEY and optional USE_LANGGRAPH)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Insurance Agent – Toggle Demo",
    description="FastAPI backend that can switch between a direct LLM call and the LangGraph brain.",
    version="2.0",
)

# CORS – same as original app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In‑memory session store (mirrors original structure)
sessions = {}

# ------------------------------------------------------------
# Helper – decide whether to use LangGraph for this request
# ------------------------------------------------------------
def use_langgraph() -> bool:
    return os.getenv("USE_LANGGRAPH", "no").lower() == "yes" and HAS_LANGGRAPH

# ------------------------------------------------------------
# Request / response models (identical to original)
# ------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_state: dict | None = None

# ------------------------------------------------------------
# /api/chat endpoint with toggle logic
# ------------------------------------------------------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Basic component checks
    if not HAS_LANGCHAIN:
        return ChatResponse(
            response="Sorry, the AI system is not properly configured. Please contact support.",
            session_id=str(uuid.uuid4()),
        )
    # Initialise Gemini LLM (used for both paths)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7,
        max_retries=2,
    )
    if not llm:
        return ChatResponse(
            response="Sorry, the AI model is not available. Please ensure GEMINI_API_KEY is set.",
            session_id=str(uuid.uuid4()),
        )

    # Session handling (unchanged)
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

    # --------------------------------------------------------
    # Path 1 – LangGraph (if toggle enabled)
    # --------------------------------------------------------
    if use_langgraph():
        # Build the AgentState expected by the graph
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
            response_text = final_state.get("agent_response", "[No response from LangGraph]")
            # Update session with any changes the graph made
            session.update({
                "messages": final_state.get("messages", session["messages"]),
                "user_info": final_state.get("user_info", session["user_info"]),
                "insurance_type": final_state.get("insurance_type", session["insurance_type"]),
                "quote_result": final_state.get("quote_result", session["quote_result"]),
                "knowledge_context": final_state.get("knowledge_context", session["knowledge_context"]),
                "next_action": final_state.get("next_action", session["next_action"]),
            })
        except Exception as e:
            # If the graph fails, fall back to the simple LLM path
            response_text = f"⚠️ LangGraph error: {e}. Falling back to direct LLM."
            # Continue to the LLM block below
            use_graph = False
        else:
            # Successfully used LangGraph – skip the LLM block
            use_graph = True
    else:
        use_graph = False

    # --------------------------------------------------------
    # Path 2 – Direct LLM (original flow) – also used on fallback
    # --------------------------------------------------------
    if not use_graph:
        # System prompt (same as original implementation)
        system_instruction = """You are an expert insurance agent powered by AI. Your role is to:\n\n1. **Understand Customer Needs**: Determine if they need auto or home insurance\n2. **Gather Information**: Ask relevant questions to collect necessary details\n3. **Use Your Knowledge**: Search your knowledge base when users ask questions\n4. **Calculate Quotes**: When you have enough info, calculate accurate premiums\n5. **Explain Clearly**: Break down how premiums are calculated and why\n\nFor AUTO insurance, you need:\n- Age, vehicle year/make/model, years licensed, accidents, violations\n\nFor HOME insurance, you need:\n- Year built, square footage, construction type, dwelling coverage\n\n**CRITICAL GUIDELINES:**\n- **STRICTLY LIMIT** your responses to insurance topics.\n- If asked about other topics (sports, coding, poetry, general knowledge, etc.), politely refuse: \"I can only assist with insurance-related inquiries.\"\n- Be conversational and friendly\n- Ask 1-2 questions at a time (don't overwhelm)\n- When users ask \"what is\" or \"explain\" questions, use your knowledge base.\n- When you have enough info, calculate the quote.\n- Explain the breakdown clearly.\n- Suggest ways to save money if appropriate.\n\nBe transparent about your reasoning and help them make informed decisions."""
        messages = [HumanMessage(content=system_instruction)] + session["messages"]
        # Optional RAG before LLM call
        msg_lower = request.message.lower()
        rag_keywords = ["what is", "explain", "tell me about", "how does", "difference"]
        if HAS_RAG and any(k in msg_lower for k in rag_keywords):
            try:
                filter_type = None
                if "auto" in msg_lower or "car" in msg_lower or "vehicle" in msg_lower:
                    filter_type = "auto"
                elif "home" in msg_lower or "house" in msg_lower or "property" in msg_lower:
                    filter_type = "home"
                results = search_knowledge(request.message, k=2, filter_type=filter_type)
                if results:
                    context = "\n\n".join([doc.page_content for doc in results])
                    session["knowledge_context"] = context
                    messages.append(HumanMessage(content=f"**Relevant Knowledge Base Info:**\n{context}\n\nPlease use this information to answer the user's question accurately."))
            except Exception:
                pass  # ignore RAG failures
        # Call Gemini
        response = llm.invoke(messages)
        response_text = response.content

    # Store assistant reply
    session["messages"].append(AIMessage(content=response_text))
    # Simple insurance‑type extraction (same as original)
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

# ------------------------------------------------------------
# Additional utility endpoints (reset, health, etc.)
# ------------------------------------------------------------
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

# End of file – run with: uvicorn main_with_toggle:app --host 0.0.0.0 --port 8001
