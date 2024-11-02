


import time
from game.gameState import GameState
from game.physicalGameState import PhysicalGameState
from game.screen import ScreenMicroRTS
from game.unitType import UnitType
from game.unitTypeTable import UnitTypeTable


class GameTestsLevel0:
    
    @staticmethod
    def testBuildUtt()->None:
        utt  = UnitTypeTable(2)
        unitTypes : list[UnitType]= utt.getUnitTypes()
        for unitType in unitTypes:
            print(unitType.getName())
            
        
    @staticmethod
    def testBuildPGS()->None:
        utt  = UnitTypeTable(2)
        name_map = "./maps/basesWorkers32x32A.xml"
        pgs :PhysicalGameState= PhysicalGameState.load(name_map,utt)
        print(pgs.getWidth(), pgs.getHeight())
        for u in pgs.getUnits().values():
            print(u.toString())
        
    @staticmethod
    def testBuildGS()->None:
        utt  = UnitTypeTable(2)
        name_map = "./maps/basesWorkers32x32A.xml"
        pgs :PhysicalGameState= PhysicalGameState.load(name_map,utt)
        gs = GameState(pgs,utt)
        screen = ScreenMicroRTS(gs)
        while True:
            screen.draw()
            print("up")
            time.sleep(0.5)