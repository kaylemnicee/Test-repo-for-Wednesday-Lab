from __future__  import annotations


from typing import TYPE_CHECKING
from synthesis.baseDSL.mainBase.empty import Empty

from synthesis.baseDSL.util.factory import Factory
from synthesis.extent1DSL.almostTerminal.direction_E1 import Direction_E1
from synthesis.extent1DSL.almostTerminal.n_E1 import N_E1
from synthesis.extent1DSL.almostTerminal.opponentPolicy_E1 import OpponentPolicy_E1
from synthesis.extent1DSL.almostTerminal.targetPlayer_E1 import TargetPlayer_E1
from synthesis.extent1DSL.almostTerminal.utype_E1 import Utype_E1
from synthesis.extent1DSL.extent1Action.AttackIfrange_E1 import AttackIfrange_E1
from synthesis.extent1DSL.extent1Action.attack_E1 import Attack_E1
from synthesis.extent1DSL.extent1Action.build_E1 import Build_E1
from synthesis.extent1DSL.extent1Action.harvest_E1 import Harvest_E1
from synthesis.extent1DSL.extent1Action.moveAway_E1 import MoveAway_E1
from synthesis.extent1DSL.extent1Action.moveToUnit_E1 import MoveToUnit_E1
from synthesis.extent1DSL.extent1Action.train_E1 import Train_E1
from synthesis.extent1DSL.extent1Main.empty_E1 import Empty_E1

from synthesis.extent1DSL.extent1Main.for_S_E1 import For_S_E1

from synthesis.extent1DSL.extent1Main.s_s_E1 import S_S_E1
if TYPE_CHECKING:
    from synthesis.baseDSL.almostTerminal.direction import Direction
    from synthesis.baseDSL.almostTerminal.targetPlayer import TargetPlayer
    from synthesis.baseDSL.almostTerminal.n import N
    from synthesis.baseDSL.almostTerminal.utype import Utype
    from synthesis.baseDSL.actionBase.build import Build
    from synthesis.baseDSL.actionBase.harvest import Harvest

    from synthesis.baseDSL.actionBase.AttackIfrange import AttackIfrange
    from synthesis.baseDSL.actionBase.moveAway import MoveAway
    from synthesis.baseDSL.actionBase.moveToUnit import MoveToUnit
    from synthesis.baseDSL.actionBase.train import Train

    from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy
    from synthesis.baseDSL.actionBase.attack import Attack
    from synthesis.baseDSL.mainBase.S import S, ChildS
    from synthesis.baseDSL.mainBase.for_S import For_S
    from synthesis.baseDSL.mainBase.c import C, ChildC
    from synthesis.baseDSL.mainBase.s_s import S_S


from synthesis.baseDSL.util.factory import Factory


class Factory_E1(Factory):
    
    def build_S(self,childS : ChildS = None) -> S:
        from synthesis.extent1DSL.extent1Main.s_E1 import S_E1
        if childS == None: return S_E1()
        else: return S_E1(childS)

 
    def build_For_S(self,s : S = None) -> For_S:
        if s == None: return For_S_E1()
        else: return For_S_E1(s)
    
    def build_C(self,childC : ChildC= None) -> C:
        from synthesis.extent1DSL.extent1Main.c_E1 import C_E1
        if childC == None: return C_E1()
        else: return C_E1(childC)
    
   
    def build_S_S(self,sL: S=None, sR: S=None) -> S_S:
        if sL == None: return S_S_E1()
        else: return S_S_E1(sL,sR)
    
    
    
    #actions
    def build_Attack(self,op : OpponentPolicy=None) -> Attack:
        if op == None: return Attack_E1()
        else: return Attack_E1(op)
    
    def build_AttackIfrange(self) -> AttackIfrange:
        return AttackIfrange_E1()
    
    def build_Empty(self,) -> Empty:
        return Empty_E1()
    
    def build_Build(self,utype : Utype=None, direc:Direction=None, n: N=None) -> Build:
        if utype == None: return Build_E1()
        else: return Build_E1(utype,n, direc)
    	

    def build_Harvest(self,n : N=None) -> Harvest:
        if n == None: return Harvest_E1()
        else: return Harvest_E1(n)
    
    def build_MoveAway(self) -> MoveAway:
        return MoveAway_E1()



    def build_MoveToUnit(self,tp:TargetPlayer=None, op:OpponentPolicy=None) -> MoveToUnit:
        if tp == None: return MoveToUnit_E1()
        else: return MoveToUnit_E1(op, tp)
	
 
 
    def build_Train(self, utype : Utype=None,  direc : Direction=None,  n : N=None) -> Train:
        if utype == None: return Train_E1()
        else: return Train_E1(utype,n,direc)


	# AlmostTerminal
    
   
    def build_Utype(self,value : str=None) -> Utype:
        if value == None: return
        return Utype_E1(value)
    
    
    def build_N(self,value : str=None) -> N:
        if value == None: return
        return N_E1(value)
        
   
    def build_Direction(self,value : str=None) -> Direction:
        if value == None: return Direction()
        return Direction_E1(value)


    
    def build_TargetPlayer(self,value : str=None) -> TargetPlayer:
        if value == None: return TargetPlayer()
        return TargetPlayer_E1(value)
    
    
    def build_OpponentPolicy(self,value : str=None) -> OpponentPolicy:
        if value == None: return OpponentPolicy()
        return OpponentPolicy_E1(value)