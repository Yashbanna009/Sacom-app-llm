from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles

from backend.services.content_service import ContentService
from backend.services.llm_service import LLMService
from backend.config import settings

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# --- Application Setup ---
app = FastAPI(
    title="SACOM II2 - LLM Wrapper Application",
    description="A modular application for interacting with an AI based on a specific knowledge domain."
)

# --- CORS Middleware ---
# This allows our frontend (running on a different port) to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Service Instantiation ---
# Create single instances of our services to be used across the application
content_service = ContentService()
llm_service = LLMService()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- API Request/Response Models ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# --- API Endpoints ---
@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("5/minute")  # 5 requests per minute per IP
async def chat_handler(request: Request, chat: ChatRequest):
    """
    Main chat endpoint. It orchestrates getting context and calling the LLM.
    """
    try:
        # 1. Get the domain-specific context from the Content Service
        context = content_service.get_context()
        
        # 2. Construct the system prompt using the context
        system_prompt = (
            f"You are a wise and empathetic AI assistant specializing in {settings.ACTIVE_DOMAIN}. "
            f"Your goal is to provide guidance, interpretations, and support based on the following teachings. "
            f"You can also engage in therapeutic-style dialogue. "
            f"Here is your core knowledge for this conversation:\n---CONTEXT---\n{context}\n---END CONTEXT---"
        )
        
        # 3. Get the AI's response from the LLM Service
        ai_reply = llm_service.get_response(system_prompt=system_prompt, user_message=chat.message)
        
        return ChatResponse(reply=ai_reply)
    except Exception as e:
        print(f"Error in chat handler: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/")
def root():
    return {"message": f"LLM Wrapper API is running. Active domain: {settings.ACTIVE_DOMAIN}"}

# To run the app: `uvicorn backend.main:app --reload` 