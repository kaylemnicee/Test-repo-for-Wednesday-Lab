
from game.unitTypeTable import  UnitTypeTable
from game.physicalGameState import PhysicalGameState
from game.unitType import UnitType
from game.gameState import GameState
from game.playerAction import PlayerAction
from game.unitAction import UnitAction
from game.unit import Unit
from game.unitActionAssignment import UnitActionAssignment
from game.AStarPathFinding import AStarPathFinding
from game.player import Player
from game.resourceUsage import ResourceUsage



from .Move import Move
from .Train import Train
from .Build import Build
from .Attack import Attack
from .AttackIfrange import AttackIfrange
from .Harvest import Harvest

import time

class AbstractionLayerAI:
    VERIFY_ACTION_CORRECTNESS = False;
    def __init__(self, pgs : PhysicalGameState):
        self._actions = {}
        self._tt0=0
        self._tt1=0
        self._tt2=0
        self._tt3=0
        self._tt4=0
        
        self._pf = AStarPathFinding(pgs.getWidth(), pgs.getHeight())
    # In case the GameState is cloned, and the Unit pointers in the "actions" map change, this variable
    # saves a pointer to the previous GameState, if it's different than the current one, then we need to find a mapping
    # between the old units and the new ones
        self.lastGameState = None
        
    def reset(self):
        self._actions.clear()
        
    def clear(self,gs : GameState):
            # print(self._actions)
            # ini = time.time()
            pgs = gs.getPhysicalGameState()
            toSalve = []
            for a in self._actions.items():
                if None == gs.getActionAssignment(a[0]) or \
                        pgs.getUnit(a[0].getID())==None:
                    pass
                else:
                    toSalve.append((a[0],a[1]))
            #for u in toDelete:
            #     self._actions.pop(u)
            self._actions.clear()
            for u in toSalve:
                self._actions[u[0]]=u[1]
    
    def translateActions(self, player : int,  gs : GameState) :
        pgs = gs.getPhysicalGameState()
        pa =  PlayerAction()
        desires = []
        
        #self._lastGameState = gs;
        
        # Execute abstract actions:
        toDelete = []
        ru =  ResourceUsage();
        inicio = time.time()
        for  aa in self._actions.values():
            if  pgs.getUnit(aa.getUnit().getID())==None:
                # The unit is dead:
                toDelete.append(aa._unit)
            else :
                if aa.completed(gs):
                    toDelete.append(aa._unit);
                else :
                    if gs.getActionAssignment(aa._unit) == None:
                        inicio = time.time()
                        ua = aa.execute(gs, ru)
                        fim = time.time()     
                        self._tt1+=fim - inicio 
                        if ua != None:
                            if AbstractionLayerAI.VERIFY_ACTION_CORRECTNESS and False:
                                pass
                                # verify that the action is actually feasible:
                                #ual = aa._unit.getUnitActions(gs);
                                #if ua in ual:
                                #    desires.append((aa._unit, ua))
                                
                            else :
                                desires.append([aa._unit, ua])
                               
                            ru.merge(ua.resourceUsage(aa._unit, pgs))
        
        fim = time.time()     
        self._tt0+=fim - inicio 
        
        for  u in toDelete:
            self._actions.pop(u);
        
        
        # compose desires:
        inicio = time.time()
        r = gs.getResourceUsage();
       
        pa.setResourceUsage(r);
        
        for  desire in desires:
            r2 = desire[1].resourceUsage(desire[0], pgs)
            if pa.consistentWith(r2, gs):
                pa.addUnitAction(desire[0], desire[1])
                pa.getResourceUsage().merge(r2)
        
        #pa.fillWithNones(gs, player, 10)
        fim = time.time()     
        self._tt2+=fim - inicio 
  
        return pa
    
    def getAbstractAction(self, u : Unit) :
        if u in self._actions:
            return self._actions[u]
        else:
            None
   

    def move(self, u : Unit, x : int,  y : int):
        self._actions[u] = Move(u, x, y, self._pf)
    

    def train(self, u : Unit,  unit_type : UnitType) :
        self._actions[u] = Train(u, unit_type)
        
    

    def train(self, u : Unit, unit_type : UnitType, preference : int= None) -> None:
        self._actions[u] = Train(u, unit_type, preference)
       
    
    
    def build(self,  u : Unit,  unit_type : UnitType, x : int,  y : int) -> None:
        self._actions[u] = Build(u, unit_type, x, y, self._pf)
       # actions.put(u, new Build(u, unit_type, x, y, pf));
    

    def harvest(self, u : Unit,  target : Unit,  base : Unit) -> None:
        self._actions[u] = Harvest(u, target, base, self._pf)
        #actions.put(u, new Harvest(u, target, base, pf));
    

    def attack(self, u : Unit, target : Unit) -> None:
        self._actions[u] = Attack(u, target, self._pf)
        

    def AttackIfrange(self, u : Unit) :
        self._actions[u] = AttackIfrange(u)

    def findBuildingPosition(self, reserved : list[int], desiredX : int, desiredY : int, p : Player, gs : GameState) -> int:
        
        x = -1
        y = -1
        pgs = gs.getPhysicalGameState()

     
        
        for l in range(1,max(pgs.getHeight(), pgs.getWidth())):
            for side in range(4):
                
                    if side == 0:#up
                        y = desiredY - l;
                        if y < 0 :
                            continue;
                        
                        for dx in range(-l,l+1):
                            x = desiredX + dx;
                            if x < 0 or x >= pgs.getWidth():
                                continue;
                            pos = x + y * pgs.getWidth();
                            if not pos in reserved and gs.free(x,y) :
                                return pos;
                           
                        
                    elif side == 1:#right
                        x = desiredX + l;
                        if x >= pgs.getWidth():
                            continue;
                        
                        for dy in range(-l,l+1):
                            y = desiredY + dy;
                            if y < 0 or y >= pgs.getHeight():
                                continue;
                            pos = x + y * pgs.getWidth();
                            if (not pos in reserved) and gs.free(x,y): 
                                return pos;
                            
                        
                    elif side == 2:#down
                        y = desiredY + l
                        if y >= pgs.getHeight():
                            continue
                        
                        for dx in range(-l,l+1):
                            x = desiredX + dx;
                            if x < 0 or x >= pgs.getWidth() :
                                continue;
                            
                            pos = x + y * pgs.getWidth();
                            if (not pos in reserved) and gs.free(x,y): 
                                return pos
                       
                    elif side== 3:#left
                        x = desiredX - l;
                        if x < 0: 
                            continue;
                      
                        for dy in range(-l,l+1):
                            y = desiredY + dy;
                            if y < 0 or y >= pgs.getHeight():
                                continue;
                            
                            pos = x + y * pgs.getWidth();
                            if (not pos in reserved) and gs.free(x,y):
                                return pos;
                     
        return -1;

    def buildIfNotAlreadyBuilding(self,  u : Unit,  utype : UnitType,  desiredX : int,  desiredY : int, reservedPositions : list[int],  p : Player,  gs : GameState) -> bool: 
        action = self.getAbstractAction(u);
#        System.out.println("buildIfNotAlreadyBuilding: action = " + action);
        pgs = gs.getPhysicalGameState()
        if not isinstance(action , Build) or action._type != utype :
            
            pos = self.findBuildingPosition(reservedPositions, desiredX, desiredY, p, gs);
           
    #           System.out.println("pos = " + (pos % pgs.getWidth()) + "," + (pos / pgs.getWidth()));
            
            self.build(u, utype, pos % pgs.getWidth(), pos // pgs.getWidth());#strange
           
            reservedPositions.append(pos);
            return True;
        else :
            return False;
        
