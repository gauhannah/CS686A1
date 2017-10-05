import numpy 
import sys
import State
import scipy.spatial as sp
from collections import OrderedDict	
import copy
import heapq
import csv
import time

'''
	This program will solve all instances of the TSP for a given number of cities.
	The user is able to give input of the number of cities, and they will be returned 
	the result of each instance of the length specified

	For this program to work, the randTSP folder must be in the same folder as this file
'''

'''
	This function calculates the distance between the current node and the start node 
	for the purposes of computing the heuristic values while building the tour
'''
def calc_h(x_start, y_start, x_end, y_end):
	return sp.distance.euclidean([x_start, y_start], [x_end, y_end])
	# return 0 to run with h(x) = 0
	#return 0

'''
	This function calculates the euclidean distance between two points, this was
	left seperate from the calc_h function for readability in the code
'''
def calc_g(x_start, y_start, x_end, y_end):
	return sp.distance.euclidean([x_start, y_start], [x_end, y_end])


'''
	This function builds the list of all of the nodes and ensures that the input is correct
'''
def load_instance(path, startNode):
	allNodes = OrderedDict()
	numNodes = 0
	file = open(path, 'r')
	for line in file:
		tmp = line.split()
		if(len(tmp) == 1):
			numNodes = tmp[0]
		else:
			allNodes[tmp[0]] = {'x': int(tmp[1]), 'y': int(tmp[2])}
			allNodes[tmp[0]]['h'] = calc_h(int(tmp[1]), int(tmp[2]), allNodes[startNode]['x'], allNodes[startNode]['y'])
	if(len(allNodes) == int(numNodes)):
		return allNodes
	else: 
		print "input error, could not complete execution"
		sys.exit()



# Start Here
while True:
	# get user input for number of cities 
	inp = input('Please Enter the number of cities: ')
	if inp == 'q':
		quit()
	i = int(inp)
	if i < 1:
		print 'invalid input, please try again'
	elif i > 16:
		print 'invalid input, please try again'
	else:	
		# store run data
		data = []
		numAssigns = []
		for j in range(1,11):
			start = time.time()
			# build path 
			path = 'randTSP/' + str(i) + '/instance_' + str(j) + '.txt'
			startNode = 'A'
			allNodes = load_instance(path, startNode)
			# for readability
			x = 'x'
			y = 'y'
			h = 'h'
			numAssign = 0
			initState = State.State([startNode])
			openStates = []
			heapq.heappush(openStates, initState)
			if len(allNodes) == 1:
				goalState = 1
			else:
				goalState = len(allNodes) + 1
			currentState = openStates.pop()
			
			while True:
				if len(currentState.path) == goalState:
					print 'Shortest path: ' + str(currentState.path) + ' ' + str(currentState.g) + ' ' + str(currentState.h) + ' ' +  str(currentState.f) 
					print 'Found in ' + str(numAssign) + ' assignments'
					data.append([j, currentState.f, numAssign, str(currentState.path), currentState.g])
					numAssigns.append(numAssign)
					break;
				elif time.time() - start > 300:
					print 'did not terminate'
					print 'completed ' + str(numAssign) + ' assignments'
					data.append([j, currentState.f, numAssign, 'didNotTerminate', currentState.g])
					break;
				else: 
					for node in allNodes: 
						if node not in currentState.path:
							numAssign += 1
							tmpPath = copy.copy(currentState.path)
							tmpPath.append(node)
							if len(tmpPath) == len(allNodes):
								tmpPath.append(startNode)
								tmpState = State.State(tmpPath)
								# calculate g from the end of the current path to the next node
								g_tmp = calc_g(allNodes[currentState.path[len(currentState.path)-1]][x],allNodes[currentState.path[len(currentState.path)-1]][y],allNodes[node][x], allNodes[node][y])
								# calculate g from the next node added to the start node
								g_end = calc_g(allNodes[node][x], allNodes[node][y], allNodes[startNode][x], allNodes[startNode][y])
								tmpState.g = g_tmp + g_end + currentState.g
							else:
								tmpState = State.State(tmpPath)
								tmpState.g = currentState.g + calc_g(allNodes[currentState.path[len(currentState.path)-1]][x],allNodes[currentState.path[len(currentState.path)-1]][y],allNodes[node][x], allNodes[node][y])
							tmpState.h = allNodes[node][h] + (allNodes[currentState.path[len(currentState.path)-1]][h]) 
							tmpState.f = tmpState.g + tmpState.h
							heapq.heappush(openStates, tmpState)
					# get the smallest f value as the current node to be expanded
					currentState = heapq.heappop(openStates)
		
		#write data to a CSV value for the run
		myfile = open(str(i) + '_cities_assignments.csv', 'w') 
		with myfile:
			writer = csv.writer(myfile)
			writer.writerows(data)	

