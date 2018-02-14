
"""
@author Dillon Carns SOM in python
@version 2/14/2018
"""
import numpy as np
import matplotlib.pyplot as plt
import csv

"""
Global parameters
"""
N = 20 # linear size of 2D map
n_teacher = 10000 # # of teacher signal
np.random.seed(100)# test seed for random number

def main():
	colors = []
	with open('chords.csv') as csvfile:
    		readCSV = csv.reader(csvfile, delimiter=',')
    		next(readCSV, None) #skip headers
    		for row in readCSV:
        		colors.append(row)

	#got all values into 12 vectors!
	teachers = np.zeros((24,12))
	for i in range(0, 24):
		for j in range(0, 12):	
			teachers[i][j] = colors[i][j+1]
		teachers[i] = i
	# initialize node vectors
	nodes = np.random.rand(N,N,12) # node array. each node has 12-dim weight vector
	#initial out put
	#TODO; make out put function to simplify here 
	plt.scatter(nodes[0][0][:], nodes[0][0][:])
	for i in range(12):
		plt.annotate(colors[i][0], (nodes[0][0][i], nodes[0][0][i]))
	plt.savefig("scatter.pdf")
	""""""
	""" Learning """
	""""""
	# teacher signal
	teachers = np.random.rand(n_teacher,12)
	for i in range(n_teacher):
		train(nodes, teachers, i)
	#output
	plt.imshow(nodes[:][:][0], interpolation='nearest')
	plt.savefig("CM.pdf")
	plt.imshow(nodes[:][:][1], interpolation='nearest')
	plt.savefig("Csharp.pdf")
    
def train(nodes, teachers, i):
	bmu = best_matching_unit(nodes, teachers[i])
	#print bmu
	for x in range(N):
		for y in range(N):
			c = np.array([x,y])# coordinate of unit
			d = np.linalg.norm(c-bmu)
			L = learning_ratio(i)
			S = learning_radius(i,d)
			for z in range(12): #TODO clear up using numpy function
				nodes[x,y,z] += L*S*(teachers[i,z] - nodes[x,y,z])



def best_matching_unit(nodes, teacher):
	#compute all norms (square)
	#TODO simplify using numpy function
	norms = np.zeros((N,N))
	for i in range(N):
		for j in range(N):
			for k in range(12):
				norms[i,j] += (nodes[i,j,k] - teacher[k])**2
	#then, choose the minimum one
	bmu = np.argmin(norms) #argment with minimum element 
	# argmin returns just flatten, serial index, 
	# so convert it using unravel_index
	return np.unravel_index(bmu,(N,N))

def neighbourhood(t):#neighbourhood radious
	halflife = float(n_teacher/4) #for testing
	initial  = float(N/2)
	return initial*np.exp(-t/halflife)

def learning_ratio(t):
	halflife = float(n_teacher/4) #for testing
	initial  = 0.02
	return initial*np.exp(-t/halflife)

def learning_radius(t, d):
	# d is distance from BMU
    	s = neighbourhood(t)
    	return np.exp(-d**2/(2*s**2))

main()
