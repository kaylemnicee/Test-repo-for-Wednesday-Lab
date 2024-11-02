import random


from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy
from synthesis.baseDSL.mainBase.node import Node


class OpponentPolicy_E1(OpponentPolicy):
    
    
        
    def __init__(self,op=None) -> None:
        self._op = op
        
    def sample(self):
        rules = self.rules()
        r = random.randint(0,len(rules) - 1)
        self._op = rules[r]
        
    def countNode(self,l : list[Node]):
        l.append(self)
        
    def mutation(self,bugdet):
        self.sample()