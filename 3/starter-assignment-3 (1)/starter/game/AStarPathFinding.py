

from game.gameState import GameState
from game.resourceUsage import ResourceUsage
from game.unit import Unit
from game.unitAction import UnitAction

import numpy as np
class AStarPathFinding:

    


    def __init__(self, a_width:int,  height : int):
        self._w : int = a_width;
        self._h : int = height; 
        self._free : list[list[bool]] = np.array((self._w,self._h),dtype=bool)    #[[None for i in range(self._w)] for j in range(self._h)]
        self._closed : list[int] = np.zeros((self._w*self._h),dtype=np.int16)# [0 for _ in range(self._w*self._h)]
        self._open : list[int] =  np.zeros((self._w*self._h),dtype=np.int16)   # open list
        self._heuristic : list[int] = np.zeros((self._w*self._h),dtype=np.int16)    # heuristic value of the elements in 'open'
        self._parents : list[int] = np.zeros((self._w*self._h),dtype=np.int16)  #[0 for _ in range(self._w*self._h)]
        self._cost : list[int] = np.zeros((self._w*self._h),dtype=np.int16)  # [0 for _ in range(self._w*self._h)]     # cost of reaching a given position so far
        self._inOpenOrClosed : list[int] = np.zeros((self._w*self._h),dtype=np.int16)# [0 for _ in range(self._w*self._h)]
        self._openinsert : int = 0;
       
    
    def clear(self,gs :GameState)->None:
        self._free = gs._free
        self._closed[:] = -1;
        self._inOpenOrClosed[:] = 0;
     
        

    #This fucntion finds the shortest path from 'start' to 'targetpos' and then returns
    # a UnitAction of the type 'actionType' with the direction of the first step in the shorteet path
    def findPath(self, start : Unit,  targetpos : int, gs: GameState)->UnitAction:
       return self.findPathToPositionInRange(start, targetpos, 0, gs);
    
    #This function is like the previous one, but doesn't try to reach 'target', but just to
    # reach a position that is at most 'range' far away from 'target'
    def findPathToPositionInRange(self, start:Unit,  targetpos : int,  rangev : int, gs : GameState)->UnitAction:
         self.clear(gs);
         pgs = gs.getPhysicalGameState();
     
         targetx : int = int(targetpos % self._w);
         targety  : int= int(targetpos / self._w);
         
         sq_range : int = rangev * rangev;
         startPos  : int= start.getY() * self._w + start.getX();


         self._openinsert = 0;
         self._open[self._openinsert] = startPos;
         self._heuristic[self._openinsert] = self.manhattanDistance(start.getX(), start.getY(), targetx, targety);
         self._parents[self._openinsert] = startPos;
         self._inOpenOrClosed[startPos] = 1;
         self._cost[startPos] = 0;
         self._openinsert+=1

         cont=0
         while self._openinsert > 0:
             cont+=1
             dx= abs(start.getX()-targetx )
             dy =abs(start.getY()-targety )
             if cont > (dx+dy)*2:
                 return  UnitAction.build_None()
             self._openinsert-=1
             pos : int  = self._open[self._openinsert];
             parent : int = self._parents[self._openinsert];
             
             if self._closed[pos] != -1: continue;

             self._closed[pos] = parent;

             x : int = int(pos % self._w);
             y : int = int(pos / self._w);
             #if start.getPlayer() == 0:
             #    print("pos",x,y)
             if ((x - targetx) * (x - targetx) + (y - targety) * (y - targety)) <= sq_range:
                 #path found, backtrack:
                 last : int = pos;
                 #System.out.println("- Path from " + start.getX() + "," + start.getY() + " to " + targetpos%w + "," + targetpos/w + " (range " + range + ") in " + iterations + " iterations");
                 while parent != pos:
                     last = pos;
                     pos = parent;
                     parent = self._closed[pos];
            
                     #System.out.println("    " + pos%w + "," + pos/w);
                 
                 if last == pos + self._w: return  UnitAction.build_Move( UnitAction.DIRECTION_DOWN);
                 if last == pos - 1: return  UnitAction.build_Move( UnitAction.DIRECTION_LEFT);
                 if last == pos - self._w: return  UnitAction.build_Move( UnitAction.DIRECTION_UP);
                 if last == pos + 1: return  UnitAction.build_Move( UnitAction.DIRECTION_RIGHT);
                 return  UnitAction.build_None()
             
             if y > 0 and self._inOpenOrClosed[pos -  self._w] == 0:
                
                #if self._free[x][y - 1] == None: self._free[x][y - 1] = gs.free(x, y - 1);
                
                if  self._free[x][y - 1]:
                    #if start.getPlayer() == 0:print("ok0",self.manhattanDistance(x, y - 1, targetx, targety))
                    self.addToOpen(x, y - 1, pos -  self._w, pos,  self.manhattanDistance(x, y - 1, targetx, targety));

             if x < pgs.getWidth() - 1 and  self._inOpenOrClosed[pos + 1] == 0:
                #if  self._free[x + 1][y] == None:  self._free[x + 1][y] = gs.free(x + 1, y);
                 
                if  self._free[x + 1][y]:
                    #if start.getPlayer() == 0:print("ok1",self.manhattanDistance(x + 1, y, targetx, targety))
                    self.addToOpen(x + 1, y, pos + 1, pos,  self.manhattanDistance(x + 1, y, targetx, targety));
                 
             
             if y < pgs.getHeight() - 1 and  self._inOpenOrClosed[pos +  self._w] == 0:
                #if  self._free[x][y + 1] == None:  self._free[x][y + 1] = gs.free(x, y + 1);
               
                if  self._free[x][y + 1]:
                    #if start.getPlayer() == 0: print("ok2",self.manhattanDistance(x, y + 1, targetx, targety))
                    self.addToOpen(x, y + 1, pos +  self._w, pos,  self.manhattanDistance(x, y + 1, targetx, targety));
            

             if x > 0 and  self._inOpenOrClosed[pos - 1] == 0:
                #if  self._free[x - 1][y] == None:  self._free[x - 1][y] = gs.free(x - 1, y);
               
                if  self._free[x - 1][y] :
                    #if start.getPlayer() == 0:print("ok3",self.manhattanDistance(x - 1, y, targetx, targety)) 
                    self.addToOpen(x - 1, y, pos - 1, pos,  self.manhattanDistance(x - 1, y, targetx, targety));
        
         return UnitAction.build_None()

      

    #virtual Pair<Integer, Integer> findPathToPositionInRange2(Unit start, int targetpos, int range, GameState gs);


    
    # This function is like the previous one, but doesn't try to reach 'target', but just to
    # reach a position adjacent to 'target'
     
   
    def shift5(self,arr, num, fill_value=np.nan):
        result = np.empty_like(arr)
        if num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:
            result[:] = arr
        return result

   
    #and keep the "open" list sorted:
    def addToOpen(self, x:int,  y : int, newPos:int, oldPos : int,  h : int)->None:
        self._cost[newPos] = self._cost[oldPos] + 1;

         # find the right position for the insert:
        
        for i in range(self._openinsert - 1,-1,-1):
             
             if self._heuristic[i] + self._cost[self._open[i]] >= h + self._cost[newPos]:
                #System.out.println("Inserting at " + (i+1) + " / " + openinsert);
                #shift all the elements:
                self._open[i+1:self._openinsert+2] = self._open[i:self._openinsert+1]
                self._heuristic[i+1:self._openinsert+2] = self._heuristic[i:self._openinsert+1]
                self._parents[i+1:self._openinsert+2] = self._parents[i:self._openinsert+1]
                #for j in range(self._openinsert,i,-1):
                     #self._open[j] = self._open[j - 1];
                     #self._heuristic[j] = self._heuristic[j - 1];
                     #self._parents[j] = self._parents[j - 1];
                 

                 #insert at i+1:
                self._open[i + 1] = newPos;
                self._heuristic[i + 1] = h;
                self._parents[i + 1] = oldPos;
                self._openinsert+=1;
                self._inOpenOrClosed[newPos] = 1;
                return;

        self._open[1:self._openinsert+2] = self._open[:self._openinsert+1]
        self._heuristic[1:self._openinsert+2] = self._heuristic[:self._openinsert+1]
        self._parents[1:self._openinsert+2] = self._parents[:self._openinsert+1]
        #for j in range(self._openinsert,0,-1): 
             #self._open[j] = self._open[j - 1];
             #self._heuristic[j] = self._heuristic[j - 1];
             #self._parents[j] = self._parents[j - 1];


         #insert at i+1:
        self._open[0] = newPos;
        self._heuristic[0] = h;
        self._parents[0] = oldPos;
        self._openinsert+=1
        self._inOpenOrClosed[newPos] = 1;

    def manhattanDistance(self, x:int ,  y:int,  x2:int,  y2:int)->int:
        return abs(x - x2) + abs(y - y2);

    def findPathToAdjacentPosition(self, start : Unit,  targetpos : Unit,  gs :GameState)->UnitAction:
        return self.findPathToPositionInRange(start, targetpos, 1, gs);