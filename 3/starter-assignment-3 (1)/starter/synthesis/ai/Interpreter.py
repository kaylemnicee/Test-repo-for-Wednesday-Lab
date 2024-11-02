from __future__  import annotations
from typing import TYPE_CHECKING
from game.gameState import GameState
from game.physicalGameState import PhysicalGameState
from game.player import Player
from game.playerAction import PlayerAction
from game.unit import Unit
from game.unitType import UnitType
from game.unitTypeTable import UnitTypeTable
from ai.abstraction.Build import Build
from ai.abstraction.Harvest import Harvest
from ai.abstraction.Train import Train
from ai.ai import AI

from synthesis.ai.Memory import Memory









if TYPE_CHECKING:
   from synthesis.baseDSL.mainBase.node import Node





from ai.abstraction.AbstractionLayerAI import AbstractionLayerAI



class Interpreter(AI):
    
    def __init__(self,pgs : PhysicalGameState, utt : UnitTypeTable, n : Node) -> None:
        self._n : Node = n
        self._utt : UnitTypeTable = utt
        self._core  : AbstractionLayerAI= AbstractionLayerAI(pgs)
        self.resource :int = None
        
    def reset(self):
        self._core.reset()
        
    def getActions(self,  gs:GameState, player:int) -> PlayerAction:
        self.resource = gs.getPlayer(player).getResources()
        ru = gs.getResourceUsage()
        self.resource -=  ru.getResourcesUsed(player)
        self._core.clear(gs)
        self._memory = Memory(gs,player,self)
        self._n.interpret(gs, player,None, self)
        pa = self._core.translateActions(player, gs)
        #print(gs.getTime())
        #for a in pa.getActions().values():
        #    print(a[0].toString(),a[1].toString())
        return pa
        
    def  farthestAllyBase(self, pgs: PhysicalGameState, player: int,  unitAlly : Unit) ->Unit :
        farthestBase = None
        farthesttDistance = 0
        for  u2 in pgs.getUnits().values():

                if (u2.getPlayer() >= 0 and u2.getPlayer() == player) :
                    d = abs(u2.getX() - unitAlly.getX()) + abs(u2.getY() - unitAlly.getY());
                    if farthestBase == None or d > farthesttDistance:
                        farthestBase = u2
                        farthesttDistance = d
     
        return farthestBase
        
    def countHarvester(self, player:int,  gs:GameState):
        pgs = gs.getPhysicalGameState()
        cont =0
        for u2 in pgs.getUnits().values():
            if player != u2.getPlayer():
                continue
            a2 = self._core.getAbstractAction(u2)
            if isinstance(a2 , Harvest) :
                cont+=1

        return cont
        
        
        
        
    def countUnit(self,type, player:int,  gs:GameState):
        count =0
        pgs = gs.getPhysicalGameState()
        for u2 in pgs.getUnits().values():
            if player != u2.getPlayer():
                continue
            if  u2.getType().getName() == type:
                count+=1
        return count
    
    def countConstrution(self,typeU, player:int,  gs:GameState):
        cont=0
        pgs = gs.getPhysicalGameState()
        for u2 in pgs.getUnits().values():
            if player != u2.getPlayer():
                continue
            if u2.getType().getName() == typeU:
                cont+=1
            elif u2.getType().getName() == "Worker":
                a2 = self._core.getAbstractAction(u2)
                aux=False
                
                if  isinstance(a2,Build)  :
                    
                    if a2._type.getName()==typeU:
                        aux=True	
                if aux:
                    cont+=1
        return cont
    
    
    
    def countTrain(self,typeU, player:int,  gs:GameState):
        cont=0
        pgs = gs.getPhysicalGameState()
        for u2 in pgs.getUnits().values():
            if player != u2.getPlayer():
                continue
           
            if u2.getType().getName() == typeU:
                
                cont+=1
                #print("cont++",cont,u2.toString())
            elif u2.getType().getName() == "Barracks" or u2.getType().getName() == "Base":
                a2 = self._core.getAbstractAction(u2)
                aux=False
                
                if  isinstance(a2,Train)  :
                    
                    if a2._type.getName()==typeU:
                        aux=True
                        
                            
                if aux:
                    cont+=1
        return cont
    
                
    def getUnitClosest(self,gs : GameState, p : Player, u : Unit) -> Unit:
        pgs = gs.getPhysicalGameState()
        closestEnemy = None
        closestDistance = 0
        for  u2 in pgs.getUnits().values():
            if  1-p.getID() == u2.getPlayer()and u.getID() != u2.getID():
                d = abs(u2.getX() - u.getX()) + abs(u2.getY() - u.getY())
                if closestEnemy == None or d < closestDistance:
                    closestEnemy = u2
                    closestDistance = d
                
        return closestEnemy
    
    def getUnitFarthest(self,gs : GameState, p : Player, u : Unit) -> Unit:
        pgs = gs.getPhysicalGameState()
        FarthestEnemy = None
        FarthestDistance = 1000000
        for u2 in pgs.getUnits().values():
            if  1-p.getID() == u2.getPlayer()and u.getID() != u2.getID():
                d = abs(u2.getX() - u.getX()) + abs(u2.getY() - u.getY())
                if FarthestEnemy == None or d > FarthestDistance:
                    FarthestEnemy = u2
                    FarthestDistance = d
        return FarthestEnemy
	
    def getUnitLessHealthy(self,gs : GameState, p : Player, u : Unit) -> Unit:
    
        pgs = gs.getPhysicalGameState()
        closestHealthy = None
        closestDistance = 0
        Healthy = 10000
        
        for   u2 in pgs.getUnits().values():
            if    1-p.getID() == u2.getPlayer()and u.getPlayer() == u2.getPlayer():
                d = abs(u2.getX() - u.getX()) + abs(u2.getY() - u.getY())
                if closestHealthy == None  or  Healthy > u2.getMaxHitPoints():
                    Healthy = u2.getMaxHitPoints()
                    closestHealthy = u2
                    closestDistance =d
                elif Healthy == u2.getMaxHitPoints() :
	            	
                    if closestHealthy == None or d < closestDistance:
                        Healthy = u2.getMaxHitPoints()
                        closestHealthy = u2
                        closestDistance =d
        return closestHealthy   
	
 
    def getUnitStrongest(self,gs : GameState, p : Player, u : Unit) -> Unit:
    
        pgs = gs.getPhysicalGameState()
        closestStrongest = None
        closestDistance = 0
        Strongest = -1
        
        
        for  u2 in pgs.getUnits().values():
            if  1-p.getID() == u2.getPlayer() and u.getID() != u2.getID():
                d = abs(u2.getX() - u.getX()) + abs(u2.getY() - u.getY())
                if closestStrongest == None or Strongest < u2.getMaxDamage():
                    Strongest = u2.getMaxDamage()
                    closestStrongest = u2
                    closestDistance =d
            	
                elif Strongest == u2.getMaxDamage():
	            	
                    if (closestStrongest == None or d < closestDistance) :
                        closestStrongest = u2
                        closestDistance = d
                        Strongest = u2.getMaxDamage()
	                
         
        return closestStrongest
	
 
 
    def getUnitMostHealthy(self,gs : GameState, p : Player, u : Unit) -> Unit:
    
        pgs = gs.getPhysicalGameState()
        closestHealthy = None
        closestDistance = 0
        Healthy = 0
    
        for  u2 in pgs.getUnits().values() :
            if  1-p.getID() == u2.getPlayer()and u.getID() != u2.getID():
                d = abs(u2.getX() - u.getX()) + abs(u2.getY() - u.getY())
                if closestHealthy == None or Healthy < u2.getMaxHitPoints():
                    Healthy = u2.getMaxHitPoints()
                    closestHealthy = u2
                    closestDistance =d
                elif Healthy == u2.getMaxHitPoints() :
                    if (closestHealthy == None or d < closestDistance) :
                        Healthy = u2.getMaxHitPoints()
                        closestHealthy = u2
                        closestDistance =d
	                
        return closestHealthy
    
    
    def getUnitWeakest(self,gs : GameState, p : Player, u : Unit) -> Unit:
        pgs = gs.getPhysicalGameState()
        closestWeakest = None
        closestDistance = 0
        Weakest = 10000
        
        
        for  u2 in pgs.getUnits().values(): 
            if  1-p.getID() == u2.getPlayer()and u.getID() != u2.getID():
                d = abs(u2.getX() - u.getX()) + abs(u2.getY() - u.getY())
                if closestWeakest == None or Weakest > u2.getMaxDamage():
                    Weakest = u2.getMaxDamage()
                    closestWeakest = u2
                    closestDistance =d
                elif Weakest == u2.getMaxDamage():
                    if closestWeakest == None or d < closestDistance:
                        closestWeakest = u2
                        closestDistance = d
                        Weakest = u2.getMaxDamage()
	      
        return closestWeakest
	
    
    def behaveBase(self,u:Unit, player:int,  gs:GameState):
        nW=self.countUnit("Worker",player,gs)
        if nW < 2 and self.resource >=self.workerType.cost:
            self._core.train(u,self.workerType)
        
    def behaveWr(self,u:Unit, player:int,  gs:GameState):
        
        nBr = self.countConstrution("Barracks",player,gs)
        p = gs.getPlayer(player)
        reservedPositions = []
        pgs = gs.getPhysicalGameState()
        
        if self._core.getAbstractAction(u)==None and nBr <1:
            r = self._core.buildIfNotAlreadyBuilding(u,self.barracksType,u.getX(),u.getY(),reservedPositions,p,pgs)
            
        
  