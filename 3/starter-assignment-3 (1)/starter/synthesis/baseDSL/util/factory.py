from __future__  import annotations


from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from synthesis.baseDSL.actionBase.AttackIfrange import AttackIfrange
    from synthesis.baseDSL.mainBase.empty import Empty

    from synthesis.baseDSL.mainBase.s_s import S_S
    from synthesis.baseDSL.almostTerminal.direction import Direction
    from synthesis.baseDSL.almostTerminal.targetPlayer import TargetPlayer
    from synthesis.baseDSL.almostTerminal.utype import Utype
    from synthesis.baseDSL.almostTerminal.n import N
    from synthesis.baseDSL.actionBase.build import Build
    from synthesis.baseDSL.actionBase.harvest import Harvest

    from synthesis.baseDSL.actionBase.AttackIfrange import Idle
    from synthesis.baseDSL.actionBase.moveAway import MoveAway
    from synthesis.baseDSL.actionBase.moveToUnit import MoveToUnit
    from synthesis.baseDSL.actionBase.train import Train
    
    from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy
    from synthesis.baseDSL.actionBase.attack import Attack
    from synthesis.baseDSL.mainBase.S import S, ChildS
    from synthesis.baseDSL.mainBase.for_S import For_S
    from synthesis.baseDSL.mainBase.c import C, ChildC

from abc import ABC, abstractmethod

class Factory(ABC):
    
    
    def build_S(self,childS : ChildS = None) -> S:
        raise Exception('Unimplemented method: build_S')
    
    
    def build_For_S(self,s : S= None) -> For_S:
        raise Exception('Unimplemented method: For_S')
    
   
    def build_C(self,childC : ChildC= None) -> C:
        raise Exception('Unimplemented method: build_C')
    

    def build_S_S(self,sL: S=None, sR: S=None) -> S_S:
        raise Exception('Unimplemented method: build_S_S')
    
    
    
    
    #actions
 
    def build_Attack(self,op : OpponentPolicy= None) -> Attack:
        raise Exception('Unimplemented method: Attack') 
    
    def build_AttackIfrange(self,) -> AttackIfrange:
        raise Exception('Unimplemented method: AttackIfrange')
    
  
    
    def build_Build(self,utype : Utype= None, direc:Direction= None, n: N= None) -> Build:
        raise Exception('Unimplemented method: Build')
    	
  
    
    def build_Harvest(self,n : N= None) -> Harvest:
        raise Exception('Unimplemented method: Harvest')
    
    def build_MoveAway(self,) -> MoveAway:
        raise Exception('Unimplemented method: MoveAway')

    def build_Empty(self,) -> Empty:
        raise Exception('Unimplemented method: Empty')

    def build_MoveToUnit(self,tp:TargetPlayer= None, op:OpponentPolicy= None) -> MoveToUnit:
        raise Exception('Unimplemented method: MoveToUnit')
	
    

    def build_Train(self, utype : Utype= None,  direc : Direction= None,  n : N= None) -> Train:
        raise Exception('Unimplemented method: Train')


	# AlmostTerminal
    
    
    def build_Utype(self,value : str= None) -> Utype:
        raise Exception('Unimplemented method: Utype')
    
 
    def build_N(self,value : str= None) -> N:
        raise Exception('Unimplemented method: N')
        
    
    def build_Direction(self,value : str= None) -> Direction:
        raise Exception('Unimplemented method: Direction')



    def build_TargetPlayer(self,value : str= None) -> TargetPlayer:
        raise Exception('Unimplemented method: Direction')
    

    def build_OpponentPolicy(self,value : str= None) -> OpponentPolicy:
        raise Exception('Unimplemented method: Direction')
    
    