import os
import sys
import traceback
from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("AIzaSyDnsQ_EaKER5TghXoh8mpkoy_tXZoaYZ58
")

if not GEMINI_API_KEY:
    print("ERROR: Please add GEMINI_API_KEY to your .env file.")
    sys.exit(1)

# Initialize the AI agent with Gemini
def create_agent():
    return Agent(
        task="",
        llm=ChatGoogle(model="gemini-2.5-flash", api_key=GEMINI_API_KEY),
        # Extend here with browser or other integrations if needed
    )

def print_intro():
    print("=" * 60)
    print("🤖  Welcome to your AI Assistant")
    print("Type what you want the AI to do for you (or type 'exit' to quit).")
    print("=" * 60)

def main():
    print_intro()
    agent = create_agent()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Exiting. Have a great day!")
                break

            agent.task = user_input
            print("Agent: (thinking...)\n")
            result = agent.run_sync()
            print(f"Agent: {result}")

            # Ask for manual help if needed
            if any(kw in str(result).lower() for kw in ["captcha", "sign up", "manual", "verification"]):
                print("\n⚠️  The agent needs your help to complete this step.")
                print("Please complete the required task in your browser or as needed.")
                input("Press Enter when you're done to continue...")

        except KeyboardInterrupt:
            print("\n👋 Exiting. Goodbye!")
            break
        except Exception:
            print("\n❌ An error occurred:")
            traceback.print_exc()
            print("Restarting agent...")

if __name__ == "__main__":
    main()
