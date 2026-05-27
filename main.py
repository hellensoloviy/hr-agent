from agent import run_agent_turn

def main():
    history = []
    print("\n" + "="*50)
    print("  TechCorp HR Agent — powered by Claude")
    print("="*50)
    print("Type 'quit' to exit | 'history' to see turns\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "history":
            print(f"\n[{len(history)} messages in history]\n")
            continue
        
        print()  # Spacing before tool logs
        response, history = run_agent_turn(user_input, history)
        print(f"\nAlex: {response}\n")

if __name__ == "__main__":
    main()