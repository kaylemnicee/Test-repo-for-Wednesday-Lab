
from distutils.command import build
from Game.GameState import GameState
from Game.ResourceUsage import ResourceUsage
from Game.Unit import Unit
from Game.UnitAction import UnitAction
from nanobind_example2 import AStarPathFinding
import numpy as np
class AStarPathFindingCPP:

    


    def __init__(self, a_width:int,  height : int):
        self._pf = AStarPathFinding(a_width,height)
       
    
    
     
        

    #This fucntion finds the shortest path from 'start' to 'targetpos' and then returns
    # a UnitAction of the type 'actionType' with the direction of the first step in the shorteet path
    def findPath(self, start : Unit,  targetpos : int, gs: GameState,  ru: ResourceUsage)->UnitAction:
       return self.findPathToPositionInRange(start, targetpos, 0, gs);
    
    #This function is like the previous one, but doesn't try to reach 'target', but just to
    # reach a position that is at most 'range' far away from 'target'
    def findPathToPositionInRange(self, start:Unit,  targetpos : int,  rangev : int, gs : GameState)->UnitAction:
        x = start.getX()
        y = start.getY()
        r = self._pf.findPathToPositionInRange(x,y,targetpos,rangev,gs._free)
        
        if r == 0:return UnitAction.build_Move( UnitAction.DIRECTION_DOWN);
        if r == 1: return  UnitAction.build_Move( UnitAction.DIRECTION_LEFT);
        if r == 2: return  UnitAction.build_Move( UnitAction.DIRECTION_UP);
        if r == 3: return  UnitAction.build_Move( UnitAction.DIRECTION_RIGHT);
        else:  return UnitAction.build_None()
         
      

    #virtual Pair<Integer, Integer> findPathToPositionInRange2(Unit start, int targetpos, int range, GameState gs);


    
    # This function is like the previous one, but doesn't try to reach 'target', but just to
    # reach a position adjacent to 'target'
     
   
   

   

    def findPathToAdjacentPosition(self, start : Unit,  targetpos : Unit,  gs :GameState)->UnitAction:
        return self.findPathToPositionInRange(start, targetpos, 1, gs);