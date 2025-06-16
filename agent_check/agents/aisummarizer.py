import json
from integrations.git_integration import GitIntegration
from agents.BaseAgent import BaseAgent
from tools.repo_summarizer import RepoSumm

class Summarizer(BaseAgent):
    def __init__(self, name="Summarizer", version="v1"):
        super().__init__(name, version)
        self.git = GitIntegration()
        self.summarizer = RepoSumm()
    
    def run(self, repo_url):
        print("🔄 Cloning repository...")
        path = self.git.clone_repo(repo_url)

        print("🧠 Summarizing codebase...")
        summary = self.summarizer.repo_sum(path)

        return summary
