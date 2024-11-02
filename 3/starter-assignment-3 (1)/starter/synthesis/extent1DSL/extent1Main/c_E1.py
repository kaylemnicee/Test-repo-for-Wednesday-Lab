from __future__  import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from synthesis.extent1DSL.util.Factory_E1 import Factory_E1
 


import random


from synthesis.baseDSL.mainBase.c import C, ChildC
from synthesis.baseDSL.mainBase.node import Node
from synthesis.extent1DSL.util.Factory_E1 import Factory_E1


class C_E1(C):

        
    def __init__(self, childC : ChildC=None):
        self._childC = childC
        
    def sample(self,budget):
        f = Factory_E1()
        rules = self.rules(f)
        r = random.randint(0,len(rules)-1)
        
        action = rules[r]
      
        action.sample()
        self._childC = action
        
    def countNode(self,l : list[Node]):
        l.append(self)
        self._childC.countNode(l)
        
    def mutation(self,bugdet):
        self.sample(bugdet)
        
    
        
        

