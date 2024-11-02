from __future__ import annotations
from typing import TYPE_CHECKING
from game.unitAction import UnitAction

from game.unitType import UnitType
if TYPE_CHECKING:
    from game.gameState import GameState
    
    from game.physicalGameState import PhysicalGameState
    
    
    

class Unit:
    next_ID =0
    
    def __init__(self, a_ID : int = None,  a_player :int  = None, a_type: UnitType = None,  a_x: int = None,  a_y:int = None,  a_resources : int =None) -> None:
        if a_ID == None:
            Unit.next_ID+=1
            a_ID = Unit.next_ID
        elif a_ID >= Unit.next_ID:
             Unit.next_ID = a_ID+1
        if a_player == None:a_player=-1
        if a_x == None : a_x=-1
        if a_y == None : a_y=-1
        if a_resources == None: a_resources=-1;
        self._ID = a_ID
        self._player = a_player
        self._x = a_x
        self._y = a_y
        self._resources = a_resources
        self._type = a_type
        self._hitpoints = a_type._hp 
        
    def clone(self):
        return Unit(self._ID,self._player, self._type,self._x,self._y,self._resources )    
        
    def __hash__(self):
        return int.__hash__(self._ID)

    #Returns the owner ID
    def getPlayer(self)->int:
        return self._player

    #Returns the type
    def getType(self)->UnitType:
        return self._type
    
    '''
         * Sets the type of this unit.
         * Note: this should not be done lightly. It is currently thought to be used
         * only when the GUI changes the unit type table, and tries to create a clone
         * of the current game state, but changing the UTT.
         * @param a_type
    '''
    def setType(self, a_type : UnitType)->None:
        self._type = a_type    

    
    #Returns the unique identifier
    def getID(self)->int:
        return self._ID

    '''
         * Changes the unique identifier
         * Note: Do not use this function unless you know what you are doing!
         * @param a_ID
    '''
    def setID(self, a_ID:int)->None:
        self._ID = a_ID
        
    '''
         * Returns the index of this unit in a {@link PhysicalGameState}
         * (as it is an 'unrolled matrix')
         * @param pgs
         * @return  
    '''
    #int getPosition(PhysicalGameState &pgs);
    
   
    #Returns the x coordinate
    def getX(self) -> int:
        return self._x    

    #Returns the y coordinate
    def getY(self) -> int:
        return self._y

    #Sets x coordinate
    def setX(self, a_x : int) -> None:
        self._x  = a_x   

    def setY(self, a_y : int) -> None:
        self._y = a_y   
   

    #Returns the amount of resources this unit is carrying
    def getResources(self) -> int:
        return self._resources    

    #Sets the amount of resources the unit is carrying
    def setResources(self, a_resources : int) -> None:
        self._resources = a_resources    
        

    #Returns the current HP
    def getHitPoints(self)->int:
        return self._hitpoints

     # Returns the maximum HP this unit could have
    def getMaxHitPoints(self) -> int:
        return self._type._hp    

    #Sets the amount of HP
    def setHitPoints(self, a_hitpoints :int)->None:
        self._hitpoints = a_hitpoints    

    #The cost to produce this unit
    def getCost(self) -> int:
        return self._type._cost  

    #The time this unit gets to move
    def getMoveTime(self)->int:
        return self._type._moveTime    

    #The time it takes to perform an attack
    def getAttackTime(self)->int:
        return self._type._attackTime    

    #Returns the attack range
    def getAttackRange(self) -> int:
        return self._type._attackRange    

    #Returns the minimum damage this unit's attack inflict
    def getMinDamage(self) -> int:
        return self._type._minDamage    

     
    #Returns the maximum damage this unit's attack inflict
    def getMaxDamage(self)->int:
        return self._type._maxDamage    

    #Returns the amount of resources this unit can harvest
    def getHarvestAmount(self)->int:
        return self._type._harvestAmount  

    #The time it takes to harvest
    def getHarvestTime(self) -> int:
        return self._type._harvestTime    

    #Returns a list of actions this unit can perform in a given game state.
    #vector<UnitAction>* getUnitActions(GameState& s);
    def getUnitActions(self, s : GameState):
        return self.getUnitActionsINT(s, 10);
    '''
    * Returns a list of actions this unit can perform in a given game state.
    * An idle action for noneDuration cycles is always generated
    * @param s
    * @param noneDuration the amount of cycles for the idle action that is always generated
    * @return
    ''' 
    def getUnitActionsINT(self, s : GameState, noneDuration:int)->list[UnitAction]:
        pgs = s.getPhysicalGameState()
        p = pgs.getPlayer(self._player)
        l : list[UnitAction]= []
        #retrieves units around me
        uup : Unit =None
        uright : Unit =None
        udown : Unit =None
        uleft : Unit =None
       
        for u in pgs.getUnits().values():
            if u._x == self._x:
                if u._y == self._y - 1:
                    uup = u
                elif u._y == self._y + 1:
                    udown = u
            else:
                if u._y == self._y:
                    if u._x == self._x - 1:
                        uleft = u
                    elif u._x == self._x + 1:
                        uright = u;
                    
        #if this unit can attack, adds an attack action for each unit around it
        if self._type._canAttack:
            if self._type._attackRange == 1:

                if self._y > 0 and uup != None and uup._player != self._player and uup._player >= 0: l.append( UnitAction.build_Attack( uup._x, uup._y))
                if self._x < pgs.getWidth() - 1 and uright != None and uright._player != self._player and uright._player >= 0: l.append( UnitAction.build_Attack( uright._x, uright._y));
                if self._y < pgs.getHeight() - 1 and udown != None and udown._player != self._player and udown._player >= 0: l.append( UnitAction.build_Attack( udown._x, udown._y));
                if self._x > 0 and uleft != None and uleft._player != self._player and uleft._player >= 0: l.append( UnitAction.build_Attack( uleft._x, uleft._y));
            else :
                sqrange = self._type._attackRange * self._type._attackRange;
                for u in pgs.getUnits().values():
                    if u._player < 0 or u._player == self._player: continue;
                    sq_dx = (u._x - self._x) * (u._x - self._x);
                    sq_dy = (u._y - self._y) * (u._y - self._y);
                    if sq_dx + sq_dy <= sqrange:
                   
                        l.append( UnitAction.build_Attack( u.getX(), u.getY()));

 
        # if this unit can harvest, adds a harvest action for each resource around it
        # if it is already carrying resources, adds a return action for each allied base around it
        if self._type._canHarvest :
            #harvest:
     
            if self._resources == 0:
                if self._y > 0 and uup != None and uup._type._isResource: l.append( UnitAction.build_Haverst( UnitAction.DIRECTION_UP));
                if self._x < pgs.getWidth() - 1 and uright != None and uright._type._isResource: l.append( UnitAction.build_Haverst( UnitAction.DIRECTION_RIGHT));
                if self._y < pgs.getHeight() - 1 and udown != None and udown._type._isResource: l.append( UnitAction.build_Haverst( UnitAction.DIRECTION_DOWN));
                if self._x > 0 and uleft != None and uleft._type._isResource: l.append( UnitAction.build_Haverst( UnitAction.DIRECTION_LEFT));

            # return:
        
            if self._resources > 0:
                if self._y > 0 and uup != None and uup._type._isStockpile and uup._player == self._player: l.append( UnitAction.build_Return( UnitAction.DIRECTION_UP));
                if self._x < pgs.getWidth() - 1 and uright != None and uright._type._isStockpile and uright._player == self._player: l.append( UnitAction.build_Return( UnitAction.DIRECTION_RIGHT));
                if self._y < pgs.getHeight() - 1 and udown != None and udown._type._isStockpile and udown._player == self._player:l.append( UnitAction.build_Return( UnitAction.DIRECTION_DOWN));
                if self._x > 0 and uleft != None and uleft._type._isStockpile and uleft._player == self._player: l.append( UnitAction.build_Return( UnitAction.DIRECTION_LEFT));

   
        #if the player has enough resources, adds a produce action for each type this unit produces.
        #a produce action is added for each free tile around the producer 
        for  ut in self._type._produces_v:
            if p.getResources() >= ut._cost:
                tup : int =  pgs.getTerrain(self._x, self._y - 1) if self._y > 0 else pgs.TERRAIN_WALL;
                tright : int =  pgs.getTerrain(self._x + 1, self._y) if self._x < pgs.getWidth() - 1 else pgs.TERRAIN_WALL
                tdown : int = pgs.getTerrain(self._x, self._y + 1) if self._y < pgs.getHeight() - 1 else pgs.TERRAIN_WALL
                tleft : int = pgs.getTerrain(self._x - 1, self._y) if self._x > 0 else pgs.TERRAIN_WALL

                if tup == pgs.TERRAIN_NONE and pgs.getUnitAt(self._x, self._y - 1) == None: l.append( UnitAction.build_Produce( UnitAction.DIRECTION_UP, ut));
                if tright == pgs.TERRAIN_NONE and pgs.getUnitAt(self._x + 1, self._y) == None: l.append( UnitAction.build_Produce( UnitAction.DIRECTION_RIGHT, ut));
                if tdown == pgs.TERRAIN_NONE and pgs.getUnitAt(self._x, self._y + 1) == None: l.append( UnitAction.build_Produce( UnitAction.DIRECTION_DOWN, ut));
                if tleft == pgs.TERRAIN_NONE and pgs.getUnitAt(self._x - 1, self._y) == None: l.append(UnitAction.build_Produce( UnitAction.DIRECTION_LEFT, ut));


        #if the unit can move, adds a move action for each free tile around it
        if self._type._canMove:
            tup : int = pgs.getTerrain(self._x, self._y - 1) if self._y > 0  else pgs.TERRAIN_WALL
            tright : int = pgs.getTerrain(self._x + 1, self._y) if self._x < pgs.getWidth() - 1   else pgs.TERRAIN_WALL
            tdown : int = pgs.getTerrain(self._x, self._y + 1) if self._y < pgs.getHeight() - 1  else pgs.TERRAIN_WALL
            tleft : int = pgs.getTerrain(self._x - 1, self._y) if self._x > 0  else pgs.TERRAIN_WALL

            if tup == pgs.TERRAIN_NONE and uup == None: l.append( UnitAction.build_Move( UnitAction.DIRECTION_UP))
            if tright == pgs.TERRAIN_NONE and uright == None: l.append( UnitAction.build_Move( UnitAction.DIRECTION_RIGHT))
            if tdown == pgs.TERRAIN_NONE and udown == None: l.append( UnitAction.build_Move( UnitAction.DIRECTION_DOWN));
            if tleft == pgs.TERRAIN_NONE and uleft == None: l.append( UnitAction.build_Move( UnitAction.DIRECTION_LEFT));
        
   
        # units can always stay idle:
        l.append( UnitAction.build_None())
    
        return l;
    
    '''
        * Indicates whether this unit can perform an action in a given state
        * @param ua
        * @param gs
        * @return
    '''
    
    def canExecuteAction(self,ua :UnitAction,gs :GameState)->bool:
        
        l : list[UnitAction] = self.getUnitActionsINT(gs,ua.ETA(self))
        
        if ua in l:
            return True
        else:
            return False
    



    def toString(self) -> str:
        return self._type._name + "(" + str(self._ID) + ")" + "(" + str(self._player) + ", (" + str(self._x) + "," + str(self._y) + "), " + str(self._hitpoints) + ", " + str(self._resources) + ")"

    def __eq__(self, others:Unit)->bool:
        if not isinstance(others, UnitAction):
            return False
        return self._ID == others._ID
    #Unit& clone();

    '''
         * Returns the unique ID
         */
        int hashCode();


        /**
         * Writes the XML representation of this unit
         * @param w
         
        void toxml(XMLWriter w);
        */
        /**
         * Writes a JSON representation of this unit
         * @param w
         * @throws Exception
        
        public void toJSON(Writer w) throws Exception {
            w.write(
                "{\"type\":\"" + type.name + "\", " +
                "\"ID\":" + ID + ", " +
                "\"player\":" + player + ", " +
                "\"x\":" + x + ", " +
                "\"y\":" + y + ", " +
                "\"resources\":" + resources + ", " +
                "\"hitpoints\":" + hitpoints +
                "}"
            );
        }
         */
    '''
    
    #Constructs a unit from a XML element
    @staticmethod
    def fromXML(xml_node , utt):
        typeName = xml_node.attrib["type"]
        ID = int(xml_node.attrib["ID"])
        player = int(xml_node.attrib["player"])
        x = int(xml_node.attrib["x"])
        y = int(xml_node.attrib["y"])
        resources = int(xml_node.attrib["resources"])
        hitpoints = int(xml_node.attrib["hitpoints"])

        
        if ID >= Unit.next_ID: Unit.next_ID = ID + 1;
        utype = utt.getUnitTypeString(typeName);
        
        u =   Unit(ID, player, utype, x, y, resources);
        u._hitpoints = hitpoints
        
        return u

    '''
        * Constructs a unit from a JSON object
        * @param o
        * @param utt
        * @return
    '''   
    #static  Unit fromJSON(JsonObject o, UnitTypeTable utt);
    
        
   