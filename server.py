from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

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

# Mount static files (Vite build output)
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    print("Warning: frontend/dist not found. Run 'npm run build' in frontend directory.")

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
    # Mock processing if no key provided, to be safe for demo
    if not request.api_key and not os.getenv("OPENAI_API_KEY"):
         return {"summary": "Mock Summary: This is a placeholder summary. Set API Key to get real results.", "tokens_used": 0}
         
    # Real processing logic would go here (omitted for safety/speed in initial setup, can add if requested)
    return {"summary": "Mock Summary: Real LLM processing requires configured environment.", "tokens_used": 0}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
