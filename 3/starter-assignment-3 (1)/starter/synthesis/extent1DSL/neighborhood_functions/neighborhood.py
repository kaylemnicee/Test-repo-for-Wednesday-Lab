from synthesis.extent1DSL.util.Factory_E1 import Factory_E1
import random

class Neighborhood():
    def __init__(self):
        self._f = Factory_E1()

    def get_neighbors(self, prog, n_neighbors):
        l_progs = []
        for _ in range(n_neighbors):
            neighboor = prog.clone(self._f)
            l= []
            neighboor.countNode(l)
            no = l[random.randint(0, len(l)-1)]
            no.mutation(15)
            l_progs.append(neighboor)
        return l_progs