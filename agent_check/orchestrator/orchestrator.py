from agents.todoagentextractor import TodoAgent
from agents.aisummarizer import Summarizer
from agents.readmeagent import ReadMe
from protocols.mcp import MCPTool
class Orchestrator:
    def __init__(self):
        self.agents={
            "summarize":Summarizer(),
            "extract_todos":TodoAgent(),
            "read_me":ReadMe()
        }
    def handle(self,message:MCPTool):
        agents = self.agents.get(message.task)
        if not agents:
            raise ValueError("not right")
        return agents.run(message.repo_url)
        