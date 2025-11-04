from pathlib import Path

BIB_FILE = Path("bibliography.log")
LOCAL_SOURCES_DIR = Path("./sources")

def bibliography_tracker(**kwargs):
    """
    Callback function to track references and write them to a bibliography file
    
    Args: Argument reference
        
    Returns: None
    """
    # Track assistant tool usage messages
    if "message" in kwargs:
        message = kwargs["message"]
        # Messages can contain multiple content blocks
        for block in message.get("content", []):
            tool_use = block.get("toolUse")
            # Track webpages read
            if tool_use and tool_use.get("name") == "http_request":
                url = tool_use.get("input", {}).get("url")
                if url:
                    # Append URL to the bibliography
                    with BIB_FILE.open("a") as f:
                        f.write(f"URL: {url}\n")
            # Track local files if mentioned in the LLM output
            text = block.get("text", "")
            for file in LOCAL_SOURCES_DIR.glob("*.txt"):
                if file.name in text:
                    with BIB_FILE.open("a") as f:
                        # Append file name to bibliography
                        f.write(f"File: {file.name}\n")
