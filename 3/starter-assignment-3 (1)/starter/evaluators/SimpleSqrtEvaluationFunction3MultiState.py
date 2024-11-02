

import math
from evaluators.evaluator import Evaluator
from game.gameState import GameState

from game.physicalGameState import PhysicalGameState


class SimpleSqrtEvaluationFunction3MultiState(Evaluator): 
    
    def __init__(self):
        self.scoreByState :list[float]= []
        self.RESOURCE : float= 20
        self.RESOURCE_IN_WORKER : float= 10
        self.UNIT_BONUS_MULTIPLIER : float= 40.0
   
    def analysis(self,gs : GameState, player:int,lastState: bool)->None:
        s1 : float = self.base_score(player,gs)
        s2 : float =self.base_score(1-player,gs)
        if s1 + s2 == 0: return 0.5
        score = (2*s1 / (s1 + s2))-1
        self.scoreByState.append(score)
    
    def base_score(self, player:int,  gs:GameState)->float:
        pgs : PhysicalGameState = gs.getPhysicalGameState()
        score :float  = gs.getPlayer(player).getResources()*self.RESOURCE
        anyunit : bool= False
        for u  in pgs.getUnits().values():
            if u.getPlayer()==player:
                anyunit = True
                score += u.getResources() * self.RESOURCE_IN_WORKER
                score += self.UNIT_BONUS_MULTIPLIER * u.getCost()*math.sqrt( u.getHitPoints()/u.getMaxHitPoints() );
  
        if not anyunit: return 0
        return score
    

    def getValue(self)->float:
        return sum(self.scoreByState)/len(self.scoreByState)
    
    def reset(self)->None:
        self.scoreByState.clear()