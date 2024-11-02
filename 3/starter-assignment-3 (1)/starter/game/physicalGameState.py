from __future__ import annotations

import xml.etree.ElementTree as ET

from game.unitType import UnitType


'''
 * The physical game state (the actual 'map') of a microRTS game
 *
 * @author santi
 */
'''

from game.player import Player
from game.unit import Unit
from game.unitTypeTable import UnitTypeTable
import numpy as np

class PhysicalGameState :
    
    #Indicates a free tile
    TERRAIN_NONE =0

    #Indicates a blocked tile
    TERRAIN_WALL=1
    @staticmethod
    def getTERRAIN_WALL():
        return PhysicalGameState.TERRAIN_WALL

    def __init__(self,width:int=8,height:int=8,terrain =None):
        self._width :int  = width
        self._height : int  = height
        #self._terrain = np.zeros((self._pgs.getWidth(), self._pgs.getHeight()), dtype=np.int8)
        self._terrain  = terrain
        self._players : list[Player] = []
        self._units :dict[int,Unit]= {}
   

    def clone(self):
        Unit.next_ID = 1224
        w = self._width
        h = self._height
        terrain = np.zeros((w, h), dtype=np.int8)
        for t in range(w*h):
            terrain[int(t/w)][int(t%w)]= self._terrain[int(t/w)][int(t%w)]
        
        pgs = PhysicalGameState(w,h,terrain)  
        for p in self._players:
            pgs._players.append(Player(p.getID(), p.getResources()))
        for u2 in self._units.values():
            u = u2.clone()
            pgs.addUnit(u)
        return pgs
            
        
       
        
    
    #Constructs the game state map from a XML
    @staticmethod
    def load( fileName:str, utt:UnitTypeTable)->PhysicalGameState:
        tree = ET.parse(fileName)
        root = tree.getroot()
        return PhysicalGameState.fromXML(root,utt)
       
    def createUnit(self,   a_player :int , a_type: UnitType ,  a_x: int ,  a_y:int ,  a_resources : int):
        
        return Unit(None,a_player,a_type,a_x,a_y,a_resources)
        
    
    def getWidth(self) -> int:
        return self._width       

    def getHeight(self)->int:
        return self._height        

  
    #Sets a new width. This do not change the terrain array, remember to
    #change that when you change the map width or height
    def  setWidth(self, w:int)->None:
        self._width =w    

    #Sets a new height. This do not change the terrain array, remember to
    #change that when you change the map width or height
    def setHeight(self, h:int)->None:
        self._height =h    

    #Returns what is on a given position of the terrain
    def getTerrain(self, x:int,  y:int)->int:
        return self._terrain[x][y]   


    # Puts an entity in a given position of the terrain
    #def setTerrain(self, x:int,  y:int,  v:int)->None:

    #Sets the whole terrain
    def setTerrain(self, t : list[int])->None:
        self._terrain = t    

    
    #Adds a player
    def addPlayer(self, p:Player)->None:
        self._players.append(p)    

        
    #Adds a new {@link Unit} to the map if its position is free
    def addUnit(self, newUnit :Unit)->None:
        self._units[newUnit.getID()]=  newUnit

    #Removes a unit from the map
    def removeUnit(self,u:Unit)->None:
        self._units.pop(u.getID())    
    

    #Returns the list of units in the map
    def getUnits(self) ->dict[int,Unit]: #->map[Unit]
        return self._units    

    #Returns a list of players
    def getPlayers(self)->list[Player]:
        return self._players         

    #Returns a player given its ID
    def getPlayer(self, pID:int)->Player:
        return self._players[pID]    

    #Returns a {@link Unit} given its ID or null if not found
    def getUnit(self, ID:int)->Unit:
        return self._units[ID] if ID in self._units else None

    #Returns the {@link Unit} at a given coordinate or null if no unit is
    #present
    def getUnitAt(self, x:int,  y:int)->Unit:
        for u  in self._units.values():
            if u.getX() == x and u.getY() == y:
                return u
        return None;    

       


    #Returns the winner of the game, given the unit counts or -1 if the game
    def  winner(self)->int:
        unitcounts = [0,0] 
        totalunits = 0;
        for  u in self._units.values():
            
            if u.getPlayer() >= 0: 
                unitcounts[u.getPlayer()]+=1
            
        winner = -1;
        for i in range(2):
            if unitcounts[i] > 0:
                if winner == -1:
                    winner = i;
                else :
                    return -1
        return winner   


    #Returns whether the game is over. The game is over when a player has zero
    # units
    def gameover(self)->bool:
        unitcounts = [0,0] 
        totalunits = 0;
        for  u in self._units.values():
            if u.getPlayer() >= 0: 
                unitcounts[u.getPlayer()]+=1
                totalunits+=1
        

        if totalunits == 0:
            return True
        

        winner = -1;
        for i in range(2):
            if unitcounts[i] > 0:
                if winner == -1:
                    winner = i;
                else :
                    return False;

        return winner != -1;    


   
    #Constructs a map from XML
    @staticmethod
    def fromXML(root, utt)->PhysicalGameState:
        w = int(root.attrib["width"])
        h  = int(root.attrib["height"])
  
        terrain_s = root[0].text
        terrain = np.zeros((w, h), dtype=np.int8)
        for t in range(len(terrain_s)):
            terrain[int(t/w)][int(t%w)]= np.int8(int(terrain_s[t]))
        
        pgs = PhysicalGameState(w,h,terrain)  
        for p in root[1]:
            player = Player.fromXML(p) 
          
            pgs.addPlayer(player)  
        for u in root[2]:
            unit = Unit.fromXML(u,utt)    
            pgs.addUnit(unit)
            
        return pgs   

 