"""
Advanced LangChain Context Window Demo with Real LLM Integration

This demonstrates:
- Actual token counting
- Processing documents that exceed context window
- Using LangChain's callback system to track tokens
- Error handling when context is too large

Note: Requires OPENAI_API_KEY environment variable to be set
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import tiktoken
import os


def count_tokens(text, model="gpt-3.5-turbo"):
    """Accurately count tokens using tiktoken"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception as e:
        # Fallback: rough estimate
        return int(len(text.split()) * 1.3)


def create_large_document():
    """Create a document that exceeds context window"""
    base_text = """
    The context window problem is one of the most significant challenges in working
    with Large Language Models (LLMs). A context window refers to the maximum number
    of tokens that a model can process in a single request. When you try to send more
    tokens than the model's context window allows, the request will fail or the model
    will truncate the input, potentially losing important information.
    
    Different models have different context window sizes:
    - GPT-3.5-turbo: 4,096 tokens
    - GPT-4: 8,192 tokens
    - GPT-4-turbo: 128,000 tokens
    - Claude-3: 200,000 tokens
    
    When working with large documents, you need strategies to handle this limitation:
    1. Text Splitting: Break documents into smaller chunks
    2. Summarization: Create summaries of chunks and process those
    3. Retrieval-Augmented Generation (RAG): Store chunks in a vector database
       and retrieve only relevant ones for each query
    4. Streaming: Process documents in streams rather than all at once
    
    LangChain provides excellent tools for handling these scenarios, including
    text splitters, document loaders, vector stores, and retrieval chains.
    """
    
    # Create a document that exceeds GPT-3.5's context window
    large_document = base_text * 200  # Repeat to create large document
    return large_document


def demonstrate_token_limits():
    """Show token limits and counting"""
    print("=" * 80)
    print("TOKEN LIMITS AND COUNTING")
    print("=" * 80)
    
    large_text = create_large_document()
    token_count = count_tokens(large_text)
    
    print(f"\nDocument Statistics:")
    print(f"  - Characters: {len(large_text):,}")
    print(f"  - Words: {len(large_text.split()):,}")
    print(f"  - Tokens (estimated): {token_count:,}")
    
    print(f"\nModel Context Window Limits:")
    models = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8192,
        "gpt-4-turbo": 128000,
        "claude-3-opus": 200000
    }
    
    for model, limit in models.items():
        fits = "✓ FITS" if token_count < limit else "✗ EXCEEDS"
        print(f"  - {model:20s}: {limit:>7,} tokens  {fits}")
    
    return large_text, token_count


def demonstrate_splitting_strategy():
    """Show how to split documents to fit context window"""
    print("\n" + "=" * 80)
    print("SPLITTING STRATEGY")
    print("=" * 80)
    
    large_text = create_large_document()
    
    # Calculate appropriate chunk size
    # Leave room for prompt and response (typically 1000-2000 tokens)
    max_context = 4096  # GPT-3.5 limit
    reserved_for_prompt = 500
    reserved_for_response = 500
    available_for_chunk = max_context - reserved_for_prompt - reserved_for_response
    
    # Roughly: 1 token ≈ 4 characters
    chunk_size_chars = available_for_chunk * 4
    
    print(f"\nChunk Size Calculation:")
    print(f"  - Max context window: {max_context:,} tokens")
    print(f"  - Reserved for prompt: {reserved_for_prompt:,} tokens")
    print(f"  - Reserved for response: {reserved_for_response:,} tokens")
    print(f"  - Available for chunk: {available_for_chunk:,} tokens")
    print(f"  - Recommended chunk size: ~{chunk_size_chars:,} characters")
    
    # Split the document
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size_chars,
        chunk_overlap=200,  # 200 chars overlap for context
        length_function=len
    )
    
    chunks = text_splitter.split_text(large_text)
    
    print(f"\nSplitting Results:")
    print(f"  - Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:5], 1):
        chunk_tokens = count_tokens(chunk)
        print(f"  - Chunk {i}: {len(chunk):,} chars, ~{chunk_tokens:,} tokens")
    
    return chunks


def demonstrate_processing_with_llm(api_key_set=False):
    """Demonstrate processing chunks with an LLM"""
    print("\n" + "=" * 80)
    print("PROCESSING WITH LLM")
    print("=" * 80)
    
    if not api_key_set:
        print("\n⚠️  Note: OPENAI_API_KEY not set. Showing example code only.")
        print("\nExample: Processing each chunk and summarizing:")
        print("""
        from langchain.llms import OpenAI
        from langchain.callbacks import get_openai_callback
        
        llm = OpenAI(temperature=0)
        chunks = split_document(large_text)
        
        summaries = []
        total_tokens = 0
        
        for i, chunk in enumerate(chunks):
            prompt = f"Summarize the following text:\\n\\n{chunk}"
            
            with get_openai_callback() as cb:
                summary = llm(prompt)
                total_tokens += cb.total_tokens
            
            summaries.append(summary)
            print(f"Chunk {i+1} processed: {cb.total_tokens} tokens")
        
        print(f"Total tokens used: {total_tokens}")
        """)
        return
    
    # If API key is set, demonstrate actual processing
    try:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        
        large_text = create_large_document()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(large_text)
        
        print(f"\nProcessing {len(chunks)} chunks...")
        
        total_tokens = 0
        summaries = []
        
        for i, chunk in enumerate(chunks[:3], 1):  # Process first 3 chunks as example
            prompt = f"Provide a brief summary (2-3 sentences) of the following text:\n\n{chunk}"
            
            with get_openai_callback() as cb:
                response = llm.predict(prompt)
                total_tokens += cb.total_tokens
            
            summaries.append(response)
            print(f"\nChunk {i}:")
            print(f"  - Tokens used: {cb.total_tokens}")
            print(f"  - Summary: {response[:200]}...")
        
        print(f"\nTotal tokens used for {len(chunks)} chunks: {total_tokens:,}")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure OPENAI_API_KEY is set correctly")


def demonstrate_rag_workflow():
    """Show RAG workflow for handling large documents"""
    print("\n" + "=" * 80)
    print("RAG WORKFLOW EXAMPLE")
    print("=" * 80)
    
    print("""
    Retrieval-Augmented Generation (RAG) Workflow:
    
    1. Document Loading & Splitting:
       ```python
       from langchain.document_loaders import TextLoader
       from langchain.text_splitter import RecursiveCharacterTextSplitter
       
       loader = TextLoader("large_document.txt")
       documents = loader.load()
       text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
       chunks = text_splitter.split_documents(documents)
       ```
    
    2. Create Embeddings & Vector Store:
       ```python
       from langchain.embeddings import OpenAIEmbeddings
       from langchain.vectorstores import FAISS
       
       embeddings = OpenAIEmbeddings()
       vectorstore = FAISS.from_documents(chunks, embeddings)
       ```
    
    3. Create Retrieval Chain:
       ```python
       from langchain.chains import RetrievalQA
       
       qa_chain = RetrievalQA.from_chain_type(
           llm=ChatOpenAI(),
           chain_type="stuff",
           retriever=vectorstore.as_retriever()
       )
       ```
    
    4. Query (only relevant chunks retrieved):
       ```python
       result = qa_chain.run("What is the context window problem?")
       ```
    
    Benefits:
    - Only relevant chunks are sent to LLM
    - Stays within context window
    - More efficient and accurate
    """)


def main():
    """Main demonstration"""
    print("\n" + "=" * 80)
    print("ADVANCED LANGCHAIN CONTEXT WINDOW DEMONSTRATION")
    print("=" * 80)
    
    # Check if API key is set
    api_key_set = bool(os.getenv("OPENAI_API_KEY"))
    if api_key_set:
        print("\n✓ OPENAI_API_KEY detected")
    else:
        print("\n⚠️  OPENAI_API_KEY not set - running in demo mode")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
    
    # Run demonstrations
    large_text, token_count = demonstrate_token_limits()
    chunks = demonstrate_splitting_strategy()
    demonstrate_processing_with_llm(api_key_set)
    demonstrate_rag_workflow()
    
    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print("""
    1. Always check token counts before sending to LLM
    2. Use text splitters to break large documents
    3. Monitor token usage with callbacks
    4. Consider RAG for large knowledge bases
    5. Leave room in context window for prompt and response
    6. Use chunk overlap to maintain context between chunks
    """)
    print("=" * 80)


if __name__ == "__main__":
    main()

