import random
import re

import backtrack
import genetic
import world

class fuzz_solver:
    def __init__(self):
        self.name = 'fuzzy'
    
    def solve(self, src, filename):
        actions = [ 'L', 'R', 'U', 'D', 'W' ]
        solution = ''        
        for _ in range(random.randint(1, len(src))):
            solution += random.choice(actions)
        return solution
    
    pass

class vlad_solver:
    def __init__(self):
        self.name = 'Vlad'
    
    def solve(self, src, filename):
        world_obj = world.World.from_string(src)
        _, solution = backtrack.solve(world_obj)
        return solution
        
    pass

class drw_solver:
    def __init__(self):
        self.name = 'DRW'
    
    def solve(self, src,  filename):
        world_obj = world.World.from_string(src)
        solver = genetic.GeneticSolver(world_obj)
        solution = 'A' # solver.solve()
        return solution

    pass

class predefined_solver:
    def __init__(self):
        self.name = 'manual'
        self.solution_srcs = open('../data/maps_manual/scores', "r").read()
        lines = self.solution_srcs.split()
        self.solutions = { }
        current_map = 'null'
        for line in lines:
            if line == '':
                current_map = 'null'            
            elif line.startswith('Path: '):
                self.solutions[current_map] = re.search("Path: (.*)", line).group(0)
            elif not line.startswith('Score'):                
                current_map = line
    
    def solve(self, src, filename):
        if filename in self.solutions.iterkeys():
            return self.solutions[filename]
        else:
            return None

    pass
