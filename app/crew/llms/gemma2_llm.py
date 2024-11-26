from crewai import LLM


def get_gemma2_llm():
    return LLM(
        model="ollama/gemma2:2b",
        temperature=0.1,
        max_tokens=1000,
        verbose=True
    )
