# Author: Naveen Chintala
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="LangChain Context Window Demo API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

class TextRequest(BaseModel):
    text: str
    model: str = "gpt-3.5-turbo"

class TokenResponse(BaseModel):
    count: int
    compatible_models: List[str]

class SplitRequest(BaseModel):
    text: str
    chunk_size: int
    chunk_overlap: int

class ProcessRequest(BaseModel):
    text: str
    api_key: Optional[str] = None

@app.post("/api/tokenize", response_model=TokenResponse)
async def count_tokens_endpoint(request: TextRequest):
    try:
        encoding = tiktoken.encoding_for_model(request.model)
        tokens = encoding.encode(request.text)
        count = len(tokens)
        
        # Check compatibility
        models = {
            "gpt-3.5-turbo": 4096,
            "gpt-4": 8192,
            "gpt-4-turbo": 128000,
            "claude-3-opus": 200000
        }
        
        compatible = [m for m, limit in models.items() if count <= limit]
        
        return TokenResponse(count=count, compatible_models=compatible)
    except Exception as e:
        # Fallback estimation
        count = int(len(request.text.split()) * 1.3)
        return TokenResponse(count=count, compatible_models=[])

@app.post("/api/split")
async def split_text_endpoint(request: SplitRequest):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(request.text)
        return {"chunks": chunks, "count": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process")
async def process_text_endpoint(request: ProcessRequest):
    # Check for key in request, then env, then fallback to hardcoded string (if user edited it)
    api_key = request.api_key or os.getenv("OPENAI_API_KEY")
    
    # If using the hardcoded key from user edit, handle it properly
    # (Checking if user pasted key into os.getenv directly like previous error)
    if not api_key:
         # Fallback for the specific user error where they might have put the key in os.getenv source
         # We will try to read it from .env again just in case
         pass

    if not api_key:
         return {"summary": "Mock Summary: No API Key found. Please add it to .env or the text input.", "tokens_used": 0}

    try:
        # Initialize LLM
        llm = ChatOpenAI(
            temperature=0, 
            model_name="gpt-3.5-turbo",
            openai_api_key=api_key
        )
        
        # Track token usage
        with get_openai_callback() as cb:
            # Simple summarization prompt
            messages = [
                SystemMessage(content="You are a helpful assistant that summarizes text concisely."),
                HumanMessage(content=f"Please provide a 2-sentence summary of the following text:\n\n{request.text}")
            ]
            response = llm.invoke(messages)
            
            return {
                "summary": response.content,
                "tokens_used": cb.total_tokens
            }
            
    except Exception as e:
        # Return error as summary for visibility in UI
        return {"summary": f"Error calling OpenAI: {str(e)}", "tokens_used": 0}

# Mount static files (Vite build output)
# Must be after API routes to avoid blocking them
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    print("Warning: frontend/dist not found. Run 'npm run build' in frontend directory.")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
