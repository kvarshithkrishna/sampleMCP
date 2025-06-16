from agents.BaseAgent import BaseAgent
from integrations.git_integration import GitIntegration
import os
class ReadMe(BaseAgent):
    def __init__(self):
        super().__init__(name = "Readme",version = "v1")
        self.git =GitIntegration()
    def run(self,repo_url):
        path = self.git.clone_repo(repo_url)
        readmepath = os.path.join(path,"README.md")
        if not os.path.exists(readmepath):
            return {"error":"Not found"}
        
        with open(readmepath, "r",encoding="UTF-8") as f:
            content=f.read()
        return{
            "path":readmepath,
            "content": content[:1000] if len(content)>1000 else content
        }
        


        