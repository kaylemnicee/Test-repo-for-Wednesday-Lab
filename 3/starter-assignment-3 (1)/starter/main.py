
import random
import time
from evaluators.SimpleSqrtEvaluationFunction3MultiState import SimpleSqrtEvaluationFunction3MultiState
from game.gameState import GameState
from game.physicalGameState import PhysicalGameState
from game.playerAction import PlayerAction
from game.screen import ScreenMicroRTS
from game.unitTypeTable import UnitTypeTable
from playout.simpleMatch import SimpleMatch
from synthesis.ai.Interpreter import Interpreter
from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.tests.scriptsToy import ScriptsToy
from synthesis.baseDSL.util.control import Control
from synthesis.baseDSL.util.factory_Base import Factory_Base
from synthesis.extent1DSL.neighborhood_functions.neighborhood import Neighborhood

class Program:
    def __init__(self, prog, best_eval, best_auxiliary, total_number_evaluations):
        self.prog = prog
        self.best_eval = best_eval
        self.best_auxiliary = best_auxiliary
        self.total_number_evaluations = total_number_evaluations
    
    def __repr__(self):
        return (f"Program(prog={str(self.prog)}, "
                f"best_eval={str(self.best_eval)}, "
                f"best_auxiliary={str(self.best_auxiliary)}, "
                f"total_number_evaluations={str(self.total_number_evaluations)})\n")

    def __lt__(self, other):
        # Compare by eval score; higher eval score is "greater"
        if self.best_eval != other.best_eval:
            return self.best_eval < other.best_eval
        # If eval scores are tied, compare by auxiliary score
        return self.best_auxiliary < other.best_auxiliary

    # Getter and Setter for prog
    def get_prog(self):
        return self.prog
    
    def set_prog(self, prog):
        self.prog = prog

    # Getter and Setter for best_eval
    def get_best_eval(self):
        return self.best_eval
    
    def set_best_eval(self, best_eval):
        self.best_eval = best_eval

    # Getter and Setter for best_auxiliary
    def get_best_auxiliary(self):
        return self.best_auxiliary
    
    def set_best_auxiliary(self, best_auxiliary):
        self.best_auxiliary = best_auxiliary

    # Getter and Setter for total_number_evaluations
    def get_total_number_evaluations(self):
        return self.total_number_evaluations
    
    def set_total_number_evaluations(self, total_number_eval):
        self.total_number_evaluations = total_number_eval


def playout(gs_a, ai0, ai1, player, max_tick, show_screen, assistant_evaluator):
    gs = gs_a.clone()
    ai0.reset()
    ai1.reset()
    if assistant_evaluator!=None: 
        assistant_evaluator.reset()

    if show_screen:
        screen = ScreenMicroRTS(gs)
    show = True
    
    while not gs.gameover() and gs.getTime()<max_tick:
        if assistant_evaluator!=None:
            assistant_evaluator.analysis(gs,player,False)
        if show and show_screen:
                screen.draw()
                time.sleep(0.1) 

        ini_time = time.time()
        try:
            pa0 :  PlayerAction =ai0.getActions(gs,player)
        except Exception as e:
            return 1-player  , -1
        timeP0 = time.time()- ini_time
        
        ini_time = time.time()  
        pa1 = ai1.getActions(gs,1 -player)
        timeP1 = time.time()- ini_time
        
        if timeP0>0.110 and timeP1>0.110:
            return -1,-1
        elif timeP0>0.110 :
            return 1- player,-1
        elif timeP1>0.110:
            return player,-1
        
        if show_screen: show = gs.updateScreen()
            
        gs.issueSafe(pa0)
        gs.issueSafe(pa1)      
        gs.cycle()
    if assistant_evaluator!=None:
        assistant_evaluator.analysis(gs,player,True)
        
    if assistant_evaluator!=None:   

        return gs.winner() ,assistant_evaluator.getValue()
    
    return gs.winner(), 0

def winToScore(player, result):
    if player == result: return 1.0
    if 1 - player == result: return 0.0
    return 0.5

def evaluate(node, target_program, gs, max_tick):
    eval = SimpleSqrtEvaluationFunction3MultiState()
    utt = gs.getUnitTypeTable()
    a1 = Interpreter(gs.getPhysicalGameState(),utt,node)
    score = 0
    
    a2 = Interpreter(gs.getPhysicalGameState(),utt,target_program)
    win, auxiliary_score0 = playout(gs,a1,a2,0,max_tick,False,eval)
    score += winToScore(0, win)
    win, auxiliary_score1 = playout(gs,a1,a2,1,max_tick,False,eval)
    score += winToScore(1, win)

    return score/2,(auxiliary_score0+auxiliary_score1)/2

def visualize_game(program_1, program_2):
    utt = UnitTypeTable(2)
    pgs = PhysicalGameState.load(map, utt)
    gs = GameState(pgs, utt)

    symbolic_1 = Interpreter(pgs, utt, program_1)
    symbolic_2 = Interpreter(pgs, utt, program_2)
    
    sm = SimpleMatch()
    win = sm.playout(gs, symbolic_1, symbolic_2, 0, 7000, True)

    print("Winner = ", win[0] + 1)

def search(target_program, neighborhood_function, num_neighbors, max_tick, map):
    utt = UnitTypeTable(2)
    pgs = PhysicalGameState.load(map, utt)
    gs = GameState(pgs, utt)
    found_optimal = False
    random_restart = True
    candidates = []
    total_number_evaluations = 0

    while not found_optimal:
        start_time = time.time()
        # 50% chance: continue from best candidate, else random restart
        if random.random() < 0.5 and candidates:
            print("\n\tCase 1: Improving on best candidate")
            program = max(candidates, key=lambda x: (x.best_eval, x.best_auxiliary))
            prog = program.prog
            print("\t\tContinuing from best candidate:", program)
        else:
            print("\n\tCase 2: Random restart")
            prog = ScriptsToy.scriptEmpty()

        best_eval, best_auxiliary = evaluate(prog, target_program, gs, max_tick)
        print("\tInitial evaluation score:", best_eval, ", Auxiliary:", best_auxiliary)
        improved = True

        while improved and best_eval < 1.0:
            improved = False
            print("\n\tNEWLOOP: Hill climbing with", num_neighbors, "neighbors")
            start_time_neighbors = time.time()
            neighbors = neighborhood_function.get_neighbors(prog, num_neighbors)
            elapsed_time_neighbors = time.time() - start_time_neighbors
            print(f"\t\tGenerated neighbors in {elapsed_time_neighbors:.4f} seconds")

            for neighbor in neighbors:
                start_time_eval = time.time()
                eval_score, aux_score = evaluate(neighbor, target_program, gs, max_tick)
                elapsed_time_eval = time.time() - start_time_eval
                print(f"\t\tEvaluated neighbor in {elapsed_time_eval:.4f} seconds")

                total_number_evaluations += 1

                # Update best scores if neighbor is better
                if eval_score > best_eval or (eval_score == best_eval and aux_score > best_auxiliary):
                    print("\t\t\tFound new best --> Eval:", eval_score, ", Aux:", aux_score)
                    prog = neighbor
                    best_eval = eval_score
                    best_auxiliary = aux_score
                    improved = True

                # Stop search if optimal solution found
                if best_eval == 1.0:
                    found_optimal = True
                    print("\nSolution found! Exiting.")
                    break

            if not improved:
                print("\t\tNo improvement from hill climbing")
                if random_restart:
                    candidates.append(Program(prog, best_eval, best_auxiliary, total_number_evaluations))

        elapsed_time_search = time.time() - start_time
        print(f"\tIteration completed in {elapsed_time_search:.4f} seconds")

    return prog, total_number_evaluations


if __name__ == "__main__":
    random.seed(23)

    max_tick = 3000
    neighborhood_function = Neighborhood()
    num_neighbors = 20
    map = "./maps/basesWorkers32x32A.xml"
    factory = Factory_Base()

    program_target_1 = ScriptsToy.script7()

    start_time = time.time()
    print('Program 1 to be Defeated')
    print(program_target_1.translate())
    print()
    prog_result, number_evaluations = search(program_target_1, neighborhood_function, num_neighbors, max_tick, map)
    print('Number of evaluations: ', number_evaluations)
    end_time = time.time()
    print('Time required to compute a best response to the first program: ', end_time - start_time)
    visualize_game(prog_result, program_target_1)
    print()

    start_time = time.time()
    program_target_string = "S;For_S;S;S_S;S;S_S;S;C;Build;Barracks;Down;2;S;C;Attack;Closest;S;C;Train;Ranged;Right;15"
    program_target_2 = Control.load(program_target_string, factory)
    print('Program 2 to be Defeated')
    print(program_target_2.translate())
    print()
    prog_result, number_evaluations = search(program_target_2, neighborhood_function, num_neighbors, max_tick, map)
    end_time = time.time()
    print('Time required to compute a best response to the second program: ', end_time - start_time)
    print('Number of evaluations: ', number_evaluations)
    visualize_game(prog_result, program_target_2)
