


from ai.rush.CombatRush import CombatRush
from evaluators.SimpleSqrtEvaluationFunction3MultiState import SimpleSqrtEvaluationFunction3MultiState
from game.gameState import GameState
from game.physicalGameState import PhysicalGameState
from game.unitTypeTable import UnitTypeTable
from playout.simpleMatch import SimpleMatch


class TestSimpleSqrtEvaluationFunction3MultiState:
    
    @staticmethod
    def simpleTests():
        eval = SimpleSqrtEvaluationFunction3MultiState()
        map = "./maps/basesWorkers32x32A.xml"
        utt = UnitTypeTable(2)
        pgs = PhysicalGameState.load(map,utt)
        gs = GameState(pgs,utt)
        ai0 = CombatRush(pgs,utt,"Light")
        ai1 = CombatRush(pgs,utt,"Heavy")
        sm = SimpleMatch()
        
        win, auxiliary_score = sm.playout(gs,ai0,ai1,1,3000,False,eval)
        print("analyzing score for ai0 as player 1")
        print("win = ",win,"auxiliary_score",auxiliary_score)
        print("analyzing score for ai1 as player 0")
        win, auxiliary_score = sm.playout(gs,ai1,ai0,0,3000,False,eval)
        print("win = ",win,"auxiliary_score",auxiliary_score)
        