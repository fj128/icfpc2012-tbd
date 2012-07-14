from reachability_tests import reachability_tests
from stone_reachability_tests import stone_reachability_tests


def reachability_step(width, data):
    result = [False]*len(data)
    reachable = set()
    tasks = set([data.index('R')])
    
    auto_empty = [False]*len(data)
    # cells that can become empty even without robot intervention
    for i in reversed(range(len(data)-width)):
        cell = data[i]
        if cell == ' ':
            auto_empty[i] = True
        elif cell == '*':
            if auto_empty[i+width]:
                # fall down
                auto_empty[i] = True
            elif data[i+width] in '^*' and\
                 auto_empty[i+width-1] and (data[i+width-1] in ' *'):
                # fall left
                auto_empty[i] = True
            elif data[i+width] in '^*\\' and\
                 auto_empty[i+width+1] and (data[i+width+1] in ' *'):
                # fall right
                auto_empty[i] = True
                
    def make_reachable(i):
        reachable.add(i)
        result[i] = True
        for j in [i+1, i-1, i-width-1, i-width, i-width+1, i+width]:
            if j not in reachable:
                tasks.add(j)
    
    while tasks:
        i = tasks.pop()
        assert i not in reachable
        
        cell = data[i]
        if cell == 'R':
            make_reachable(i)
        elif cell in ' .\\' or auto_empty[i]:
            if i-1 in reachable or i+1 in reachable or\
               i+width in reachable or i-width in reachable:
                make_reachable(i)
        elif cell == '*':
            if i+width in reachable:
                # dig under
                make_reachable(i)
            elif i-1 in reachable and (i+1 in reachable or auto_empty[i+1]):
                # push right
                make_reachable(i)
            elif i+1 in reachable and (i-1 in reachable or auto_empty[i-1]):
                # push left
                make_reachable(i)
            elif data[i+width] in '*^\\' and\
                 (i+1 in reachable or auto_empty[i+1]) and\
                 (i+width+1 in reachable or auto_empty[i+width+1]):
                # fall right
                make_reachable(i)
            elif data[i+width] in '*^' and\
                 (i-1 in reachable or auto_empty[i-1]) and\
                 (i+width-1 in reachable or auto_empty[i+width-1]):
                # fall left
                make_reachable(i)
            
    return result


def stone_reachability_step(width, data):
    result = [False]*len(data)
    
    def make_reachable(i):
        if data[i] not in '#^LO':
            result[i] = True
    
    for i in range(width, len(data)-width, width):
        for j in range(i, i+width):
            if data[j] == '*':
                make_reachable(j-1)
                make_reachable(j)
                make_reachable(j+1)
            if result[j-width]:
                make_reachable(j)
        
        # push to the right            
        for j in range(i, i+width):
            if result[j] and\
               data[j+width] not in 'R ':
                make_reachable(j+1)
        
        #push to the left            
        for j in reversed(range(i, i+width)):
            if result[j] and\
               data[j+width] not in 'R ':
                make_reachable(j-1)
                
    return result


def parse_test(s):
    lines = s.split('\n')
    assert lines[0] == ''
    del lines[0]
    assert all(len(lines[0]) == len(line) for line in lines)
    width = len(lines[0])
    data = sum(map(list, lines), [])
    return width, data

def data_to_string(width, data):
    lines = []
    for i in range(0, len(data), width):
        lines.append(''.join(data[i:i+width]))
    return '\n'.join(lines)

   
def test_processing_step(tests, step):
    fails = 0
    for test, result in tests:
        print '-'*10
        print test
        width, data = parse_test(test)
        assert test == '\n'+data_to_string(width, data)
        
        
        reachable = step(width, data)
        
        print data_to_string(width, reachable)
        
        _, expected = parse_test(result)
        
        if expected != reachable:
            print 'fail, expected'
            print data_to_string(width, expected)
            fails += 1
            
    print '='*20
    print fails, 'fails'
    return fails
            
            
    
if __name__ == '__main__':
    def bool_to_01(b):
        return {False:'0', True:'1'}[b]
    def bool_step_to_01(step):
        return lambda w, h: map(bool_to_01, step(w, h))
    
    fails = 0
    fails += test_processing_step(reachability_tests, bool_step_to_01(reachability_step))
    
    fails += test_processing_step(stone_reachability_tests, bool_step_to_01(stone_reachability_step))
    
    print '/'*30
    print fails, 'fails total' 
