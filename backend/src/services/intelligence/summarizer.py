from backend.src.services.intelligence.llm_client import LLMClient


def summarize_content(content: str) -> str:
    llm = LLMClient()
    prompt = f"Summarize the following news article content:\n{content}\nSummary:"  
    summary = llm.generate_summary(prompt)
    return summary
