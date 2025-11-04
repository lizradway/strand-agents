#!/usr/bin/env python3
from workflow import run_research_workflow

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

def main():
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
            print("Please try again.")

if __name__ == "__main__":
    main()