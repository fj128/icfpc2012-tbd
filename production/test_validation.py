from time import sleep

from game import validate as local_validate
from webvalidator import validate


def main():
    tests = [
        ('flood1', 'LLLLDDDDDWWWWUUUWWWWWW'), # surface barely in time
        ('flood1', 'LLLLDDDDDWWWWWWWWWWWW'), # drowning
        ('flood1', 'W'*100), # passive drowning
             
        ('contest1', 'LDRDDULULLDD'), # complete solution
        ('contest8', 'WWWRRRLLLWWWA'), # abort or death?
        
        # write your own tests, especially for interesting cases
        
        # note that these tests are expensive unless we implement some form
        # of server results caching
        ]
    
    for i, test in enumerate(tests):
        if i > 0:
            sleep(60)
        print '{}% {}'.format(100*(i+1)//len(tests), test),
        local = local_validate(*test)
        web = validate(*test)
        if local == web:
            print 'ok (score {})'.format(local[0])
        else:
            print 'FAIL !!!!!!!'
            print 'local:'
            print local[0]
            print local[1]
            print 'theirs:'
            print web[0]
            print web[1]


if __name__ == '__main__':
    main()