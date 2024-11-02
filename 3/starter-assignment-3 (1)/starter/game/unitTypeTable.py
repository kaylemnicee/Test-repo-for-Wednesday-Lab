

'''
 * The unit type table stores the unit types the game can have.
 * It also determines the attributes of each unit type.
 * The unit type table determines the balance of the game.
 * @author santi
 '''

from game.unitType import UnitType


class UnitTypeTable:
	

        #Empty type table should not be used!
        EMPTY_TYPE_TABLE = -1

        #Version one
        VERSION_ORIGINAL = 1

        #Version two (a fine tune of the original)
        VERSION_ORIGINAL_FINETUNED = 2

        
         #A non-deterministic version (damages are random)
        VERSION_NON_DETERMINISTIC = 3

        #A conflict resolution policy where move conflicts cancel both moves
        MOVE_CONFLICT_RESOLUTION_CANCEL_BOTH = 1;   # (default)

        #A conflict resolution policy where move conflicts are solved randomly
        MOVE_CONFLICT_RESOLUTION_CANCEL_RANDOM = 2;   #// (makes game non-deterministic)

        #A conflict resolution policy where move conflicts are solved by
        #alternating the units trying to move
        MOVE_CONFLICT_RESOLUTION_CANCEL_ALTERNATING = 3


        

        '''
            * Creates a unit type table specifying both the version and the move conflict
            * resolution strategy
            * @param version
            * @param crs the move conflict resolution strategy
        '''
        def __init__(self, version :int = None,  crs :int = None):
            if version == None: version = UnitTypeTable.VERSION_ORIGINAL 
            if crs == None: crs = UnitTypeTable.MOVE_CONFLICT_RESOLUTION_CANCEL_BOTH 
            
            self._unitTypes = [] # vector<UnitType*> unitTypes;
            self.setUnitTypeTable(version,crs)
            


        '''
         * Sets the version and move conflict resolution strategy to use
         * and configures the attributes of each unit type depending on the
         * version
         * @param version
         * @param crs the move conflict resolution strategy
        '''
        def setUnitTypeTable(self, version:int,  crs ):
            self._moveConflictResolutionStrategy = crs

            if version == UnitTypeTable.EMPTY_TYPE_TABLE: return

            #Create the unit types:
            #RESOURCE:
            resource =   UnitType()
            resource._name = "Resource"
            resource._isResource = True
            resource._isStockpile = False
            resource._canHarvest = False
            resource._canMove = False
            resource._canAttack = False
            resource._sightRadius = 0
            self.addUnitType(resource)

            #BASE:
            base =   UnitType()
            base._name = "Base"
            base._cost = 10
            base._hp = 10
            
            if version == UnitTypeTable.VERSION_ORIGINAL: base._produceTime = 250
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED: base._produceTime = 200
            
            base._isResource = False
            base._isStockpile = True
            base._canHarvest = False
            base._canMove = False
            base._canAttack = False
            base._sightRadius = 5
            self.addUnitType(base)

            #BARRACKS: 
            barracks =  UnitType()
            barracks._name = "Barracks"
            barracks._cost = 5
            barracks._hp = 4
            
            if version == UnitTypeTable.VERSION_ORIGINAL:
                barracks._produceTime = 200
             
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED:
              barracks._produceTime = 100
                  
            if version == UnitTypeTable.VERSION_NON_DETERMINISTIC:
                barracks._produceTime = 100
               
            barracks._isResource = False
            barracks._isStockpile = False
            barracks._canHarvest = False
            barracks._canMove = False
            barracks._canAttack = False
            barracks._sightRadius = 3
            self.addUnitType(barracks)

            #WORKER: 
            worker =  UnitType()
            worker._name = "Worker"
            worker._cost = 1
            worker._hp = 1
            if version == UnitTypeTable.VERSION_ORIGINAL:
                worker._minDamage = worker._maxDamage = 1
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED:
                worker._minDamage = worker._maxDamage = 1
                
            if version == UnitTypeTable.VERSION_NON_DETERMINISTIC:
                worker._minDamage = 0
                worker._maxDamage = 2
            
            worker._attackRange = 1
            worker._produceTime = 50
            worker._moveTime = 10
            worker._attackTime = 5
            worker._harvestTime = 20
            worker._returnTime = 10
            worker._isResource = False
            worker._isStockpile = False
            worker._canHarvest = True
            worker._canMove = True
            worker._canAttack = True
            worker._sightRadius = 3
            self.addUnitType(worker)

            #LIGHT: 
            light =   UnitType()
            light._name = "Light"
            light._cost = 2
            light._hp = 4
            
            if version == UnitTypeTable.VERSION_ORIGINAL:
                light._minDamage = light._maxDamage = 2;   
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED:
                light._minDamage = light._maxDamage = 2
     
            if version == UnitTypeTable.VERSION_NON_DETERMINISTIC:
                light._minDamage = 1
                light._maxDamage = 3
           
            light._attackRange = 1
            light._produceTime = 80
            light._moveTime = 8
            light._attackTime = 5
            light._isResource = False
            light._isStockpile = False
            light._canHarvest = False
            light._canMove = True
            light._canAttack = True
            light._sightRadius = 2
            self.addUnitType(light)

            #HEAVY: 
            heavy =  UnitType()
            heavy._name = "Heavy"
            
            if version == UnitTypeTable.VERSION_ORIGINAL:
                heavy._minDamage = heavy._maxDamage = 4;   
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED:
                heavy._minDamage = heavy._maxDamage = 4
            if version == UnitTypeTable.VERSION_NON_DETERMINISTIC:
                heavy._minDamage = 0
                heavy._maxDamage = 6
            
            heavy._attackRange = 1
            heavy._produceTime = 120
           
            if version == UnitTypeTable.VERSION_ORIGINAL:
                heavy._moveTime = 12
                heavy._hp = 4
                heavy._cost = 2
           
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED:
                heavy._moveTime = 10
                heavy._hp = 8
                heavy._cost = 3   
            if version == UnitTypeTable.VERSION_NON_DETERMINISTIC:
                heavy._moveTime = 10
                heavy._hp = 8
                heavy._cost = 3   
               
           
            heavy._attackTime = 5
            heavy._isResource = False
            heavy._isStockpile = False
            heavy._canHarvest = False
            heavy._canMove = True
            heavy._canAttack = True
            heavy._sightRadius = 2
            self.addUnitType(heavy)

            #RANGED: 
            ranged =   UnitType()
            ranged._name = "Ranged"
            ranged._cost = 2
            ranged._hp = 1
            
            if version == UnitTypeTable.VERSION_ORIGINAL:
                ranged._minDamage = ranged._maxDamage = 1;   
            if version == UnitTypeTable.VERSION_ORIGINAL_FINETUNED:
                ranged._minDamage = ranged._maxDamage = 1
                
            if version == UnitTypeTable.VERSION_NON_DETERMINISTIC:
                ranged._minDamage = 1
                ranged._maxDamage = 2
          
           
            ranged._attackRange = 3
            ranged._produceTime = 100
            ranged._moveTime = 10
            ranged._attackTime = 5
            ranged._isResource = False
            ranged._isStockpile = False
            ranged._canHarvest = False
            ranged._canMove = True
            ranged._canAttack = True
            ranged._sightRadius = 3
            self.addUnitType(ranged)


            base.produces(worker)
            barracks.produces(light)
            barracks.produces(heavy)
            barracks.produces(ranged)
            worker.produces(base)
            worker.produces(barracks)

        '''
         * Adds a new unit type to the game
         * @param ut
        '''
        def addUnitType(self, ut:UnitType)->None:
            ut._ID = len(self._unitTypes)
            self._unitTypes.append(ut)

        '''
         * Retrieves a unit type by its numeric ID
         * @param ID
         * @return
         '''
        def getUnitType(self, ID:int)->UnitType:
            return self._unitTypes[ID]

        '''
         * Retrieves a unit type by its name. Returns null if name is not found.
         * @param name
         * @return
         '''
        def getUnitTypeString(self, name: str)-> UnitType:
            for ut in self._unitTypes:
                if ut._name == name:
                    return ut
        
        '''
         * Returns the list of all unit types
         * @return
        '''
        def getUnitTypes(self) -> list[UnitType]:
            return self._unitTypes    

        '''
         * Returns the integer corresponding to the move conflict resolution strategy in use
         * @return
         '''
        def getMoveConflictResolutionStrategy(self) -> int:
            return self._moveConflictResolutionStrategy    


       