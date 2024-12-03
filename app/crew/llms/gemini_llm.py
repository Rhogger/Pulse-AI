import os
from crewai import LLM
from dotenv import load_dotenv


def get_gemini_llm():
    load_dotenv()

    return LLM(
        model="gemini/gemini-1.5-flash",
        api_key=os.environ["GEMINI_API_KEY"],
        verbose=True
    )
