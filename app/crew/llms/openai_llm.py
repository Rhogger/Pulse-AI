import os
from crewai import LLM
from dotenv import load_dotenv


def get_openai_llm():
    load_dotenv()

    return LLM(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        verbose=True
    )
