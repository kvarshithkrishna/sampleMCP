from integrations.git_integration import GitIntegration
from tools.repo_scanner import RepoScanner
from agents.BaseAgent import BaseAgent
class TodoAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="TODOAGENT",version="v2")
        self.git = GitIntegration()
        self.scanner = RepoScanner()
    def run(self,repo_url):
        print("cloning...")
        url = self.git.clone_repo(repo_url)
        print("Scanning")
        todos = self.scanner.repo_scanner(url)
        return todos