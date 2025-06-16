import git
import os
class GitIntegration:
    def clone_repo(self,repo_url,clone_path = "/tmp/clonedpath"):
        if os.path.exists(clone_path):
            os.system(f"rm -rf {clone_path}")
        git.Repo.clone_from(repo_url,clone_path)
        return clone_path
    