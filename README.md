# 🤖 Agentic AI Insurance Agent

**A complete enterprise-grade Agentic AI application for insurance quote generation**

Built with: Google Gemini 1.5 Flash • LangChain • RAG • FastAPI • React

---

## 🚨 IMPORTANT: Python 3.12 Required

**This application requires Python 3.12** due to compatibility issues with Python 3.14.

### Quick Setup (5 minutes)

1. **Download Python 3.12**: https://www.python.org/downloads/release/python-3120/
2. **Run the setup script**:
   ```powershell
   cd backend
   .\setup_python312.ps1
   ```
3. **Start the application** (see below)

📖 **Detailed instructions**: See `QUICK_START_PYTHON312.md`

---

## 🚀 Quick Start

### Prerequisites
- ✅ Python 3.12 (download link above)
- ✅ Node.js 18+ (for frontend)
- ✅ Google Gemini API key (from https://aistudio.google.com/app/apikey)

### Backend Setup

```powershell
cd backend

# Option 1: Automated (recommended)
.\setup_python312.ps1

# Option 2: Manual
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend Setup

```powershell
cd frontend
npm install
```

### Environment Variables

Create `backend/.env`:
```
GEMINI_API_KEY=your_api_key_here
```

### Run the Application

```powershell
# Terminal 1: Backend
cd backend
.\venv\Scripts\python.exe main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open: **http://localhost:5173**

---

## 📚 Workshop Materials

This project includes **25 comprehensive guides** for teaching Agentic AI:

### Core Guides
- `FINAL_STATUS_REPORT.md` - Complete project overview
- `QUICK_START_PYTHON312.md` - Setup instructions
- `ARCHITECTURE_OVERVIEW.md` - System design
- `WORKSHOP_90MIN_GUIDE.md` - 90-minute workshop plan

### Teaching Materials
- `FACILITATOR_NOTES.md` - Instructor guide
- `VISUAL_LANGGRAPH_GUIDE.md` - Visual workflow design
- `PROMPT_ENGINEERING_GUIDE.md` - Prompt best practices
- `CONTEXT_VS_PROMPT_VS_RAG.md` - Key concepts explained
- `HUMAN_IN_THE_LOOP_GUIDE.md` - Interactive patterns

### Technical Guides
- `AI_STUDIO_GUIDE.md` - Google AI Studio tutorial
- `ORCHESTRATOR_QUICK_REFERENCE.md` - LangGraph reference
- `LANGGRAPH_VISUALIZATION_EXPLAINED.md` - Visualization guide
- `ITERATIVE_WORKFLOW_GUIDE.md` - Development workflow

### Research Materials
- `IEEE_PAPER_TEMPLATE.md` - Research paper template
- `WORKSHOP_QUESTIONNAIRES.md` - Data collection forms

### Troubleshooting
- `PYTHON_314_ISSUE.md` - Python compatibility issue
- `API_KEY_TROUBLESHOOTING.md` - API key problems

📁 **All guides located in**: `C:\Users\Naveen Nalajala\.gemini\antigravity\brain\8457259b-11c1-4422-9f04-0beafc242e4d\`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   React Frontend (localhost:5173)   │
│   • Chat Interface                  │
│   • Document Upload                 │
│   • Quote Display                   │
└─────────────────────────────────────┘
              ↓ HTTP
┌─────────────────────────────────────┐
│   FastAPI Backend (localhost:8000)  │
│   • /api/chat - Conversational AI   │
│   • /api/analyze-quote - Doc AI     │
│   • Session Management              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Google Gemini 1.5 Flash (FREE)    │
│   • Natural language understanding  │
│   • Quote generation                │
│   • Document analysis               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   RAG System (ChromaDB)             │
│   • Insurance knowledge base        │
│   • Semantic search                 │
│   • Context retrieval               │
└─────────────────────────────────────┘
```

---

## ✨ Features

### Agentic AI Capabilities
- ✅ **Autonomy**: Agent decides what questions to ask
- ✅ **Reasoning**: Multi-step decision making
- ✅ **Tool Use**: Calls functions autonomously
- ✅ **Memory**: Maintains conversation context
- ✅ **Planning**: Uses graph workflow
- ✅ **Learning**: Searches knowledge base

### Application Features
- 💬 Natural language conversation
- 📄 Document analysis (PDF, images)
- 💰 Auto & home insurance quotes
- 🧠 RAG-powered knowledge base
- 🔄 Session management
- ⚡ Real-time responses

---

## 🎓 For Workshop Participants

### What You'll Learn
1. Agentic AI principles and patterns
2. Google Gemini API integration
3. RAG (Retrieval Augmented Generation)
4. LangChain & LangGraph orchestration
5. Production-ready application architecture

### Prerequisites for Participants
- Python 3.12 installed
- Basic Python knowledge
- Google account (for API key)
- Code editor (VS Code recommended)

### Workshop Duration
90 minutes (hands-on coding included)

---

## 📊 Project Stats

- **Lines of Code**: ~2,500
- **Workshop Guides**: 25
- **Development Time**: ~6 hours
- **Setup Time**: 5-10 minutes
- **Target Audience**: 40 participants

---

## 🆘 Troubleshooting

### "No response from agent"
→ Check `PYTHON_314_ISSUE.md` - you need Python 3.12

### "API key not working"
→ Check `API_KEY_TROUBLESHOOTING.md`

### "Import errors"
→ Make sure virtual environment is activated and using Python 3.12

### "Frontend not loading"
→ Run `npm install` in frontend directory

---

## 📞 Support

- 📖 **Setup Guide**: `QUICK_START_PYTHON312.md`
- 🐛 **Python Issue**: `PYTHON_314_ISSUE.md`
- 🔑 **API Issues**: `API_KEY_TROUBLESHOOTING.md`
- 📊 **Full Status**: `FINAL_STATUS_REPORT.md`

---

## 🎯 Next Steps

1. ✅ Install Python 3.12
2. ✅ Run `setup_python312.ps1`
3. ✅ Add your Gemini API key to `.env`
4. ✅ Start backend and frontend
5. ✅ Open http://localhost:5173
6. 🎉 Your agent is ready!

---

## 📄 License

MIT License - Feel free to use for educational purposes

---

## 🙏 Acknowledgments

Built with:
- Google Gemini 1.5 Flash
- LangChain & LangGraph
- FastAPI
- React + Vite
- ChromaDB

---

**Ready for your workshop!** 🚀

For detailed setup instructions, see `QUICK_START_PYTHON312.md`
