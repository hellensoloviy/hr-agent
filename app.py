import gradio as gr
from agent import run_agent_turn

def chat(message: str, history: list):
    """Gradio-compatible chat function."""
    # Convert Gradio history format → our format
    our_history = []
    for user_msg, assistant_msg in history:
        our_history.append({"role": "user", "content": user_msg})
        our_history.append({"role": "assistant", "content": assistant_msg})
    
    response, our_history = run_agent_turn(message, our_history)
    return response

demo = gr.ChatInterface(
    fn=chat,
    title="TechCorp HR Agent",
    description="Powered by Claude Sonnet. Ask me about candidates, positions, and interview scheduling.",
    examples=[
        "What positions are currently open?",
        "Show me candidates in the final round",
        "What interview slots are available on June 11th?",
    ]
)

if __name__ == "__main__":
    demo.launch()