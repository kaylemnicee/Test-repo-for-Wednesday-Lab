from __future__  import annotations


from typing import TYPE_CHECKING





if TYPE_CHECKING:
    from synthesis.baseDSL.mainBase.node import Node
    from synthesis.baseDSL.util.factory import Factory



from abc import ABC, abstractmethod


class NoTerminal(ABC):
    
    @abstractmethod
    def getRule(self)->Node:
        pass
    
    @abstractmethod
    def setRule(self, node : Node)->None:
        pass
    
    @abstractmethod
    def rules(f: Factory)->list[Node] :
        pass