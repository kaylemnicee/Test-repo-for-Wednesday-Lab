from abc import ABC, abstractmethod
from game.gameState import GameState
from game.playerAction import PlayerAction

class AI(ABC):
    @abstractmethod
    def getActions(self, gs : GameState,player : int)->PlayerAction:
        pass
    
    @abstractmethod
    def reset(self)->None:
        pass
    
    