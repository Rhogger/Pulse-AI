from crewai import LLM


def get_phi3_llm():
    return LLM(
        model="ollama/phi3:latest",
        max_tokens=100000,
        verbose=True
    )
