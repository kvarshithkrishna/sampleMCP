from abc import ABC, abstractmethod
class BaseAgent(ABC):
    """
    base agent
    """

    def __init__(self,name="BaseAgent",version="v1"):
        self.name = name
        self.version = version
    #for metadata
        
    @abstractmethod
    def run(self,*args,**kwargs):
        """
        logic
        """
        pass