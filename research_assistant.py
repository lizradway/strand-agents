#!/usr/bin/env python3
"""
# Agentic Workflow: Research Assistant

This agentic workflow uses Strands agents with web and local file research capabilities.

## Key Features
- Specialized agent roles working in sequence
- Direct passing of information between workflow stages
- Web research using http_request tool
- Local file research using RAG
- Fact-checking and information synthesis

## How to Run
1. Navigate to the example directory
2. Run: python research_assistant.py
3. Enter queries or claims at the prompt

## Example Queries
- "Thomas Edison invented the light bulb"
- "Tuesday comes before Monday in the week"

## Workflow Process
1. Web Researcher Agent: Gathers web information using HTTP
2. Local Research Agent: Gathers local file information using RAG
3. Analyst Agent: Verifies facts and synthesizes findings
3. Writer Agent: Creates final report
"""
import json
from pathlib import Path
from strands import Agent
from strands_tools import http_request

BIB_FILE = Path("bibliography.log") # Bibliography output file
LOCAL_SOURCES_DIR = Path("./sources") # Local sources input file

def run_research_workflow(user_input):
    """
    Run a four-agent workflow for research and fact-checking with web and file sources.
    Shows progress logs during execution but presents only the final report to the user.
    
    Args:
        user_input: Research query or claim to verify
        
    Returns:
        str: The final report from the Writer Agent
    """
    
    print(f"\nProcessing: '{user_input}'")
    
    # Step 1: Researcher Agent with enhanced web capabilities
    print("\nStep 1: Researcher Agent gathering web information...")
    
    researcher_agent = Agent(
        system_prompt=(
            "You are a Researcher Agent that gathers information from the web. "
            "1. Determine if the input is a research query or factual claim "
            "2. Use your research tools (http_request) to find relevant information "
            "3. Include source URLs and keep findings under 500 words"
        ),
        callback_handler=bibliography_tracker,
        tools=[http_request]
    )
    
    researcher_response = researcher_agent(
        f"Research: '{user_input}'. Use your available tools to gather information from reliable sources. "
        f"Focus on being concise and thorough, but limit web requests to 1-2 sources.",
    )
    
    # Extract only the relevant content from the researcher response
    web_research_findings = str(researcher_response)
    
    print("Web research complete")

    # Step 2: Researcher Agent with local file search RAG capabilities
    print("\nStep 2: Researcher Agent with local file search...")

    # Obtain user content to access local sources
    use_local = can_use_local_sources()
    local_summaries = ""
    local_research_findings = ""
    if use_local:
        print("Gathering local source summaries...")
        local_summaries = gather_local_summaries()
    else:
        print("Skipping Step 2 Researcher Agent with local file search...")

    # Runs Step 2 only if local sources exist
    if local_summaries:
        researcher_agent = Agent(
            system_prompt=(
                "You are a Researcher Agent that gathers information from local sources."
                "1. Determine if the input is a research query or factual claim "
                "2. Use the local sources below to find relevant information"
                "3. Include source file paths in output and keep findings under 500 words"),
            callback_handler=bibliography_tracker
        )

        # Ask LLM to research query
        researcher_response = researcher_agent(
            f"Research: '{user_input}'. Use local file summaries to gather information from reliable source files. "
            "Focus on being concise and thorough, but limit file reads to 1-2 sources."
        )

        # Extract only the relevant content from the researcher response
        local_research_findings = str(researcher_response)
        print("\nLocal research complete.\n")

    print("Passing research findings to Analyst Agent...\n")
    
    # Step 3: Analyst Agent to verify facts
    print("Step 3: Analyst Agent analyzing findings...")
    
    analyst_agent = Agent(
        system_prompt=(
            "You are an Analyst Agent that verifies information. "
            "1. For factual claims: Rate accuracy from 1-5 and correct if needed "
            "2. For research queries: Identify 3-5 key insights "
            "3. Evaluate source reliability and keep analysis under 400 words"
        ),
        callback_handler=None
    )

    # Analyze findings from web and local source
    analyst_response = analyst_agent(
        f"Analyze these findings about '{user_input}':\n\n {web_research_findings}\n\n {local_research_findings}",
    )
    
    # Extract only the relevant content from the analyst response
    analysis = str(analyst_response)
    
    print("Analysis complete")
    print("Passing analysis to Writer Agent...\n")
    
    # Step 4: Writer Agent to create report
    print("Step 4: Writer Agent creating final report...")
    
    writer_agent = Agent(
        system_prompt=(
            "You are a Writer Agent that creates clear reports. "
            "1. For fact-checks: State whether claims are true or false "
            "2. For research: Present key insights in a logical structure "
            "3. Keep reports under 500 words with brief source mentions"
        )
    )
    
    # Execute the Writer Agent with the analysis (output is shown to user)
    final_report = writer_agent(
        f"Create a report on '{user_input}' based on this analysis:\n\n{analysis}"
    )
    
    print("Report creation complete")
    
    # Return the final report
    return final_report

def bibliography_tracker(**kwargs):
    """
    Callback function to track http_request URLs and write them to a log file.
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
    Use LLM to summarize local files before passing them to the workflow
    
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

if __name__ == "__main__":
    # Print welcome message
    print("\nAgentic Workflow: Research Assistant\n")
    print("This demo shows Strands agents in a workflow with web and local file research.")
    print("Try research questions or fact-check claims.")
    print("\nExamples:")
    print("- \"What are quantum computers?\"")
    print("- \"Lemon cures cancer\"")
    print("- \"Tuesday comes before Monday in the week\"")
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye!")
                break
            
            # Process the input through the workflow of agents
            final_report = run_research_workflow(user_input)
        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try a different request.")