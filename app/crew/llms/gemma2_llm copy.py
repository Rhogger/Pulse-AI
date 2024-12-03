from crewai import LLM


def get_gemma2_llm():
    return LLM(
        model="ollama/gemma2:latest",
        max_tokens=100000,
    )
