# Technical Interview Agent

Built a multi-agent AI interview system with a state-driven orchestration engine, leveraging **MCP** for modular tool execution and **RAG** for context-aware questioning, enabling adaptive interviews, response evaluation, and automated feedback/report generation via a **FastAPI** based backend.

## 🚀 Features

- **Multi-Agent Orchestration**: Specialized agents for resume analysis, interviewing, evaluation, follow-up, and reporting.
- **Web Interface**: Modern FastAPI-backend with a clean chat interface for candidates.
- **MCP Architecture**: Decoupled tool execution using Model Context Protocol (MCP) Client-Server model.
- **Autonomous Flow**: State-machine driven interview logic that adapts based on candidate performance.
- **RAG Integration**: Project-specific knowledge retrieval using Chroma vector store.
- **Automated Reporting**: Generates a detailed PDF-ready evaluation report at the end of the session.

## 📁 Project Structure

```text
technical-interview-agent/
├── agents/              # Specialized AI agents (LLM prompts & logic)
├── mcp_server/          # MCP Server implementation (Tools exposure)
├── nodes/               # Workflow nodes
├── services/            # RAG, Vector Store, and Ingestion services
├── states/              # TypedDict state management
├── static/              # Frontend web assets (HTML/JS/CSS)
├── tools/               # Core tool implementations
├── app.py               # CLI entry point (Asynchronous)
├── main.py              # FastAPI Web entry point
├── orchestrator.py      # Core interview state machine logic
├── mcp_client.py        # MCP Client for tool communication
└── .env                 # Environment configuration
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd technical-interview-agent
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root:
   ```env
   OPENAI_API_KEY=your_key
   GROQ_API_KEY=your_key
   MODEL_NAME=gpt-4o  # or your preferred model
   ```

## 🏃 Usage

The system requires the **MCP Server** to be running for tool access.

### 1. Start the MCP Server
In a separate terminal:
```bash
python mcp_server/mcp_server.py
```

### 2. Run the Web Application
```bash
python main.py
```
Visit `http://localhost:8000` to start the interview.

### 3. Run the CLI Version (Optional)
```bash
python app.py
```

## 🧠 Architecture

### Multi-Agent Flow
The `orchestrator.py` manages the transition between different agents:
1.  **Resume Analyzer**: Parses and extracts key skills/projects.
2.  **Interviewer Agent**: Asks technical/HR questions based on context.
3.  **Evaluator Agent**: Analyzes the answer and provides a score (1-10).
4.  **Follow-up Agent**: If the score is low (< 5), it asks a deeper clarification question.
5.  **Report Agent**: Consolidates the full interview history into a summary report.

### MCP Integration
This project uses the **Model Context Protocol** (MCP) to separate the LLM reasoning from tool execution. The agents communicate with the `mcp_server` through the `mcp_client`, allowing for scalable and modular tool management.

## 📝 Configuration

-   **Interview Depth**: Default is set to 2 main questions per session (configurable in `orchestrator.py`).
-   **Persona**: The `interviewer_agent` is currently tuned for an **HR Screening** persona.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
