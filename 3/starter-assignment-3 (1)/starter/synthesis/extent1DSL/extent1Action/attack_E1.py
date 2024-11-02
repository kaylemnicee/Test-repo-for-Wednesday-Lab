


from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy
from synthesis.baseDSL.actionBase.attack import Attack
from synthesis.baseDSL.mainBase.node import Node
from synthesis.extent1DSL.almostTerminal.opponentPolicy_E1 import OpponentPolicy_E1


class Attack_E1(Attack):
    
        
    def __init__(self,op :OpponentPolicy =OpponentPolicy_E1()) -> None:
        self._op =op 
        self._used = False
        
    def sample(self):
        op=OpponentPolicy_E1()
        op.sample()
        self._op = op
        
    def countNode(self,l : list[Node]):
        l.append(self)
        self._op.countNode(l)
        
    def mutation(self,bugdet):
        self.sample()
        