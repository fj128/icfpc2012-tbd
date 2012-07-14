from collections import defaultdict
import itertools

class ScoreEstimator(object):
	def __init__(self, data):
		self.lambdas, self.lift, self.simple_map = simplify(data)
		
		self.distances = defaultdict(lambda: {})
		
		points = self.lambdas + [self.lift]
		while points:
			source = points.pop()
			distances = self.distances_from_source(source, points)
			for (point, distance) in distances.items():
				self.distances[point][source] = distance
				self.distances[source][point] = distance
		
	def distances_from_source(self, source, targets):
		''' Compute grid distances from source to targets.
			Assumes that each target is marked on the map. ''' 
		distances = {}
	
		old_front = set()
		front = set([source])
	
		step = 0
		while len(distances) < len(targets):
			step += 1
			new_front = set()
			for (i, j) in front:
				new_front |= set([(i+1, j), (i,j+1), (i-1,j), (i,j-1)])
			new_front = new_front - front - old_front
			
			new_front = set(point for point in new_front if self.simple_map[point] != '#') 
			for point in new_front:
					if self.simple_map[point] == 'x':
						if point in targets and point not in distances:
							distances[point] =  step
			old_front = front
			front = new_front
		return distances
					
	def estimate(self, lambdas_collected, robot):
		''' Estimate maximum achievable score.
			Currently assumes that we won't stop prematurely. '''
		lambdas_remaining = set(self.lambdas) - set(lambdas_collected)
		distances_from_robot = self.distances_from_source(robot, \
														list(lambdas_remaining) + [self.lift])
		
		tour_length = self.find_tour(lambdas_remaining, robot, distances_from_robot)
		
		return -tour_length + 75 * len(self.lambdas)
		
	def find_tour(self, lambdas_remaining, robot, distances_from_robot):
		# nearest neighbour
		# placeholder code
		# untested
		points_remaining = set(lambdas_remaining)
		
		tour_length = 0
		
		last_point = self.lift
		while points_remaining:
			weight = lambda point: self.distances[last_point][point]
			distance_to_next, next_point = argmin(weight, points_remaining)
			tour_length += distance_to_next
			points_remaining.remove(next_point)
			last_point = next_point
		tour_length += distances_from_robot[last_point]
		return tour_length
			
	def debug_print(self):
		inf = 10**6
		x1, y1 = inf, inf
		x2, y2 = -inf, -inf
		for (x, y) in self.simple_map:
			x1 = min(x1, x)
			x2 = max(x2, x)
			y1 = min(y1, y)
			y2 = max(y2, y)

		lambda_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		for y in xrange(y1, y2+1):
			line = ''		
			for x in xrange(x1, x2+1):
				if (x, y) not in self.lambdas:
					line += self.simple_map[x, y]
				else:
					line += lambda_symbols[self.lambdas.index((x,y))]
			print line
		print
		for i in xrange(len(self.lambdas)):
			for j in xrange(i+1, len(self.lambdas)):
				print "%s to %s: %d" % (lambda_symbols[i], lambda_symbols[j], \
									self.distances[self.lambdas[i]][self.lambdas[j]])
		
	
def simplify(data):
	''' Reduce map to walls, lambdas and lift. '''
	# TODO: replace this with something that doesn't insert missing values
	simple_map = defaultdict(lambda: ' ')
	
	lambdas = []
	
	for (point, value) in data.items():
			if value == '#':
				simple_map[point] = '#'
			elif value in ['L', 'O']:
				simple_map[point] = 'x'
				lift = point	
			elif value == '\\':
				simple_map[point] = 'x'
				lambdas.append(point)
	return (lambdas, lift, simple_map)

argmin = lambda funct, items: min(itertools.izip(itertools.imap(funct, items), items))

if __name__ == '__main__':
	import game
	map_name = 'contest10'
	m = game.Map.load_file('../data/sample_maps/{}.map'.format(map_name))
	
	benchmark = False
	#benchmark = True
	if benchmark:
		# crappy benchmark
		for i in xrange(50):
			estimator = ScoreEstimator(m.data)
	else:
		# crappy unit test
		estimator = ScoreEstimator(m.data)
		contest10_distances = [(1, 16), (2, 9), (2, 16), (3, 9), (3, 19), (3, 20), (3, 21), (4, 9), (4, 18), (4, 21), (5, 4), (5, 5), (5, 7), (5, 19), (5, 20), (6, 4), (6, 5), (6, 7), (6, 20), (7, 4), (7, 5), (7, 20), (8, 4), (8, 5), (14, 4), (15, 4), (16, 10), (16, 13), (17, 11), (17, 15), (19, 11), (20, 11), (20, 19), (21, 6), (21, 20), (22, 3), (22, 4), (22, 6), (22, 20), (23, 3), (23, 6), (24, 3), (24, 6), (25, 3), (25, 20), (26, 12), (27, 0), (27, 4), (27, 5), (27, 6), (27, 12), (27, 22)]
		assert(sorted(estimator.distances) == contest10_distances)
		
		estimator.estimate(set(), (0,0))