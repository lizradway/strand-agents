# Agentic Workflow: Research Assistant

This project demonstrates an **agentic workflow** for research and fact-checking using **Strands agents**, combining both **web research** and **local file retrieval**. It leverages multiple specialized agents that collaborate sequentially to gather, verify, and summarize information. This implementation is built on top of the[multi-agent workflow example used in the Strand SDK Documentation](https://github.com/strands-agents/docs/blob/main/docs/examples/python/agents_workflows.md).

---

## Key Features

* **Multi-agent workflow**: Separate agents for web research, local file research, analysis, and report writing.
* **Web research**: Gathers information using the `http_request` tool.
* **Local file research**: Uses Retrieval-Augmented Generation (RAG) to summarize and reference local sources.
* **Fact-checking and synthesis**: Analyst Agent evaluates findings and rates accuracy.
* **Automated report generation**: Writer Agent produces concise, structured reports.
* **Bibliography tracking**: URLs and local source files are logged automatically.

---

## Installation

1. Ensure Python 3.9+ is installed.
2. Install required packages (example, adjust for your environment):

```bash
pip install strands strands-tools
```

3. Clone the repository and navigate to the project directory:

```bash
git clone <repo-url>
cd <project-directory>
```

---

## Directory Structure

```
.
├── research_assistant.py   # Main workflow script
├── sources/                # Local text sources for RAG
├── bibliography.log        # Generated bibliography of URLs and files
└── README.md
```

* **`sources/`**: Place any `.txt` files you want the agent to use for local research here.
* **`bibliography.log`**: Automatically updated with all sources accessed during research.

---

## Usage

Run the research assistant script:

```bash
python research_assistant.py
```

You will be prompted to enter a query or claim. Example queries:

* `"Thomas Edison invented the light bulb"`
* `"Tuesday comes before Monday in the week"`
* `"What are quantum computers?"`

Type `exit` to quit the program.

---

## Workflow Process

1. **Web Researcher Agent**

   * Gathers web information using `http_request`.
   * Limits requests to 1–2 sources and extracts key content.

2. **Local Researcher Agent**

   * Optionally summarizes local `.txt` files using RAG.
   * Produces concise summaries with file references.

3. **Analyst Agent**

   * Verifies factual claims (rating accuracy 1–5).
   * Synthesizes findings for research queries (3–5 key insights).
   * Evaluates reliability of sources.

4. **Writer Agent**

   * Produces the final report under 500 words.
   * Presents fact-check results or research insights clearly.
   * Includes brief source mentions from web and local files.

---

## Features in Detail

* **Interactive Consent for Local Sources**: You can choose whether to include local files for each query.
* **Chunking for Large Files**: Large local files are automatically broken into chunks for summarization.
* **Bibliography Tracking**: All URLs accessed via web requests and local files mentioned are appended to `bibliography.log`.

---

## Example Workflow

1. User inputs: `"Lemon cures cancer"`
2. Web Researcher finds recent articles and relevant studies.
3. Local Researcher checks local sources for supporting evidence.
4. Analyst Agent rates claim as false based on evidence.
5. Writer Agent generates a concise report explaining findings and sources.

---

## Next Steps

1. Integration of Bedrock Knowledge Base: Allows for shared and use-case specific knowledge access
2. Source Restriction: Restrict HTTP access to sources for specific use cases (ie. JSTOR for academic research)
3. User Interaction: Allow user to engage further and iterate on research questions