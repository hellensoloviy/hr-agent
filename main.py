from agent import run_agent_turn
from session_manager import save_session, load_session, list_sessions

def main():
    history = []
    session_id = None
    
    print("\n" + "="*50)
    print("  TechCorp HR Agent — powered by Claude")
    print("="*50)
    
    # Offer to resume a session
    sessions = list_sessions()
    sessions = list_sessions()
    if sessions:
        last = sessions[0]  # most recent
        print(f"\nLast session: {last['saved_at'][:16]} ({last['turns']} turns)")
        resume = input("Resume it? (y/n): ").strip().lower()
        if resume == "y":
            try:
                history = load_session(last["id"])
                session_id = last["id"]
                print(f"Resumed. {len(history)} messages loaded.\n")
            except FileNotFoundError:
                print("Could not load session. Starting fresh.\n")
                
    print("\nType 'quit' to exit | 'save' to save session\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == "quit":
            if history:
                session_id = save_session(history, session_id)
                print(f"Session saved as: {session_id}")
            break
        
        if user_input.lower() == "save":
            session_id = save_session(history, session_id)
            print(f"Saved as: {session_id}\n")
            continue
        
        print()
        response, history = run_agent_turn(user_input, history)
        print(f"\nAlex: {response}\n")

if __name__ == "__main__":
    main()