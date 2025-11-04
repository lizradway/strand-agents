from agents import create_web_researcher, create_local_researcher, create_analyst, create_writer
from local_tools import can_use_local_sources, gather_local_summaries
from bibliography import bibliography_tracker

def run_research_workflow(user_input):
    """
    Run a five-agent workflow for research and fact-checking with web and file sources.
    Shows progress logs during execution but presents only the final report to the user.
    
    Args:
        user_input: Research query or claim to verify
        
    Returns:
        str: The final report from the Writer Agent
    """
    print(f"\nProcessing: '{user_input}'\n")

    # Step 1: Researcher Agent with enhanced web capabilities
    print("\nStep 1: Researcher Agent gathering web information...\n")
    web_agent = create_web_researcher(bibliography_tracker)

    web_researcher_response = web_agent(
        f"Research: '{user_input}'. Use your available tools to gather information from reliable sources. "
        "Focus on being concise and thorough, but limit web requests to 1-2 sources.",
    )
    
    # Extract only the relevant content from the web researcher response
    web_research_findings = str(web_researcher_response)
    print("Web research complete")

    # Step 2: Researcher Agent with local file search RAG capabilities
    print("\nStep 2: Researcher Agent with local file search...\n")
    local_research_findings = ""

    # Verify user consent to access local source directory
    if can_use_local_sources():

        # Chunk and summarize files
        local_source_summaries = gather_local_summaries()

        # Runs Step 2 local file search only if local source directory is not empty
        if local_source_summaries:

            local_researcher_agent = create_local_researcher(bibliography_tracker)
            local_researcher_response = local_researcher_agent(
                f"Research: '{user_input}'. Use local file summaries to gather information from reliable source files. "
                "Focus on being concise and thorough, but limit file reads to 1-2 sources."
            )

            # Extract only the relevant content from the researcher response
            local_research_findings = str(local_researcher_response)
            print("Local research complete.")

        else:
            print("Skipping Step 2 Researcher Agent with local file search... No local sources found.")
    else:
        print("Skipping Step 2 Researcher Agent with local file search... User declined local source directory access.")

    print("\nPassing research findings to Analyst Agent...")

    # Step 3: Analyst Agent to verify facts
    print("\nStep 3: Analyst Agent analyzing findings...\n")
    analyst_agent = create_analyst()

    # Analyze findings from web and local source
    analyst_response = analyst_agent(
        f"Analyze these findings about '{user_input}':\n\n {web_research_findings}\n\n {local_research_findings}",
    )

    # Extract only the relevant content from the analyst response
    analysis = str(analyst_response)
    print("Analysis complete")
    print("Passing analysis to Writer Agent...")  

    # Step 4: Writer Agent to create report
    print("\nStep 4: Writer Agent creating final report...\n")
    writer_agent = create_writer()
        
    # Execute the Writer Agent with the analysis (output is shown to user)
    final_report = writer_agent(
        f"Create a report on '{user_input}' based on this analysis:\n\n{analysis}"
    )
    print("Report creation complete")
    return final_report