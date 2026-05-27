from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from agent.loop import run_agent_turn
from session_manager import save_session, load_session, list_sessions

console = Console()
SESSIONS_DIR = Path("data/sessions")


def cleanup_old_sessions(days=7):
    cutoff = datetime.now().timestamp() - (days * 86400)
    for path in SESSIONS_DIR.glob("*.json"):
        if path.stat().st_mtime < cutoff:
            path.unlink()


def print_header():
    console.print(Panel.fit(
        "[bold blue]TechCorp HR Agent[/bold blue]\n[dim]powered by Claude Sonnet[/dim]",
        border_style="blue"
    ))


def main():
    history = []
    session_id = None

    print_header()
    cleanup_old_sessions()

    sessions = list_sessions()
    if sessions:
        last = sessions[0]
        console.print(f"\n[dim]Last session: {last['saved_at'][:16]} ({last['turns']} turns)[/dim]")
        resume = Prompt.ask("Resume it?", choices=["y", "n"], default="n")
        if resume == "y":
            try:
                history = load_session(last["id"])
                session_id = last["id"]
                console.print(f"[green]Resumed. {len(history)} messages loaded.[/green]\n")
            except FileNotFoundError:
                console.print("[red]Could not load session. Starting fresh.[/red]\n")

    console.print("[dim]Commands: quit · save · clear[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold]You[/bold]").strip()
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            if history:
                session_id = save_session(history, session_id)
                console.print(f"[dim]Session saved: {session_id}[/dim]")
            break
        if user_input.lower() == "save":
            session_id = save_session(history, session_id)
            console.print(f"[dim]Saved: {session_id}[/dim]\n")
            continue
        if user_input.lower() == "clear":
            history = []
            console.clear()
            print_header()
            continue

        console.print()
        response, history, _ = run_agent_turn(user_input, history)
        console.print(Panel(Markdown(response), title="[bold green]Alex[/bold green]", border_style="green"))
        console.print()


if __name__ == "__main__":
    main()