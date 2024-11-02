from __future__ import annotations

'''
 * A general unit definition that could turn out to be anything
 * @author santi, inspired in the original UnitDefinition class by Jeff Bernard
 *
 */
 '''



class UnitType:
    
        def __init__(self):
            #* The unique identifier of this type
            self._ID : int = 0

            #The name of this type
            self._name : str= ""

            #Cost to produce a unit of this type
            self._cost : int  = 1

            #Initial Hit Points of units of this type
            self._hp : int  = 1

            #Minimum damage of the attack from a unit of this type
            self._minDamage : int  = 1

            # Maximum damage of the attack from a unit of this type
            self._maxDamage : int  = 1

            # Range of the attack from a unit of this type
            self._attackRange : int  = 1

            #Time that each action takes to accomplish
            self._produceTime : int  = 10
            self._moveTime : int  = 10
            self._attackTime : int  = 10
            self._harvestTime : int  = 10
            self._returnTime : int  = 10

            '''
            * How many resources the unit can carry.
            * Each time the harvest action is executed, this is
            * how many resources does the unit gets
            '''
            self._harvestAmount : int  = 1

            #the radius a unit can see for partially observable game states.
            self._sightRadius : int  = 4

            #Can this unit type be harvested?
            self._isResource : bool = False

           #Can resources be returned to this unit type?
            self._isStockpile : bool = False

            #Is this a harvester type?
            self._canHarvest : bool = False
            
            #Can a unit of this type move?
            self._canMove : bool = True

            # Can a unit of this type attack?
            self._canAttack : bool = True

            #Units that this type of unit can produce
            self._produces_v : list[UnitType] = [] #vector<UnitType*> produces_v;

            #Which unit types produce a unit of this type
            self._producedBy_v : list[UnitType]= [] #vector<UnitType*> producedBy_v;

           
            #Returns the hash code of the name
            #assume that all unit types have different names
            #int hashCode();
            

         
        def copy(self,  other ) :
            pass  
            
        def getCost(self):
            return self._cost

        def getCanMove(self) -> bool:
            return self._canMove
        def getIsStockpile(self) -> bool:
            return self._isStockpile
        def getCanAttack(self) -> bool:
            return self._canAttack
        def getcanHarvest(self) -> bool:
            return self._canHarvest
        def getisResource(self) -> bool:
            return self._isResource  
       
        def equals(self, ut:UnitType ) ->bool:
            return ut.name == self._name   

        '''
            * Adds a unit type that a unit of this type can produce
            * @param ut
        '''
        def produces(self, ut:UnitType ) -> None:
            self._produces_v.append(ut)
            ut._producedBy_v.append(self)   

      
        def getName(self) -> str:
            return self._name    