from .AbstractAction import AbstractAction
from .AbstractAction import AbstractAction
from game.unit import Unit
from game.unitAction import UnitAction
from game.resourceUsage import ResourceUsage
from game.gameState import GameState
from game.AStarPathFinding import AStarPathFinding

class Move(AbstractAction):

    def toString(self):
        return "no done "

    
    def __init__(self, u : Unit,  a_x: int,  a_y : int,  a_pf : AStarPathFinding):
        super().__init__(u);
        self._x = a_x
        self._y = a_y
        self._pf = a_pf
    
    
    def completed(self, gs) :
    
        return self._unit.getX() == self._x and self._unit.getY() == self._y;
    
    '''
    
    public boolean equals(Object o)
    {
        if (!(o instanceof Move)) return false;
        Move a = (Move)o;
        return x == a.x && y == a.y && pf.getClass() == a.pf.getClass();
    }

    
    public void toxml(XMLWriter w)
    {
        w.tagWithAttributes("Move","unitID=\""+unit.getID()+"\" x=\""+x+"\" y=\""+y+"\" pathfinding=\""+pf.getClass().getSimpleName()+"\"");
        w.tag("/Move");
    }       
    '''
    def execute(self, gs : GameState,  ru: ResourceUsage)->UnitAction :
        pgs = gs.getPhysicalGameState();
        move = self._pf.findPathToPositionInRange(self._unit, self._x+self._y*gs.getPhysicalGameState().getWidth(), 1, gs);
#       System.out.println("AStarAttak returns: " + move);
        
        if move.getType()!=UnitAction.getTYPE_NONE() and gs.isUnitActionAllowed(self._unit, move): return move
  
        return None;
   