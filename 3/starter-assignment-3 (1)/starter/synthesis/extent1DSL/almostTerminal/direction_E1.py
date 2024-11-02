import random

from synthesis.baseDSL.almostTerminal.direction import Direction
from synthesis.baseDSL.mainBase.node import Node


class Direction_E1(Direction):
    
   
        
    def __init__(self,direc=None) -> None:
        self._direc = direc
        
    def sample(self)->None:
        rules = self.rules()
        r = random.randint(0,len(rules) - 1)
        self._direc = rules[r]
        
    def countNode(self,l : list[Node]):
        l.append(self)
        
    def mutation(self,bugdet):
        self.sample()