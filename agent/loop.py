import anthropic
from dotenv import load_dotenv
from .tools import TOOLS
from .handlers import run_tool

load_dotenv()

client = anthropic.Anthropic()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2048
SYSTEM_PROMPT = """You are Alex, a professional HR assistant at TechCorp.
You help recruiters manage candidates and schedule interviews.
Today's date is 2026-05-27. Always confirm before booking an interview."""


def trim_history(history: list, max_turns: int = 20) -> list:
    if len(history) <= max_turns * 2:
        return history
    return history[:2] + history[-(max_turns - 1) * 2:]


def run_agent_turn(user_message: str, history: list) -> tuple[str, list, list]:
    """
    Run one user turn through the agent loop.
    Returns (response_text, updated_history, tools_used)
    """
    history = trim_history(history)
    history.append({"role": "user", "content": user_message})
    tools_used = []

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=history
        )

        if response.stop_reason == "end_turn":
            text = next(b.text for b in response.content if hasattr(b, "text"))
            history.append({"role": "assistant", "content": response.content})
            return text, history, tools_used

        if response.stop_reason == "tool_use":
            history.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"  🔧 {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    tools_used.append({
                        "name": block.name,
                        "input": block.input,
                        "result": result
                    })
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            history.append({"role": "user", "content": tool_results})