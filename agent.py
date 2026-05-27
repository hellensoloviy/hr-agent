import anthropic
import time
from tools import TOOLS
from handlers import run_tool
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are Alex, a professional HR assistant at TechCorp.
You help recruiters manage candidates and schedule interviews.

Your capabilities:
- Look up open positions and candidate profiles
- Check calendar availability and book interview slots
- Update candidate notes after conversations

Guidelines:
- Always confirm before booking an interview
- Be concise but warm in tone
- If asked to book, first check availability if you don't already have it
- Today's date is 2025-06-09 (Monday)

When showing lists, format them clearly for easy reading."""


def run_agent_turn(user_message: str, history: list) -> tuple[str, list]:
    """Process one user turn and return the response + updated history."""
    
    history = trim_history(history)
    history.append({"role": "user", "content": user_message})
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=history
        )
        
        if response.stop_reason == "end_turn":
            text = next(b.text for b in response.content if hasattr(b, "text"))
            history.append({"role": "assistant", "content": response.content})
            return text, history
        
        if response.stop_reason == "tool_use":
            history.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n  🔧 {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    print(f"  ✓  {result[:120]}{'...' if len(result) > 120 else ''}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            history.append({"role": "user", "content": tool_results})

# Trim to avoid hitting the context window limit
def trim_history(history: list, max_turns: int = 20) -> list:
    """
    Keep only the most recent N user/assistant turn pairs.
    Always preserve the first message for context anchoring.
    """
    if len(history) <= max_turns * 2:
        return history
    
    # Keep first exchange + last (max_turns - 1) exchanges
    first_two = history[:2]
    recent = history[-(max_turns - 1) * 2:]
    return first_two + recent


# - Function Re-try 
def call_claude_with_retry(client, max_retries=3, **kwargs):
    """Call Claude API with exponential backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"  Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
        except anthropic.APIError as e:
            print(f"  API error: {e}")
            raise