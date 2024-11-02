from __future__  import annotations
from typing import TYPE_CHECKING

from synthesis.baseDSL.mainBase.node import Node
from synthesis.extent1DSL.extent1Main.c_E1 import C_E1
from synthesis.extent1DSL.extent1Main.empty_E1 import Empty_E1
from synthesis.extent1DSL.extent1Main.for_S_E1 import For_S_E1
from synthesis.extent1DSL.extent1Main.s_s_E1 import S_S_E1
if TYPE_CHECKING:
    from synthesis.extent1DSL.util.Factory_E1 import Factory_E1


from synthesis.baseDSL.mainBase.S import S
from synthesis.baseDSL.mainBase.S import ChildS
import random



class S_E1(S):
  
    def __init__(self, childS : ChildS=None):
        self._childS = childS
       
       
    def countNode(self,l : list[Node]):
        l.append(self)
        self._childS.countNode(l)
        
    def raffleChild(self, budget :int):
        op = 0
        if budget >= 1: op = 1
        if budget >= 2: op = 2
        if budget >= 3: op = 3
        if op <= 0:
            return Empty_E1() 
        
        r = random.randint(0,op-1)
        
        if r == 0: return C_E1()
        if r == 1: return S_S_E1()
        if r == 2: return For_S_E1()
        
        return Empty_E1() 
        
     
    def sample(self,bugdet):
       
        action = self.raffleChild(bugdet)
    
        action.sample(bugdet)
        self._childS = action
        
    def sample2(self,bugdet,n):
       
        action = S_S_E1()
        aux = S_E1()
        aux1 = S_E1(n)
        aux.sample(bugdet)
        r = random.randint(0,1)
        if r == 0: 
            action._sLeft = aux
            action._sRight = aux1
        if r == 1: 
            action._sLeft = aux1
            action._sRight = aux
            
        self._childS = action
            
    def mutation(self,bugdet):
        n = self._childS
        if random.random() <= 0.5:
            self.sample(bugdet)
        else:
            self.sample2(bugdet,n)
        
        