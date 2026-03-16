# Technical Interview Agent

Multi-agent AI system that conducts technical interviews, evaluates answers, and provides feedback using LLMs, LangGraph, and RAG.

## Features

- **Multi-Agent Architecture**: Uses specialized agents for different tasks
- **Domain-Specific Questions**: Generates questions based on job role and resume
- **RAG-Powered Knowledge Base**: Retrieves relevant information from question banks
- **Follow-up Questions**: Asks intelligent follow-up questions based on answers
- **Comprehensive Evaluation**: Scores answers and provides detailed feedback
- **MCP Integration**: Exposes tools through an MCP server

## Project Structure

```
technical-interview-agent/
├── agents/                  # AI agents (interviewer, evaluator, etc.)
├── nodes/                   # LangGraph nodes
├── graphs/                  # LangGraph workflows
├── states/                  # State management
├── tools/                   # Custom tools
├── mcp_server/              # MCP server implementation
├── data/                    # Data files
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd technical-interview-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

### Run the Interview

```bash
python run_interview.py
```

### Start MCP Server

```bash
python mcp_server/mcp_server.py
```

## Configuration

### Interview Parameters

Edit `run_interview.py` to configure:
- `job_role`: Job title for the interview
- `resume_path`: Path to candidate's resume
- `num_questions`: Number of questions to ask
- `domain`: Interview domain (e.g., "software_engineering")

### Agent Configuration

Edit agent files in `agents/` to customize:
- LLM model selection
- System prompts
- Tool usage

## Tools

The system includes the following tools:

| Tool | Description |
|------|-------------|
| `resume_parser_tool` | Parses candidate resumes |
| `question_bank_tool` | Retrieves questions from knowledge base |
| `vector_search_tool` | Searches vector database for relevant information |
| `scoring_tool` | Scores answers and provides feedback |

## MCP Server

The MCP server exposes the following tools for use with other MCP clients:

- `resume_parser.parse_resume` - Parse a resume file
- `question_bank.get_questions` - Get interview questions
- `vector_search.search` - Search vector database
- `scoring.score_answer` - Score a candidate's answer

## Development

### Adding New Tools

1. Create a new tool in `tools/`
2. Register the tool in `mcp_server/tools_registry.py`
3. Update `mcp_server/mcp_server.py` to include the tool

### Creating New Agents

1. Create a new agent file in `agents/`
2. Define the agent using `langgraph.prebuilt.create_react_agent`
3. Update `graphs/interview_graph.py` to include the agent

### Adding New Nodes

1. Create a new node function in `nodes/`
2. Register the node in `graphs/interview_graph.py`
3. Update the workflow to include the node

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue in the repository.
