from .AbstractAction import AbstractAction


from .AbstractAction import AbstractAction
from game.unit import Unit
from game.unitAction import UnitAction
from game.resourceUsage import ResourceUsage
from game.gameState import GameState

class AttackIfrange (AbstractAction):
    

    def toString(self):
        return "no done "

    def __init__(self, u : Unit) :
        super().__init__(u)
    
    
    def completed(self, gs , GameState)->bool:
        return False
    
    
    #public boolean equals(Object o)
   

    
    #public void toxml(XMLWriter w)            

    def execulte(self, gs : GameState,  ru : ResourceUsage)->UnitAction :
        pgs = gs.getPhysicalGameState();
        if  not self._unit.getType().getCanAttack(): return None;
        for target in pgs.getUnits() :
            if target.getPlayer()!=-1 and target.getPlayer()!=self._unit.getPlayer():
                dx = target.getX()-self._unit.getX();
                dy = target.getY()-self._unit.getY();
                d = (dx*dx+dy*dy)**0.5;
                if d<=self._unit.getAttackRange():
                    return  UnitAction.build_Attack(target.getX(),target.getY());
           
        return None;
    
    
    
    