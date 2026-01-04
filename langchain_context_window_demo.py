# Author: Naveen Chintala
"""
LangChain Context Window Problem Demonstration

This program showcases:
1. The context window limitation in LLMs
2. How to handle documents that exceed the context window
3. Using LangChain's text splitters and document loaders
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.schema import Document
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

# Note: This is a demonstration. In production, use environment variables for API keys
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"


def create_large_document():
    """Create a large document that exceeds typical context windows"""
    # Simulating a large document by repeating content
    base_text = """
    Artificial Intelligence (AI) has revolutionized the way we interact with technology.
    Machine learning algorithms can now process vast amounts of data and make predictions
    with remarkable accuracy. Natural Language Processing (NLP) enables computers to
    understand and generate human language. Deep learning neural networks have achieved
    breakthroughs in image recognition, speech synthesis, and autonomous systems.
    
    The transformer architecture, introduced in 2017, has become the foundation for
    modern language models. These models use attention mechanisms to understand context
    and relationships between words. Large Language Models (LLMs) like GPT, BERT, and
    their successors have demonstrated remarkable capabilities in text generation,
    translation, summarization, and question answering.
    
    However, these models face a critical limitation: the context window. A context
    window is the maximum number of tokens (words or subwords) that a model can process
    in a single interaction. When a document exceeds this limit, the model cannot
    process the entire document at once, requiring strategies like chunking, summarization,
    or retrieval-augmented generation (RAG).
    """
    
    # Create a document that's too long for most context windows
    large_document = base_text * 50  # Repeat 50 times to create a large document
    return large_document


def demonstrate_context_window_problem():
    """Demonstrate the context window limitation"""
    print("=" * 80)
    print("CONTEXT WINDOW PROBLEM DEMONSTRATION")
    print("=" * 80)
    
    # Create a large document
    large_text = create_large_document()
    document = Document(page_content=large_text)
    
    print(f"\n1. Document Statistics:")
    print(f"   - Character count: {len(large_text):,}")
    print(f"   - Approximate word count: {len(large_text.split()):,}")
    print(f"   - Approximate token count (rough estimate): ~{len(large_text.split()) * 1.3:.0f}")
    print(f"   - Typical GPT-3.5 context window: 4,096 tokens")
    print(f"   - Typical GPT-4 context window: 8,192 tokens (or 32,768 for extended)")
    
    # Check if document exceeds context window
    estimated_tokens = len(large_text.split()) * 1.3
    if estimated_tokens > 4096:
        print(f"\n   ⚠️  PROBLEM: Document exceeds typical context window!")
        print(f"   The document is too large to process in a single API call.")
    else:
        print(f"\n   ✓ Document fits within context window")
    
    return document


def demonstrate_text_splitting():
    """Demonstrate how to split large documents using LangChain"""
    print("\n" + "=" * 80)
    print("SOLUTION: TEXT SPLITTING WITH LANGCHAIN")
    print("=" * 80)
    
    large_text = create_large_document()
    
    # Method 1: Recursive Character Text Splitter (Recommended)
    print("\n2. Using RecursiveCharacterTextSplitter:")
    print("   - Splits text recursively by characters")
    print("   - Tries to keep paragraphs, sentences, and words together")
    print("   - Best for preserving semantic meaning")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Target chunk size in characters
        chunk_overlap=200,  # Overlap between chunks to maintain context
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # Priority order for splitting
    )
    
    chunks = text_splitter.split_text(large_text)
    print(f"\n   - Original document split into {len(chunks)} chunks")
    print(f"   - Average chunk size: {sum(len(c) for c in chunks) / len(chunks):.0f} characters")
    print(f"   - First chunk preview: {chunks[0][:100]}...")
    
    # Method 2: Character Text Splitter (Simple)
    print("\n3. Using CharacterTextSplitter (Simple):")
    char_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        separator=" "
    )
    char_chunks = char_splitter.split_text(large_text)
    print(f"   - Split into {len(char_chunks)} chunks")
    print(f"   - Simpler but may break words/sentences")
    
    return chunks


def demonstrate_document_processing():
    """Demonstrate processing documents with LangChain"""
    print("\n" + "=" * 80)
    print("PROCESSING SPLIT DOCUMENTS")
    print("=" * 80)
    
    large_text = create_large_document()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Split into documents
    documents = text_splitter.create_documents([large_text])
    
    print(f"\n4. Document Processing Strategy:")
    print(f"   - Split document into {len(documents)} manageable chunks")
    print(f"   - Each chunk can be processed independently")
    print(f"   - Results can be combined or summarized")
    
    print(f"\n   Example chunks:")
    for i, doc in enumerate(documents[:3], 1):
        print(f"\n   Chunk {i} (length: {len(doc.page_content)} chars):")
        print(f"   {doc.page_content[:150]}...")
    
    return documents


def demonstrate_rag_approach():
    """Demonstrate Retrieval-Augmented Generation approach"""
    print("\n" + "=" * 80)
    print("ADVANCED SOLUTION: RETRIEVAL-AUGMENTED GENERATION (RAG)")
    print("=" * 80)
    
    print("\n5. RAG Approach:")
    print("   - Split documents into chunks")
    print("   - Create embeddings for each chunk")
    print("   - Store in a vector database")
    print("   - When querying:")
    print("     a. Convert query to embedding")
    print("     b. Find most relevant chunks (semantic search)")
    print("     c. Use only relevant chunks as context")
    print("     d. Generate response with limited, relevant context")
    print("\n   Benefits:")
    print("   - Only uses relevant parts of large documents")
    print("   - Stays within context window limits")
    print("   - More efficient and cost-effective")
    print("   - Better accuracy for specific queries")


def demonstrate_token_counting():
    """Show how to estimate token counts"""
    print("\n" + "=" * 80)
    print("TOKEN COUNTING")
    print("=" * 80)
    
    print("\n6. Token Counting Methods:")
    print("   - Rough estimate: ~1.3 tokens per word")
    print("   - Use tiktoken library for accurate counting:")
    print("     ```python")
    print("     import tiktoken")
    print("     encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')")
    print("     tokens = encoding.encode(text)")
    print("     print(f'Token count: {len(tokens)}')")
    print("     ```")
    print("   - LangChain's token counting utilities:")
    print("     ```python")
    print("     from langchain.callbacks import get_openai_callback")
    print("     with get_openai_callback() as cb:")
    print("         result = llm(text)")
    print("         print(f'Tokens used: {cb.total_tokens}')")
    print("     ```")


def main():
    """Main function to run all demonstrations"""
    print("\n" + "=" * 80)
    print("LANGCHAIN CONTEXT WINDOW DEMONSTRATION")
    print("=" * 80)
    print("\nThis program demonstrates:")
    print("1. The context window limitation problem")
    print("2. How to split large documents")
    print("3. Strategies for handling large documents")
    print("4. Token counting methods")
    
    # Run demonstrations
    document = demonstrate_context_window_problem()
    chunks = demonstrate_text_splitting()
    documents = demonstrate_document_processing()
    demonstrate_rag_approach()
    demonstrate_token_counting()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("1. LLMs have limited context windows (typically 4K-32K tokens)")
    print("2. Large documents must be split into smaller chunks")
    print("3. LangChain provides text splitters for this purpose")
    print("4. RAG is an advanced approach for handling large knowledge bases")
    print("5. Always monitor token usage to stay within limits")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

