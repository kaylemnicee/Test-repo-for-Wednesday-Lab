


from game.unit import Unit
from game.unitAction import UnitAction


class UnitActionAssignment:
    def __init__(self,u :Unit,a :UnitAction, a_time:int):
        self._unit : Unit = u
        self._action : UnitAction = a
        self._time :int = a_time
    

    def getIdUnit(self)->int:
        return self._unit.getID()
    
    def getUnit(self)->Unit:
        return self._unit
    
    def getUnitAction(self)->UnitAction:
        return self._action
    
    def getTime(self)->int:
        return self._time

    def toString(self)->str:
        return "uaa : {"+str(self._time)+", " + self._unit.toString() + ", " + self._action.toString() + "}"
