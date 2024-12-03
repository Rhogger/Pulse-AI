import os
from crewai import LLM
from dotenv import load_dotenv


def get_mistral_llm():
    load_dotenv()

    return LLM(
        model="mistral/open-mistral-7b",
        api_key=os.environ["MISTRAL_API_KEY"]
    )
