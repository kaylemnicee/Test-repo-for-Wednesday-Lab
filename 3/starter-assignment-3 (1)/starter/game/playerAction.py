from __future__ import annotations
from game.resourceUsage import ResourceUsage
from game.unit import Unit
from game.unitAction import UnitAction


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.gameState import GameState


class PlayerAction:
    

    def __init__(self):
        #A list of unit actions
        self._actions : list[tuple[Unit,UnitAction]]= [] #vector<pair<Unit, UnitAction>> actions;
   
        #Represents the resources used by the player action
        #TODO rename the field
        self._r = ResourceUsage()

    #@see java.lang.Object#equals(java.lang.Object)
    #bool equals(PlayerAction o);


    #Returns whether there are no player actions
    #bool isEmpty();

    #Returns whether the player has assigned any action different
    #than {@link UnitAction#TYPE_NONE} to any of its units
    #bool hasNonNoneActions();

    #Returns the number of actions different than
    #{@link UnitAction#TYPE_NONE}
    #int hasNamNoneActions();


    #Returns the usage of resources
    def getResourceUsage(self)->ResourceUsage:
        return self._r

    #Sets the resource usage
    def setResourceUsage(self,a_r:ResourceUsage)->None:
        self._r = a_r

    #Adds a new {@link UnitAction} to a given {@link Unit}
    def addUnitAction(self, u:Unit,  a:UnitAction)->None:
        self._actions.append([u,a])

    #Removes a pair of Unit and UnitAction from the list
    #void removeUnitAction(Unit &u, UnitAction &a);

    #Merges this with another PlayerAction
    #PlayerAction merge(PlayerAction a);


    #Returns a list of pairs of units and UnitActions
    def getActions(self)->list[tuple[Unit,UnitAction]]:
        return self._actions

    #Searches for the unit in the collection and returns the respective {@link UnitAction}
    #def  getAction(self, u:Unit)->UnitAction:
    #    pass

    #vector<PlayerAction> cartesianProduct(vector<UnitAction>* lu, Unit* u, GameState* s);

    #Returns whether this PlayerAction is consistent with a
    # given {@link ResourceUsage} and a {@link GameState}
    def consistentWith(self, u:ResourceUsage,  gs:GameState)->bool:
        return self._r.consistentWith(u, gs);


    #Assign "none" to all the units that need an action and do not have one
    #for the specified duratio
    #@param duration the number of frames the 'none' action should last
    def fillWithNones(self, s:GameState,  pID:int,  duration:int)->None:
        pgs = s.getPhysicalGameState()
        for u in pgs.getUnits().values():
            if u.getPlayer() == pID :
                if not u.getID() in s._unitActions:
                    found = False;
                    for  u2, au in self._actions:
                         
                         if u2.getID() == u.getID() :
                             
                            found = True
                          
                            break
                    if not found:  
                        t = [u, UnitAction.build_None()]
                        self._actions.append(t)


    #Returns true if this object passes the integrity check.
    #It fails if the unit is being assigned an action from a player
    #that does not owns it
    def integrityCheck(self)->bool:
        player = -1;
        for u, ua in self._actions:
            if player == -1:
                player = u.getPlayer()
            else :
                if player != u.getPlayer():
                    print ("integrityCheck: units from more than one player!")
                    return False;
        return True;

    #@see java.lang.Object#clone()
    #PlayerAction clone();
    

    #Resets the PlayerAction
    #def  clear()->None:
    #    pass


    #@see java.lang.Object#toString()
    #string toString();


    #Writes to XML
    #void toxml(XMLWriter w);


    #Writes to JSON
    #void toJSON(Writer w);
    


    #Creates a PlayerAction from a XML element
    #static PlayerAction fromXML(Element e, GameState gs, UnitTypeTable utt) 
    
    #Creates a PlayerAction from a JSON object
    #static PlayerAction fromJSON(String JSON, GameState gs, UnitTypeTable utt);
