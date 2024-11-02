from abc import ABC, abstractmethod

from game.gameState import GameState

class Evaluator(ABC):
    @abstractmethod
    def analysis(self,gs : GameState, player:int,lastState: bool)->None:
        pass
    
    @abstractmethod
    def getValue(self)->float:
        pass
    
    @abstractmethod
    def reset(self)->None:
        pass