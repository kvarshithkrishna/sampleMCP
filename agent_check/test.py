# import json
# from agents.todoagentextractor  import TodoAgent
# from agents.aisummarizer import Summarizer

# def main():
#     print("👋 Welcome to Repo Agent!")
    
#     # Ask user for the repo URL
#     repo_url = input("📎 Enter GitHub repo URL: ").strip()
    
#     # Ask what operation they want
#     print("\n🤖 What do you want to do?")
#     print("1. Extract TODOs")
#     print("2. Summarize repo")
#     choice = input("Enter choice (1 or 2): ").strip()

#     # Choose agent
#     if choice == "1":
#         agent = TodoAgent()
#         result = agent.run(repo_url)
#     elif choice == "2":
#         agent = Summarizer()
#         result = agent.run(repo_url)  # Assuming local clone path is fixed in RepoSumm
#     else:
#         print("❌ Invalid choice.")
#         return

#     print("\n✅ Operation Result:\n")
    
#     # Output result nicely
#     if isinstance(result, list) or isinstance(result, dict):
#         print(json.dumps(result, indent=2))
#     else:
#         print(result)

# if __name__ == "__main__":
#     main()
# test.py

from protocols.mcp import MCPTool
from orchestrator.orchestrator import Orchestrator
import json

def main():
    print("🤖 What do you want to do?")
    print("1. Extract TODOs")
    print("2. Summarize repo")
    print("3.Read me")
    choice = input("Enter choice (1 or 2 or 3): ").strip()

    task_map = {"1": "extract_todos", "2": "summarize","3":"read_me"}
    task = task_map.get(choice)

    if not task:
        print("Invalid choice.")
        return

    repo_url = input("🔗 Enter public GitHub repo URL: ").strip()
    message = MCPTool(repo_url=repo_url, task=task)

    orchestrator = Orchestrator()
    result = orchestrator.handle(message)
    print("\n✅ Result:\n")
    print(json.dumps(result, indent=2) if isinstance(result, (dict, list)) else result)

if __name__ == "__main__":
    main()
