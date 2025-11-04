from pathlib import Path
from strands import Agent

LOCAL_SOURCES_DIR = Path("./sources")

def can_use_local_sources():
    """
    Retrieves user consent to read local files in 'sources' directory
    
    Args: None
        
    Returns:
        bool: Yes/no of user consent to read files
    """
    while True:
        choice = input(f"Include local sources from'{LOCAL_SOURCES_DIR}' directory? (y/n): ").strip().lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def gather_local_summaries(max_chunk_size=2000):
    """
    Summarize local files with LLM before passing them to the workflow
    
    Args: None
        
    Returns:
        str: Local file summaries
    """
    summaries = []
    summarization_agent = Agent(
        system_prompt="You are a summarization agent. Summarize the input concisely.",
        callback_handler = None
    )
    for file in LOCAL_SOURCES_DIR.glob("*.txt"):
        content = file.read_text(encoding="utf-8")
        
        # Chunk large files
        chunks = [content[i:i+max_chunk_size] for i in range(0, len(content), max_chunk_size)]
        file_summary = []

        for chunk in chunks:
            prompt = (
                f"Summarize the following content in under 200 words, "
                f"highlighting key points relevant to potential research queries:\n\n{chunk}"
            )
            chunk_summary = summarization_agent(prompt)
            file_summary.append(str(chunk_summary))
        
        # Combine chunk summaries for the file
        combined_summary = "\n".join(file_summary)
        summaries.append(f"{file.name}: {combined_summary}")

    return "\n".join(summaries)
