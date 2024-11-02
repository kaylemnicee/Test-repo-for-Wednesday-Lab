


from synthesis.baseDSL.actionBase.AttackIfrange import AttackIfrange
from synthesis.baseDSL.mainBase.node import Node


class AttackIfrange_E1(AttackIfrange):
    def __init__(self) -> None:
        self._used = False
        pass
    
    def sample(self):
        pass
    
         
    def countNode(self,l : list[Node]):
        pass
        
    def mutation(self,bugdet):
        self.sample()