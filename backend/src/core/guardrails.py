"""
guardrails.py
-------------
Implements the "Brand Score" logic.
Uses a secondary LLM call to grade generated content against Vaisala guidelines.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.config import settings

# Define the structure for the grading output
class BrandScoreResult(BaseModel):
    score: int = Field(description="Score from 0 to 100")
    reasoning: str = Field(description="Brief explanation of the score")

# The Judge's Prompt
GRADING_TEMPLATE = """
You are the Vaisala Brand Compliance Officer. 
Evaluate the following text against these rules:
1. Scientific Precision: No vague claims.
2. Tone: Professional, inspiring, grounded in data.
3. Terminology: Uses standard industrial/scientific terms.

TEXT TO EVALUATE:
"{text}"

Provide a score (0-100) and a brief reasoning.
Return strictly JSON.
"""

class BrandGuard:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0, # Deterministic grading
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.parser = JsonOutputParser(pydantic_object=BrandScoreResult)
        self.prompt = ChatPromptTemplate.from_template(GRADING_TEMPLATE)

    def evaluate(self, text: str) -> BrandScoreResult:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"text": text})

brand_guard = BrandGuard()