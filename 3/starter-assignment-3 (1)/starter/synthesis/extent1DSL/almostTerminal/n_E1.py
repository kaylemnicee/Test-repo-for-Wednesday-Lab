
import random

from synthesis.baseDSL.almostTerminal.n import N
from synthesis.baseDSL.mainBase.node import Node



class N_E1(N):
    
    
    def __init__(self,n=None) -> None:
        self._n = n
        
    def sample(self,act=None)->None:
        rules = self.rules(act)
        r = random.randint(0,len(rules) - 1)
        self._n = rules[r]
        
    def countNode(self,l : list[Node]):
        l.append(self)
        
    def mutation(self,bugdet):
        self.sample()