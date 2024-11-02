import random
# from tkinter import N
from synthesis.baseDSL.almostTerminal.n import N
from synthesis.baseDSL.almostTerminal.direction import Direction
from synthesis.baseDSL.almostTerminal.utype import Utype

from synthesis.baseDSL.actionBase.build import Build
from synthesis.baseDSL.mainBase.node import Node
from synthesis.extent1DSL.almostTerminal.direction_E1 import Direction_E1
from synthesis.extent1DSL.almostTerminal.n_E1 import N_E1
from synthesis.extent1DSL.almostTerminal.utype_E1 import Utype_E1


class Build_E1(Build):
    
        
    def __init__(self,utype : Utype = Utype_E1(), n : N = N_E1, direc : Direction = Direction_E1) -> None:
        self._type =utype
        self._n = n
        self._direc = direc
        self._used = False
        
    def sample(self):
        n = N_E1()
        n.sample("b")
        self._n = n
        utype = Utype_E1()
        utype.sample("b")
        self._type = utype
        direc = Direction_E1()
        direc.sample()
        self._direc = direc
        
    def countNode(self,l : list[Node]):
        l.append(self)
        self._type.countNode(l)
        self._n.countNode(l)
        self._direc.countNode(l)
        
    def mutation(self,bugdet):
        self.sample()