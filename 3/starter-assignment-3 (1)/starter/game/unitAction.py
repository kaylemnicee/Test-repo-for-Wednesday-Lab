from __future__ import annotations
from random import Random

from game.resourceUsage import ResourceUsage


from game.unitType import UnitType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.gameState import GameState
    from game.unit import Unit
    from game.physicalGameState import PhysicalGameState

class UnitAction:
    
   
    #The 'no-op' action
    TYPE_NONE = 0
    @staticmethod
    def getTYPE_NONE()->int:
        return UnitAction.TYPE_NONE

    #Action of moving
    TYPE_MOVE = 1
    @staticmethod
    def  getTYPE_MOVE()->int:
        return UnitAction.TYPE_MOVE


    #Action of harvesting
    TYPE_HARVEST = 2
    @staticmethod
    def getTYPE_HARVEST()->int:
        return UnitAction.TYPE_HARVEST

    #Action of return to base with resource
    TYPE_RETURN = 3
    @staticmethod
    def getTYPE_RETURN()->int:
        return UnitAction.getTYPE_RETURN
        

    #Action of produce a unit
    TYPE_PRODUCE = 4
    @staticmethod
    def getTYPE_PRODUCE()->int:
        return UnitAction.TYPE_PRODUCE

    #Action of attacking a location
    TYPE_ATTACK_LOCATION = 5
    @staticmethod
    def getTYPE_ATTACK_LOCATION()->int:
        return UnitAction.TYPE_ATTACK_LOCATION

    #Total number of action types
    NUMBER_OF_ACTION_TYPES = 6
    @staticmethod
    def getNUMBER_OF_ACTION_TYPES()->int:
       return UnitAction.NUMBER_OF_ACTION_TYPE

    actionName :tuple[str,str,str,str,str,str] = ["wait", "move",
            "harvest", "return", "produce", "attack_location"];


    #Direction of 'standing still'
    DIRECTION_NONE = -1;
    @staticmethod
    def getDIRECTION_NONE()->int:
        return UnitAction.DIRECTION_NONE


    # Alias for up
    DIRECTION_UP = 0;
    @staticmethod
    def getDIRECTION_UP()->int:
        return UnitAction.DIRECTION_UP
    
     #Alias for right
    DIRECTION_RIGHT = 1;
    @staticmethod
    def getDIRECTION_RIGHT()->int:
        return UnitAction.DIRECTION_RIGHT

    #Alias for down
    DIRECTION_DOWN = 2;
    @staticmethod
    def getDIRECTION_DOWN()->int:
        return UnitAction.DIRECTION_DOWN

    # Alias for left
    DIRECTION_LEFT = 3;
    @staticmethod
    def getDIRECTION_LEFT():
       return UnitAction.DIRECTION_LEFT
   

    #The offset caused by each direction of movement in X Indexes correspond
    #to the constants used in this class
    DIRECTION_OFFSET_X : tuple[int,int,int,int] = [0, 1, 0, -1 ]

    #The offset caused by each direction of movement in y Indexes correspond
    #to the constants used in this class
    DIRECTION_OFFSET_Y : tuple[int,int,int,int] = [ -1, 0, 1, 0]

    #Direction names. Indexes correspond to the constants used in this class
    DIRECTION_NAMES : tuple[str,str,str,str] = [ "up", "right", "down", "left" ]

    @staticmethod
    def build_None()->UnitAction:
        return UnitAction()
    
    @staticmethod
    def build_Move(a_direction:int)->UnitAction:
        a = UnitAction()
        a._type = UnitAction.TYPE_MOVE
        a._parameter = a_direction
        return a

    @staticmethod
    def build_Attack(x:int,y:int)->UnitAction:
        a = UnitAction()
        a._type = UnitAction.TYPE_ATTACK_LOCATION
        a._x = x
        a._y = y
        return a

    @staticmethod
    def build_Haverst(a_direction:int)->UnitAction:
        a = UnitAction()
        a._type = UnitAction.TYPE_HARVEST
        a._parameter = a_direction
        return a
    
    @staticmethod
    def build_Return(a_direction:int)->UnitAction:
        a = UnitAction()
        a._type = UnitAction.TYPE_RETURN
        a._parameter = a_direction
        return a
    
    @staticmethod
    def build_Produce(a_direction:int,a_unit_type:UnitType)->UnitAction:
        a = UnitAction()
        a._type = UnitAction.TYPE_PRODUCE
        a._parameter = a_direction
        
        a._unitType = a_unit_type
        return a


    def __init__(self):
        #Type of this UnitAction
 
        self._type = UnitAction.TYPE_NONE

        #used for both "direction" and "duration"
        self._parameter = UnitAction.DIRECTION_NONE

        #X and Y coordinates of an attack-location action
        self._x =None
        self._y =None
    

        # UnitType associated with a 'produce' action
        self._unitType = None

        #Amount of resources associated with this action
        self._r_cache=None;

      
    def __eq__(self, others:UnitAction)->bool:
        if not isinstance(others, UnitAction):
            return False
        if others._type != self._type:
                return False
        elif self._type == UnitAction.TYPE_NONE or \
                    self._type == UnitAction.TYPE_MOVE or \
                    self._type == UnitAction.TYPE_HARVEST or \
                    self._type == UnitAction.TYPE_RETURN:
            return others._parameter == self._parameter
    
        elif self._type == UnitAction.TYPE_ATTACK_LOCATION:
            return others._x == self._x and others._y == self._y
        else:
            return others._parameter == self._parameter and others._unitType == self._unitType;
    


    #int hashCode();

    
    #Returns the type associated with this action
    def getType(self)->int:
        return self._type

    #Returns the UnitType associated with this action
    def getUnitType(self)->UnitType:
        return self._unitType

    #Returns the ResourceUsage associated with this action, given a Unit and a
    #PhysicalGameState
    def resourceUsage(self, u : Unit,  pgs : PhysicalGameState)->ResourceUsage:
        if self._r_cache != None:
            return self._r_cache;
        self._r_cache =  ResourceUsage()
 
        if self._type  == UnitAction.TYPE_MOVE: 
            pos :int = u.getX() + u.getY() * pgs.getWidth();
            
            if self._parameter == UnitAction.DIRECTION_UP:
                pos -= pgs.getWidth();
            elif self._parameter == UnitAction.DIRECTION_RIGHT:
                pos+=1
            elif self._parameter == UnitAction.DIRECTION_DOWN:
                pos += pgs.getWidth();
            elif self._parameter == UnitAction.DIRECTION_LEFT:
                pos-=1
                
            self._r_cache._positionsUsed.append(pos);
        
        
        elif self._type  == UnitAction.TYPE_PRODUCE: 
            self._r_cache._resourcesUsed[u.getPlayer()] += self._unitType._cost;
            pos :  int = u.getX() + u.getY() * pgs.getWidth();
            
            if self._parameter == UnitAction.DIRECTION_UP:
                pos -= pgs.getWidth()
            elif self._parameter == UnitAction.DIRECTION_RIGHT:
                pos+=1
            elif self._parameter == UnitAction.DIRECTION_DOWN:
                pos += pgs.getWidth()
            elif self._parameter == UnitAction.DIRECTION_LEFT:
                pos-=1
           
            self._r_cache._positionsUsed.append(pos);
      
  
        return self._r_cache;

    '''
     Returns the estimated time of conclusion of this action The Unit
     * parameter is necessary for actions of {@link #TYPE_MOVE},
     * {@link #TYPE_ATTACK_LOCATION} and {@link #TYPE_RETURN}. In other cases it
     * can be null
     *
     * @param u
     * @return
     */
    '''
    def ETA(self, u:Unit)->int:
        if self._type == UnitAction.TYPE_NONE:
            return self._parameter;
        elif self._type == UnitAction.TYPE_MOVE:
            return u.getMoveTime();
        elif self._type == UnitAction.TYPE_ATTACK_LOCATION:
            return u.getAttackTime();
        elif self._type == UnitAction.TYPE_HARVEST:
            return u.getHarvestTime();
        elif self._type == UnitAction.TYPE_RETURN:
            return u.getMoveTime();
        elif self._type == UnitAction.TYPE_PRODUCE:
            return self._unitType._produceTime;
        return 0;

       
    '''
     * Effects this action in the game state. If the action is related to a
     * unit, changes it position accordingly
     *
     * @param u
     * @param s
    '''
    def execute(self, u:Unit, s:GameState)->None:
        pgs = s.getPhysicalGameState();

   
        if self._type ==  UnitAction.TYPE_NONE:	#no-op
            pass;

        elif self._type ==  UnitAction.TYPE_MOVE: #moves the unit in the intended direction
            
            if self._parameter == UnitAction.DIRECTION_UP:
                u.setY(u.getY() - 1);
            elif self._parameter == UnitAction.DIRECTION_RIGHT:
                u.setX(u.getX() + 1);
            elif self._parameter == UnitAction.DIRECTION_DOWN:
                u.setY(u.getY() + 1);  
            elif self._parameter == UnitAction.DIRECTION_LEFT:
                u.setX(u.getX() - 1);
             
        elif self._type ==  UnitAction.TYPE_ATTACK_LOCATION: #if there's a unit in the target location, damages it
            other = pgs.getUnitAt(self._x, self._y);
            if other != None:
                damage = 0
                
                if u.getMinDamage() == u.getMaxDamage():
                    damage = u.getMinDamage()
                else :
                    damage = u.getMinDamage() + (Random()%(1 + (u.getMaxDamage() - u.getMinDamage())));
                
                other.setHitPoints(other.getHitPoints() - damage)
   

        elif self._type == UnitAction.TYPE_HARVEST: #//attempts to harvest from a resource in the target direction
            maybeAResource = None;
            if self._parameter == UnitAction. DIRECTION_UP:
                maybeAResource = pgs.getUnitAt(u.getX(), u.getY() - 1);
            elif self._parameter == UnitAction.DIRECTION_RIGHT:
                maybeAResource = pgs.getUnitAt(u.getX() + 1, u.getY());
            elif self._parameter == UnitAction.DIRECTION_DOWN:
                maybeAResource = pgs.getUnitAt(u.getX(), u.getY() + 1);
            elif self._parameter == UnitAction.DIRECTION_LEFT:
                maybeAResource = pgs.getUnitAt(u.getX() - 1, u.getY());

            
            if maybeAResource != None and maybeAResource.getType()._isResource and u.getType()._canHarvest and u.getResources() == 0:
                #indeed it is a resource, harvest from it
               
                maybeAResource.setResources(maybeAResource.getResources() - u.getHarvestAmount());
                if maybeAResource.getResources() <= 0:
                    s.removeUnit(maybeAResource);
                
                u.setResources(u.getHarvestAmount());
      
        elif self._type == UnitAction.TYPE_RETURN: #//returns to base with a resource
            base =  None;
            if self._parameter == UnitAction.DIRECTION_UP:
                base = pgs.getUnitAt(u.getX(), u.getY() - 1)
            elif self._parameter == UnitAction.DIRECTION_RIGHT:
                base = pgs.getUnitAt(u.getX() + 1, u.getY())
            elif self._parameter == UnitAction.DIRECTION_DOWN:
                base = pgs.getUnitAt(u.getX(), u.getY() + 1)
            elif self._parameter == UnitAction.DIRECTION_LEFT:
                base = pgs.getUnitAt(u.getX() - 1, u.getY());

           
            if base != None and base.getType()._isStockpile and u.getResources() > 0:
                p = pgs.getPlayer(u.getPlayer())
                p.setResources(p.getResources() + u.getResources())
                u.setResources(0);  
            else :#{// base is not there
                pass

        elif self._type == UnitAction.TYPE_PRODUCE:# //produces a unit in the target direction
            targetx : int = u.getX();
            targety : int = u.getY();
            
            if self._parameter == UnitAction.DIRECTION_UP:
                targety-=1
            elif self._parameter == UnitAction.DIRECTION_RIGHT:
                targetx+=1
            elif self._parameter == UnitAction.DIRECTION_DOWN:
                targety+=1
            elif self._parameter == UnitAction.DIRECTION_LEFT:
                targetx-=1
            
            newUnit =  pgs.createUnit(u.getPlayer(), self._unitType, targetx, targety, 0);
           
            p = pgs.getPlayer(u.getPlayer());
            if p.getResources() - newUnit.getCost() >= 0:
                pgs.addUnit(newUnit);
                p.setResources(p.getResources() - newUnit.getCost())

            if p.getResources() < 0:
                #System.err.print("Illegal action executed! resources of player " + p.ID + " are now " + p.getResources() + "\n");
                #System.err.print(s);
                print("Illegal action executed! resources of player",p.getID(),"are now",p.getResources() );

   
     

    def toString(self)->str:
        tmp = UnitAction.actionName[self._type] + "("

        if type == UnitAction.TYPE_ATTACK_LOCATION:
            tmp += str(self._x) + ", " + str(self._y)
        elif type == UnitAction.TYPE_NONE:
            pass
        else :
            if self._parameter != UnitAction.DIRECTION_NONE:
                if self._parameter == UnitAction.DIRECTION_UP :tmp += "up";
                if self._parameter == UnitAction.DIRECTION_RIGHT: tmp += "right";
                if self._parameter == UnitAction.DIRECTION_DOWN:tmp += "down";
                if self._parameter == UnitAction.DIRECTION_LEFT: tmp += "left";
               
            if self._parameter != UnitAction.DIRECTION_NONE and \
                                 self._unitType != None: 
                tmp += ",";
            if self._unitType != None:
                
                tmp += self._unitType._name;
     
        return tmp + ")"; 

    #Returns the name of this action
    def getActionName(self)->str:
        return UnitAction.actionName[self._type];   

    #Returns the direction associated with this action
    def getDirection(self) ->int:
        return self._parameter  

    #Returns the X coordinate associated with this action
    def getLocationX(self)->int:
       return self._x

    #Returns the Y coordinate associated with this action
    def getLocationY(self):
        return self._y   
       

    #Writes a XML representation of this action
    #void toxml(XMLWriter w) 

    #Writes a JSON representation of this action
    #void toJSON(Writer w); 



    #void clearResourceUSageCache();

    '''
     * Creates a UnitAction from a XML element (calls the corresponding
     * constructor)
    //static UnitAction fromXML(Element e, UnitTypeTable utt) 
    
    /**
     * Creates a UnitAction from a JSON string
     *
     * @param JSON
     * @param utt
     * @return
     */
    // static UnitAction fromJSON(String JSON, UnitTypeTable utt);
    
    /**
     * Creates a UnitAction from a JSON object
     *
     * @param o
     * @param utt
     * @return
     */
     //static UnitAction fromJSON(JsonObject o, UnitTypeTable utt);
     '''
