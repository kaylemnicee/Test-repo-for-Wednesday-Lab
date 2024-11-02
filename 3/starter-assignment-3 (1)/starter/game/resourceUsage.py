from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.gameState import GameState


class ResourceUsage:

    def __init__(self):
        self._positionsUsed :list[int] = []
        self._resourcesUsed : list[int] = [ 0,0 ]


    #Returns whether this instance is consistent with another ResourceUsage in
    #* a given game state. Resource usages are consistent if they respect the
    #* players' resource amount and don't have conflicting uses
    def consistentWith(self, anotherUsage:ResourceUsage, gs:GameState)->bool:
        for pos in anotherUsage._positionsUsed:
            if pos in self._positionsUsed:
                return False
        for i in range(2): # conferir
            if anotherUsage._resourcesUsed[i] == 0: continue;
            #&& // this extra condition (which should not be needed), is because \
            # if an AI has a bug and allows execution of actions that
            # brings resources below 0, this code would fail.
                   
            if self._resourcesUsed[i] + anotherUsage._resourcesUsed[i] > 0 and \
                     self._resourcesUsed[i] + anotherUsage._resourcesUsed[i] > gs.getPlayer(i).getResources():
                return False;
        return True
    

    

    

    #Returns the list with used resource positions
    def getPositionsUsed(self) -> list[int]:
        return self._positionsUsed;

    #Returns the amount of resources used by the player
    def getResourcesUsed(self, player:int)->int:
        return self._resourcesUsed[player]

    #Merges this and another instance of ResourceUsage into a new one
    #def  mergeIntoNew(self, other):
    #    pass

    #Merges another instance of ResourceUsage into this one
    def merge(self, other)->None:
        for  pos in other._positionsUsed:
            self._positionsUsed.append(pos)
        for i in range(2):
            self._resourcesUsed[i] += other._resourcesUsed[i]

    #ResourceUsage clone();

    #string toString();