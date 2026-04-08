from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    # Accept **kwargs to catch any "ghost" arguments from LangChain
    def __init__(self, **kwargs): 
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")

    def get_llm(self):
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env")
            
        return ChatGroq(
            groq_api_key=self.api_key, 
            model_name="llama-3.3-70b-versatile"
        )