import os
import re
class RepoScanner:
    def repo_scanner(self,directory):
        todos = []
        for root,_,files in os.walk(directory):
            for file in files:
                if file.endswith((".py",".ts",".js",".html",".md")):
                    path = os.path.join(root,file)
                    with open(path,"r") as f:
                        for i, line in enumerate(f.readlines(),1):
                            if "TODO" in line:
                                todos.append({
                                    "line":i,
                                    "path":path,
                                    "comment":line.strip()
                                })
        return todos