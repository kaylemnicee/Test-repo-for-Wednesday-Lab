from random import Random
from game.physicalGameState import PhysicalGameState
from game.player import Player
from game.playerAction import PlayerAction
from game.resourceUsage import ResourceUsage
from game.unit import Unit
from game.unitAction import UnitAction
from game.unitActionAssignment import UnitActionAssignment
from game.unitTypeTable import UnitTypeTable
import numpy as np



class GameState:
    
    REPORT_ILLEGAL_ACTIONS = False

    
     #Initializes the GameState with a PhysicalGameState and a UnitTypeTable
    def __init__(self, a_pgs:PhysicalGameState, a_utt:UnitTypeTable):
        self._unitCancelationCounter = 0#  // only used if the action conflict resolution strategy is set to alternating

        self._time  :int = 0
        self._pgs : PhysicalGameState = a_pgs
        self._unitActions : dict[int,UnitActionAssignment]= {} #unordered_map<long, UnitActionAssignment> 
        self._utt : UnitTypeTable = a_utt
        self._free  = np.zeros((self._pgs.getWidth(), self._pgs.getHeight()), dtype=bool)
        
        self.calculateFree()
        

    def clone(self):#->GameState:
        utt : UnitTypeTable = self.getUnitTypeTable()
        pgs : PhysicalGameState = self.getPhysicalGameState().clone()
        
        gs : GameState = GameState(pgs,utt)
        return gs
        

    #Current game timestep (frames since beginning)
    def getTime(self)->int:
       return self._time

    #Removes a unit from the game
    def removeUnit(self,  u:Unit) ->None:

       if u.getID() in self._unitActions:self._unitActions.pop(u.getID())
       self._pgs.removeUnit(u)

    #  @see PhysicalGameState#getPlayer(int)
    def getPlayer(self, ID:int) ->Player:
       return self._pgs.getPlayer(ID)
    

    #@see PhysicalGameState#getUnit(long)
    def getUnit(self, ID:int)->Unit:
       return self._pgs.getUnit()

    #@see PhysicalGameState#getUnits()
    def getUnits(self)->list[Unit]:
       return self._pgs.getUnits()

    #Returns a map with the units and the actions assigned to them
    def getUnitActions(self)->dict[int,UnitActionAssignment]: #unordered_map<Unit, UnitActionAssignment>
        return self._unitActions

    def  getUnitTypeTable(self)->UnitTypeTable:
        return self._utt


    #Returns the action of a unit
    #def getUnitAction(self, u:Unit)->UnitAction:
       

    #Returns the action assigned to a unit
    def getActionAssignment(self, u :Unit) ->UnitActionAssignment:
        return self._unitActions.get(u._ID)
    
    
    #Indicates whether all units owned by the players have a valid action or not
    #def  isComplete()->bool:
        
        

    # @see PhysicalGameState#winner()
    def  winner(self)->int:
        return self._pgs.winner()

    #@see PhysicalGameState#gameover()
    def gameover(self) ->bool:
        return self._pgs.gameover()

    #Returns the {@link PhysicalGameState} associated with this state
    def getPhysicalGameState(self)->PhysicalGameState:
        return self._pgs


    '''
    Returns true if there is no unit in the specified position and no unit is executing
     * an action that will use that position
     * @param x coordinate of the position
     * @param y coordinate of the position
     * @return
     '''
    def free(self, x:int,  y:int)->bool:
        return self._free[x][y]    


    '''
    Returns a boolean array with true if there is no unit in
     * the specified position and no unit is executing an action that will use that position
     * @return
    '''
    #bool** getAllFree();
    def calculateFree(self)->None:
        self.calculateFree0()
        self.calculateFree1()
        self.calculateFree2()
    
    def calculateFree0(self)->None:
        self._free[:][:]= self._pgs._terrain[:][:] == PhysicalGameState.TERRAIN_NONE
      

    def calculateFree1(self)->None:
        for u in self._pgs._units.values():
            self._free[u.getX()][u.getY()] = False

    def calculateFree2(self)->None:
        for ua in self._unitActions.values():
            if ua._action._type == UnitAction.TYPE_MOVE or \
                ua._action._type == UnitAction.TYPE_PRODUCE:
                    u = ua._unit
                    if ua._action.getDirection() == UnitAction.DIRECTION_UP: self._free[u.getX()][u.getY()-1] = False
                    if ua._action.getDirection() == UnitAction.DIRECTION_RIGHT : self._free[u.getX()+1][u.getY()] = False
                    if ua._action.getDirection() == UnitAction.DIRECTION_DOWN : self._free[u.getX()][u.getY()+1] = False
                    if ua._action.getDirection() == UnitAction.DIRECTION_LEFT : self._free[u.getX()-1][u.getY()] = False
         
  
        
    def issue(self, pa:PlayerAction)->bool:
        returnValue = False
    
        for p in pa._actions:
            ru : ResourceUsage = p[1].resourceUsage(p[0], self._pgs)
        
            for  Puaa in self._unitActions.items():
                uaa = Puaa[1]
                u = self._pgs.getUnit(Puaa[0])
                aux = uaa._action.resourceUsage(u, self._pgs).consistentWith(ru, self)
          
                if not aux:
                    #conflicting actions:
             
                    if uaa._time == self._time:
                        # The actions were issued in the same game cycle, so it's normal
                        cancel_old : bool= False
                        cancel_new : bool = False
                        if self._utt.getMoveConflictResolutionStrategy() == UnitTypeTable.MOVE_CONFLICT_RESOLUTION_CANCEL_BOTH:
                            cancel_old = cancel_new = True

                        elif self._utt.getMoveConflictResolutionStrategy() == UnitTypeTable.MOVE_CONFLICT_RESOLUTION_CANCEL_RANDOM:
                            if Random.random() % 2 == 0: cancel_new = True
                            else: cancel_old = True
                        if self._utt.getMoveConflictResolutionStrategy() ==UnitTypeTable.MOVE_CONFLICT_RESOLUTION_CANCEL_ALTERNATING:
                            if (self._unitCancelationCounter % 2) == 0: cancel_new = True
                            else: cancel_old = True
                            self._unitCancelationCounter+=1
                       
                
                        u : Unit = self._pgs.getUnit(Puaa[0])
                        duration1 : int = uaa._action.ETA(u)
                        duration2 : int= p[1].ETA(p[0])
                 
                        if cancel_old:
                            #System.out.println("Old action canceled: " + uaa.unit.getID() + ", " + uaa.action);
                            uaa._action =  UnitAction.build_None()
              
                        if cancel_new: # System.out.println("New action canceled: " + p.m_a.getID() + ", " + p.m_b);
                            p = [p[0], UnitAction.build_None()]

                    else:
                        # This is more a problem, since it means there is a bug somewhere...
                        # (probably in one of the AIs)
                        # cout << "Inconsistent actions were executed!" << endl;
                        # cout << uaa.toString() << endl;
                        # cout << "  Resources: " << uaa.action->resourceUsage(uaa.unit, pgs).toString() << endl;
                        # cout << p.first->toString() + " assigned action " + p.second.toString() << " at time " << time << endl;
                        # cout << "  Resources: " + ru.toString() << endl;
                        #// cout << "Player resources: " << this->pgs->getPlayer(0).getResources().toString() << ", " + pgs.getPlayer(1).getResources() << endl;
                        # cout << "Resource Consistency: " << uaa.action->resourceUsage(uaa.unit, pgs).consistentWith(ru, this) << endl;

                        
                        # only the newly issued action is cancelled, since it's the problematic one...
                    
                        p[1] = UnitAction.build_None()

     
            uaa : UnitActionAssignment = UnitActionAssignment(p[0],  p[1], self._time)
            
       
            self._unitActions[p[0]._ID] = uaa 
       

            if p[1]._type != UnitAction.getTYPE_NONE(): returnValue = True
      
        return returnValue


    '''
     * Issues a player action, with additional checks for validity. This function is slower
     * than "issue", and should not be used internally by any AI. It is used externally in the main loop
     * to verify that the actions proposed by an AI are valid, before sending them to the game.
     * @param pa
     * @return "true" is any action different from NONE was issued
    '''
    def issueSafe(self, pa:PlayerAction)->bool:
        if not pa.integrityCheck(): print("PlayerAction inconsistent before 'issueSafe'")
  
        if not self.integrityCheck(): print("GameState inconsistent before 'issueSafe'")
        for p in pa._actions:
            
            if p[0] == None:
                #cout<<"Issuing an action to a null unit!!!"<<endl;
                return False
        

            if not p[0].canExecuteAction(p[1], self):
            
                if self.REPORT_ILLEGAL_ACTIONS:
                     print( "Issuing a non legal action to unit " , p[1].toString() , "!! Ignoring it...")
                #replace the action by a NONE action of the same duration:
            
                l : int = p[1].ETA(p[0])
           
                p[1]._type =  UnitAction.build_None()
          
            
            # get the unit that corresponds to that action (since the state might have been cloned):
            if  self._pgs.getUnit(p[0]._ID) != None:
                found : bool= False
           
                for  u in self._pgs._units.values():
                    if u.getX() == p[0].getX() and \
                        u.getY() == p[0].getY():
                        p[0] = u
                        found = True
                        break
            
                if not found:print( "Inconsistent order: pa") 

         
                #check to see if the action is legal!
                r : ResourceUsage = p[1].resourceUsage(p[0], self._pgs)
                for  position in r.getPositionsUsed():
                    y : int= int(position / self._pgs.getWidth())
                    x : int = int(position % self._pgs.getWidth())
                    if self._pgs.getTerrain(x, y) != PhysicalGameState.TERRAIN_NONE or \
                        self._pgs.getUnitAt(x, y) != None:
                        new_ua : UnitAction=  UnitAction(UnitAction.TYPE_NONE, p[1].ETA(p[0]))
                        # cout << "Player " << p.first->getPlayer() << " issued an illegal move action (to " << x + "," << y + ") to unit " + p.first->getID() << " at time " + this->getTime() << ", cancelling and replacing by " + new_ua.toString() << endl;
                        # cout << "    Action: " + p.second.toString() << endl;
                        # cout << "    Resources used by the action: " << r.toString() << endl;
                        # cout << "    Unit at that coordinate " << pgs->getUnitAt(x, y) << endl;
                        
                        p[1] = new_ua
             
        returnValue : UnitAction = self.issue(pa)
    
        if not self.integrityCheck():  print("GameState inconsistent after 'issueSafe': pa ")
        return returnValue
    

    '''
         * Indicates whether a player can issue an action in this state
         * @param pID the player ID
         * @return true if the player can execute any action
    '''
    def canExecuteAnyAction(self, pID : int)->bool:
        for u in self._pgs._units.values():
            if u.getPlayer() == pID:
                if u._ID in self._unitActions: return True
       
        return False


    '''
     *  This function checks whether the intended unit action  has any conflicts with some
     *  other action. It assumes that the UnitAction ua is valid (i.e. one of the
     *  actions that the unit can potentially execute)
    '''
    def isUnitActionAllowed(self, u : Unit,  ua :UnitAction)->bool:
        empty : PlayerAction = PlayerAction()

        if ua.getType() == UnitAction.TYPE_MOVE:
            x2 : int = u.getX() + UnitAction.DIRECTION_OFFSET_X[ua.getDirection()]
            y2 : int = u.getY() + UnitAction.DIRECTION_OFFSET_Y[ua.getDirection()]
            if x2 < 0 or y2 < 0 or \
                x2 >= self._pgs.getWidth() or \
                y2 >= self._pgs.getHeight() or \
                self._pgs.getTerrain(x2, y2) == PhysicalGameState.TERRAIN_WALL or \
                self._pgs.getUnitAt(x2, y2) != None: return False

        # Generate the reserved resources:
        for  u2 in self._pgs._units.values():
            uaa = self._unitActions[u2._ID] if u2._ID in self._unitActions else None 
        
            if uaa != None:
                ru : ResourceUsage= uaa._action.resourceUsage(u2, self._pgs)
                empty._r.merge(ru)

        return ua.resourceUsage(u, self._pgs).consistentWith(empty.getResourceUsage(), self)




  


    '''
     * Returns the time the next unit action will complete, or current time
     * if a player can act
     * @return
    '''
    def getNextChangeTime(self)->int:
        nextChangeTime = -1
        for ID,uaa in self._unitActions.items():
            u = self._pgs.getUnit(ID)
            t = uaa._time + uaa._action.ETA(u)
            if nextChangeTime == -1 or t < nextChangeTime: nextChangeTime = t
     
    
        if nextChangeTime == -1: return self.getTime()
        return nextChangeTime;  
    

    def updateScreen(self)->bool:
        nextChangeTime = -1
        for ID,uaa in self._unitActions.items():
            if uaa._time == self.getTime():return True
            u = self._pgs.getUnit(ID)
            t = uaa._time + uaa._action.ETA(u)
            if t - 1 == self.getTime(): return True
        return False;   
       

    '''
     * Runs a game cycle, execution all assigned actions
     * @return whether the game was over
    '''
    def cycle(self)->bool:
        self._time+=1
   
        readyToExecute : list[UnitActionAssignment] = []
        for  uaa in self._unitActions.items():
            u = self._pgs.getUnit(uaa[0])
         
            if uaa[1]._action.ETA(u) + uaa[1]._time <= self._time: readyToExecute.append(uaa[1]);
        
        # execute the actions:
      
        for uaa in readyToExecute:
       
            self._unitActions.pop(uaa._unit.getID())
            #System.out.println("Executing action for " + u + " issued at time " + uaa.time + " with duration " + uaa.action.ETA(uaa.unit));
            u = self._pgs.getUnit(uaa._unit.getID())
            uaa._action.execute(u, self)
            
        
        list_remove :list[Unit] =[]
        for  u in self._pgs.getUnits().values():
            if u.getHitPoints() <= 0:
                list_remove.append(u)
        for u in list_remove:
            self.removeUnit(u)


        self.calculateFree()
        return True





    '''
     * Returns the resources being used for all actions issued
     * in current cycle
     * @return
    '''
    def getResourceUsage(self)->ResourceUsage:
        base_ru : ResourceUsage =  ResourceUsage()

        for aux in self._pgs._units.items() :
            u = aux[1]
            uaa = self._unitActions[u._ID] if u._ID in self._unitActions else None 
            if uaa != None:
                ru : ResourceUsage = uaa._action.resourceUsage(u, self._pgs)
                base_ru.merge(ru)

        return base_ru




    '''
     * Verifies integrity: if an action was assigned to non-existing unit
     * or two actions were assigned to the same unit, integrity is violated
     * @return
    '''
    def integrityCheck(self)->bool:
        for it in self._unitActions.items():
  
            u = self._pgs.getUnit(it[0])
        
            if u == None:
                print("integrityCheck: unit does not exist!")
                return False
            
            # olhar dps
            #if (std::find(alreadyUsed.begin(), alreadyUsed.end(), u) != alreadyUsed.end()) {
            #     cout << "integrityCheck: two actions to the same unit!" << endl;
            #    return false;
            #}

        return True



 
    
  

  

