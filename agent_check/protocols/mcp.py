class MCPTool:
    def __init__(self,repo_url:str,task:str):
        """
        mcp tool 
        """
        self.repo_url = repo_url
        self.task = task.lower()
    def to_dict(self):
        return{
            "repo_url":self.repo_url,
            "task":self.task
        }
        