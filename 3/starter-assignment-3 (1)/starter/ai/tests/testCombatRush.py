
import time

from ai.rush.CombatRush import CombatRush
from game.gameState import GameState
from game.physicalGameState import PhysicalGameState
from game.screen import ScreenMicroRTS
from game.unitTypeTable import UnitTypeTable

class TesteCombatRush:

    @staticmethod
    def test0():
        utt = UnitTypeTable(2)
        map = "./maps/basesWorkers32x32A.xml"
        #pgs = PhysicalGameState.load("../maps/basesWorkers32x32A.xml",utt);
        #pgs = PhysicalGameState.load("../maps/mapadavid2.xml",utt);
        #pgs = PhysicalGameState.load("../maps/BWDistantResources32x32.xml",utt)
        pgs = PhysicalGameState.load(map,utt)
        gs = GameState(pgs,utt)
        ai0 = CombatRush(pgs,utt,"Light")
        ai1 = CombatRush(pgs,utt,"Heavy")
        screen = ScreenMicroRTS(gs)
        
        show = True
    
        while not gs.gameover() and gs.getTime()<30000:
            
            if show :
                screen.draw()
                time.sleep(0.1) 
 
            pa0 = ai0.getActions(gs,0)
            pa1 = ai1.getActions(gs,1)
            show = gs.updateScreen()
            gs.issueSafe(pa0)
            gs.issueSafe(pa1)
          
            gs.cycle()

        print("winner = ", gs.winner(), gs.getTime())


            

    