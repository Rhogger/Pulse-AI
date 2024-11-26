from crewai import LLM


def get_llama2_llm():
    return LLM(
        model="ollama/llama3.2:latest",
        temperature=0.1,
        max_tokens=1000,
        verbose=True
    )
