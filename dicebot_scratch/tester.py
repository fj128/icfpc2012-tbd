import worlds
import emulator
import solvers

import random
import time
import json
from itertools import chain

default_interpreter = emulator.interpret_main

def run_test(world_text, solver, interpretator):
    time1 = time.time()
    commands = solver.solve(world_text)
    time_taken = time.time() - time1
    score = interpretator(world_text, commands)
    
    return { 
            'score' : score,
            'time' : '{:f}'.format(time_taken),
            'solution_length' : len(commands),
            'solution' : commands
            }

def test_world_list(worlds):
    results = { }
    for world in worlds:
        results[world['name']] = {
            'meta' : {
                'width' : world['width'],
                'height' : world['height']
            },
            'stats_per_solver' : { solver.name : 
                run_test(world['source'], solver, default_interpreter) for solver in solvers.enumerate_all() 
            }
        }
    return results

def test_fuzzy(count, min_width = 5, max_width = 1000, min_height = 5, max_height = 1000):
    return test_world_list([ 
        worlds.create_one_random(random.randint(min_height, max_height),
                                 random.randint(min_width, max_width),
                                 {'mode' : 'chaotic'}
                                )
        for _ in range(count) 
    ])
    
def test_all_official():
    return test_world_list(worlds.load_official_worlds())
    
def test_basic_official():
    return test_world_list(worlds.load_official_basic_worlds())
    
def test_all():
    return test_world_list(chain( 
       worlds.create_some_random(amount = 3, height = 4, width = 5),
       worlds.load_official_worlds(),
       worlds.load_our_worlds()
    ))
    
if __name__ == '__main__':
    random.seed(42)
    #stats = test_fuzzy(2, max_width = 20, max_height = 30)
    stats = test_basic_official()
    print json.dumps(stats, indent=4, sort_keys = False)