# HR Interview Scheduling Agent

An AI-powered HR assistant built with the Anthropic Claude API. 
Demonstrates tool use, the agent loop (ReAct pattern), and persistent state.

## Features
- Natural language interface for HR workflows
- Books and tracks interview slots
- Manages candidate profiles and pipeline stages
- Persists conversation sessions for continuity

## Architecture
User Input → Agent Loop → Claude API
↓ (tool_use)
Tool Dispatcher
↓
JSON Data Layer (calendar, candidates, positions)

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install anthropic python-dotenv rich
echo "ANTHROPIC_API_KEY=your-key" > .env
python main.py
```

## Key Concepts Demonstrated
- **Tool Use / Function Calling**: Model signals intent; code executes
- **Agent Loop**: while stop_reason == "tool_use": run tools, loop
- **ReAct Pattern**: Reason about task → Act via tools → Observe results
- **Stateless LLMs**: Full conversation history passed with every API call
- **External Memory**: Persistent JSON data layer read/written by tools