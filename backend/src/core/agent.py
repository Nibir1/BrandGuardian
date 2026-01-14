"""
agent.py
--------
The Core Logic Module.
Orchestrates the RAG flow: Retrieval -> Prompt Augmentation -> Generation.
"""

from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from src.config import settings
from src.core.retrieval import get_brand_retriever
from src.models.schemas import BrandRequest, BrandResponse

# Define the System Prompt
# This enforces the "Vaisala" persona and instructs on how to use the examples.
SYSTEM_TEMPLATE = """
You are BrandGuardian, the AI Brand Assistant for Vaisala.
Vaisala is a global leader in weather, environmental, and industrial measurements.
Your voice is:
1. Scientific & Precise (No fluff, no hyperbole)
2. Inspiring but Grounded (We enable a sustainable planet through data)
3. Professional (B2B audience: engineers, scientists, decision-makers)

TASK:
Write {content_type} content about: "{topic}"

STYLE INSTRUCTIONS:
- Tone Modifier: {tone_modifier}
- Use the provided "Context Examples" below to mimic Vaisala's vocabulary and sentence structure.
- Do NOT explicitly mention "Based on the examples". Just write in that style.

CONTEXT EXAMPLES (Approved Vaisala Copy):
{context}

OUTPUT:
Return only the generated content.
"""

class BrandAgent:
    """
    The main orchestrator class for text generation.
    """
    
    def __init__(self):
        # Initialize LLM
        # We use temperature=0.7 for a balance of creativity and strict adherence
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo", # Or "gpt-4-turbo" for higher quality
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize Retriever
        self.retriever = get_brand_retriever(k=3)
        
        # Setup Chain
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_TEMPLATE)
        self.parser = StrOutputParser()
        # chain = prompt | llm | parser (We construct this dynamically below)

    def _format_docs(self, docs: List[Document]) -> str:
        """Helper to combine retrieved docs into a single string."""
        return "\n\n".join([f"---\n{doc.page_content}\n---" for doc in docs])

    def generate(self, request: BrandRequest) -> Dict[str, Any]:
        """
        Executes the RAG pipeline.
        
        1. Retrieve similar approved copy.
        2. Construct prompt with Few-Shot examples.
        3. Generate text.
        4. Return result + metadata.
        """
        print(f"🔎 Agent finding context for: {request.topic}")
        
        # 1. Retrieval
        # We query the vector DB using the user's topic
        retrieved_docs = self.retriever.invoke(request.topic)
        formatted_context = self._format_docs(retrieved_docs)
        
        print(f"✅ Found {len(retrieved_docs)} reference examples.")

        # 2. Generation
        chain = self.prompt | self.llm | self.parser
        
        generated_text = chain.invoke({
            "content_type": request.content_type,
            "topic": request.topic,
            "tone_modifier": request.tone_modifier or "Professional",
            "context": formatted_context
        })

        # 3. Structure Output
        # Extract snippets for the "Used References" field
        references = [doc.page_content[:100] + "..." for doc in retrieved_docs]

        return {
            "content": generated_text,
            "used_references": references
        }

# Singleton instance for import
brand_agent = BrandAgent()