

from synthesis.baseDSL.mainBase.s_s import S_S
from synthesis.baseDSL.mainBase.S import S
from synthesis.baseDSL.mainBase.node import Node


class S_S_E1(S_S):
    
    
    def __init__(self, sL : S= None, sR : S=None):
        self._sLeft = sL
        self._sRight = sR
        
    def sample(self,budget):
        from synthesis.extent1DSL.extent1Main.s_E1 import S_E1
        sL = S_E1()
        sL.sample(budget/2)
        
        sR = S_E1()
        sR.sample(budget/2)
        self._sLeft = sL
        self._sRight = sR
    
    def countNode(self,l : list[Node]):
        l.append(self)
        self._sLeft.countNode(l)
        self._sRight.countNode(l)
        
    def mutation(self,bugdet):
        self.sample(bugdet)