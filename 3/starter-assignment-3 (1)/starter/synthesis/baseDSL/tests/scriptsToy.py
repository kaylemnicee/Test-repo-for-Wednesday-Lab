


from synthesis.baseDSL.almostTerminal.direction import Direction
from synthesis.baseDSL.almostTerminal.n import N
from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy
from synthesis.baseDSL.almostTerminal.targetPlayer import TargetPlayer
from synthesis.baseDSL.almostTerminal.utype import Utype
from synthesis.baseDSL.actionBase.attack import Attack
from synthesis.baseDSL.actionBase.build import Build
from synthesis.baseDSL.actionBase.harvest import Harvest
from synthesis.baseDSL.actionBase.AttackIfrange import AttackIfrange
from synthesis.baseDSL.actionBase.moveToUnit import MoveToUnit
from synthesis.baseDSL.actionBase.train import Train
from synthesis.baseDSL.mainBase.c import C
from synthesis.baseDSL.mainBase.S import S
from synthesis.baseDSL.mainBase.empty import Empty
from synthesis.baseDSL.mainBase.s_s import S_S
from synthesis.baseDSL.mainBase.for_S import For_S
from synthesis.baseDSL.mainBase.node import Node


class ScriptsToy(object):
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def scriptEmpty() ->Node:
        emp  = Empty()
        return S(emp)

    @staticmethod
    def script0() ->Node:
        op = OpponentPolicy("LessHealthy")
        attack = Attack(op)
        c = C(attack)
        for_s = For_S(S(c))
        return S(for_s)
    
    @staticmethod
    def script1() ->Node:
        op = OpponentPolicy("Closest")
        attack = Attack(op)
        c = C(attack)
        c1= C(Build(Utype("Barracks"),N("3"),Direction("Up")))
        for_s = For_S(
                S(S_S(
                    S(c1),
                    S(c)
                    )
                ))
        return S(for_s)    
    
    @staticmethod
    def script2() ->Node:
        c1 = S(C(Attack(OpponentPolicy("Closest"))))
        c2 = S(C(Build(Utype("Barracks"),N("1"),Direction("Up"))))
        c3 = S(C(Train(Utype("Ranged"),N("3"),Direction("Left"))))
        ss1 = S(S_S(c3,c2))
        ss2 = S(S_S(ss1,c1))
        for_s = For_S(ss2)
        return S(for_s)  
    
    @staticmethod
    def script3() ->Node:
        c1 = S(C(Attack(OpponentPolicy("Closest"))))
        c2 = S(C(Build(Utype("Barracks"),N("1"),Direction("Up"))))
        c3 = S(C(Train(Utype("Ranged"),N("3"),Direction("Left"))))
        c4 = S(C(Harvest(N("2"))))
        ss1 = S(S_S(c3,c2))
        ss2 = S(S_S(c4,c1))
        ss3 = S(S_S(ss1,ss2))
        for_s = For_S(ss3)
        return S(for_s)  
    
    @staticmethod
    def script6() ->Node:
        c1 = S(C(Attack(OpponentPolicy("Closest"))))
        c2 = S(C(Build(Utype("Barracks"),N("1"),Direction("Up"))))
        c3 = S(C(Train(Utype("Worker"),N("4"),Direction("Left"))))
        c4 = S(C(Harvest(N("2"))))
        ss1 = S(S_S(c3,c2))
        ss2 = S(S_S(c4,c1))
        ss3 = S(S_S(ss1,ss2))
        for_s = For_S(ss3)
        return S(for_s)  
    
    @staticmethod
    def script7() ->Node:
        c1 = S(C(Train(Utype("Worker"),N("10"),Direction("Left"))))
        c2 = S(C(Harvest(N("3"))))
        c3 = S(C(Attack(OpponentPolicy("Weakest"))))
        c4 = S(C(Harvest(N("10"))))
        c5 = S(C(Attack(OpponentPolicy("Farthest"))))
       
        ss1 = S(S_S(c1,c2))
        ss2 = S(S_S(c3,c4))
        ss3 = S(S_S(ss1,ss2))
        ss4 = S(S_S(ss3,c5))
        for_s = For_S(ss4)
        return S(for_s)  
    
    
    @staticmethod
    def script4() ->Node:
        c1 = S(C(MoveToUnit(OpponentPolicy("Closest"),TargetPlayer("Enemy"))))
        c2 = S(C(Build(Utype("Barracks"),N("1"),Direction("Up"))))
        c3 = S(C(Train(Utype("Worker"),N("4"),Direction("Left"))))
        c4 = S(C(Harvest(N("2"))))
        ss1 = S(S_S(c3,c2))
        ss2 = S(S_S(c4,c1))
        ss3 = S(S_S(ss1,ss2))
        for_s = For_S(ss3)
        return S(for_s)  
    
    
    @staticmethod
    def script5() ->Node:
        c1 = S(C(MoveToUnit(OpponentPolicy("Closest"),TargetPlayer("Enemy"))))
        c2 = S(C(Build(Utype("Barracks"),N("1"),Direction("Up"))))
        c3 = S(C(Train(Utype("Worker"),N("4"),Direction("Left"))))
        c4 = S(C(Harvest(N("2"))))
        c5 = S(C(AttackIfrange()))
        ss1 = S(S_S(c3,c2))
        ss2 = S(S_S(c4,c1))
        ss3 = S(S_S(ss1,ss2))
        for_s = For_S(S(S_S(c5,ss3)))
        return S(for_s)  
    
    @staticmethod
    def script8() ->Node:
        c10 = S(C(MoveToUnit(OpponentPolicy("Closest"),TargetPlayer("Enemy"))))
        c11 = S(C(MoveToUnit(OpponentPolicy("Closest"),TargetPlayer("Enemy"))))
        c1 = S(S_S(c10,c11))
        c20 = S(C(Build(Utype("Heavy"),N("7"),Direction("Up"))))
        c21 = S(C(Build(Utype("Ranged"),N("2"),Direction("Up"))))
        c2 = S(S_S(c20,c21))
        c3 = S(C(Train(Utype("Worker"),N("2"),Direction("Left"))))
        c4 = S(C(Harvest(N("2"))))
        c50 = S(C(AttackIfrange()))
        c51 = S(C(Attack(OpponentPolicy("Weakest"))))
        c5 = S(S_S(c50,c51))
        ss1 = S(S_S(c3,c2))
        ss2 = S(S_S(c4,c1))
        ss3 = S(S_S(ss1,ss2))
        for_s = For_S(S(S_S(c5,ss3)))
        return S(for_s)  