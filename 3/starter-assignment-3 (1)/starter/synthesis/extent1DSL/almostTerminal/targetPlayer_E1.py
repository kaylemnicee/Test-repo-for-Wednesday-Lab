
import random

from synthesis.baseDSL.almostTerminal.targetPlayer import TargetPlayer
from synthesis.baseDSL.mainBase.node import Node


class TargetPlayer_E1(TargetPlayer):
    
   
        
    def __init__(self,tp=None) -> None:
        self._tp = tp
        
    def sample(self)->None:
        rules = self.rules()
        r = random.randint(0,len(rules) - 1)
        self._tp = rules[r]
        
    def countNode(self,l : list[Node]):
        l.append(self)
        
    def mutation(self,bugdet):
        self.sample()
    
    