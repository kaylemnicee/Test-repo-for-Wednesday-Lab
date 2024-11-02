from synthesis.baseDSL.almostTerminal.direction import Direction
from synthesis.baseDSL.almostTerminal.n import N
from synthesis.baseDSL.almostTerminal.utype import Utype
from synthesis.baseDSL.actionBase.harvest import Harvest
from synthesis.baseDSL.actionBase.train import Train
from synthesis.baseDSL.mainBase.node import Node
from synthesis.extent1DSL.almostTerminal.direction_E1 import Direction_E1
from synthesis.extent1DSL.almostTerminal.n_E1 import N_E1
from synthesis.extent1DSL.almostTerminal.utype_E1 import Utype_E1


class Harvest_E1(Harvest):
    
        
    def __init__(self, n : N = N_E1()) -> None:
        self._n = n
        self._used = False
        
    def sample(self):
        n = N_E1()
        n.sample("h")
        self._n = n
        
         
    def countNode(self,l : list[Node]):
        l.append(self)
        self._n.countNode(l)
        
    def mutation(self,bugdet):
        self.sample()
     