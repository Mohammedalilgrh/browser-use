import sys
import traceback
import os
import platform
import subprocess
from browser_use import Agent, ChatGoogle, Browser

# Direct Gemini API key (no .env needed)
GEMINI_API_KEY = "AIzaSyDnsQ_EaKER5TghXoh8mpkoy_tXZoaYZ58"

class ManusAgent:
    def __init__(self):
        self.ai_name = "Manus"
        self.intro()
        self.agent = Agent(
            task="",
            llm=ChatGoogle(model="gemini-2.5-flash", api_key=GEMINI_API_KEY),
            browser=Browser(use_cloud=True),
        )

    def intro(self):
        print("=" * 70)
        print(f"🤖  {self.ai_name} AI Assistant - Ultimate System Automation & Chat")
        print("=" * 70)
        print("Capabilities:")
        print(" - Advanced chat, research, problem-solving, coding, file and system automation")
        print(" - Web browsing, file management, command execution, and more")
        print(" - Will ask for your help whenever manual action (CAPTCHA, sign-up, etc.) is needed")
        print(" - To run system commands, prefix with: ! (e.g. !dir, !ls, !python myfile.py)")
        print("Type your request, or 'help' for guidance, or 'exit' to quit.")
        print("=" * 70)

    def run(self):
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in {"exit", "quit"}:
                    print("👋 Exiting. Have a productive day!")
                    break
                if user_input.lower() == "help":
                    self.print_help()
                    continue
                if user_input.startswith("!"):
                    self.run_system_command(user_input[1:])
                    continue

                # AI agent handles the rest
                self.agent.task = user_input
                print(f"{self.ai_name}: (thinking...)\n")
                result = self.agent.run_sync()
                print(f"{self.ai_name}: {result}")

                # Ask for manual help if needed
                if any(kw in str(result).lower() for kw in ["captcha", "sign up", "manual", "verification"]):
                    print("\n⚠️  The agent needs your help to complete this step.")
                    print("Please complete the required task in your browser or as needed.")
                    input("Press Enter when you're done to continue...")

            except KeyboardInterrupt:
                print(f"\n👋 {self.ai_name} session ended by user.")
                break
            except Exception:
                print("\n❌ An error occurred:")
                traceback.print_exc()
                print(f"\nRestarting {self.ai_name} agent...")

    def print_help(self):
        help_text = """
Commands & Usage:
- Just describe your task or problem, and Manus will try to solve it.
- To run a Windows/Linux command, prefix it with ! (example: !dir, !ls, !python script.py)
- To automate browser actions or fill web forms, just describe your goal!
- For coding help, describe your code issue or request code generation.
- For file operations, describe the action (e.g., 'create a text file with this content', 'find file named foo.txt').
- To deploy or run scripts, just ask.
- If Manus needs human intervention (CAPTCHA/sign up), it will prompt you.

Examples:
  - "Summarize the latest news about AI."
  - "Create a folder called Reports and write a summary.txt file."
  - "!echo Hello World"
  - "Download and analyze the CSV file at this URL."
  - "Automate filling out this website's registration form."
  - "Fix this Python code: [paste your code]"
  - "Deploy a simple static site with this HTML."

Type 'exit' to leave, or keep chatting!
"""
        print(help_text)

    def run_system_command(self, cmd):
        print(f"Running system command: {cmd}")
        try:
            if platform.system() == "Windows":
                completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            else:
                completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash")
            output = completed.stdout.strip()
            if output:
                print(output)
            else:
                print(completed.stderr.strip())
        except Exception as e:
            print(f"❌ Failed to run command: {e}")

if __name__ == "__main__":
    ManusAgent().run()
