from abc import ABC, abstractmethod

class AlmostTerminal(ABC):
    
    @abstractmethod
    def rules(self):#->list[str]:
        pass
    
    @classmethod
    def getName(cls)->str:
        return cls.__name__
    
    def getValue(self)->str:
        pass
    
    def setValue(self, s :str)->None:
        pass
	
    def translate(self)->str:
        pass
 

    