import matplotlib.pyplot as plt
from bitarray import bitarray
import numpy as np
import random
import time
import sys

def spread_covid19(X):
	day_positive,day_recovered,day_deceased = 0,0,0
	death_code = 2
	immune_code = 3
	healthy_code = 0
	sick_code = 1
	incubation_period = 2
	page, row, col	 = X.shape
	for rowid in range(1, row-1):
		for colid in range(1, col-1):
			if X[2][rowid][colid] == immune_code or X[2][rowid][colid] == death_code:
				continue
			if X[0][rowid][colid] == 1:
				X[1][rowid][colid] = X[1][rowid][colid] + 1 
			covid_cell = 0
			if X[1][rowid-1][colid]>incubation_period and X[0][rowid-1][colid] == 1:
				covid_cell += 1 
			if X[1][rowid+1][colid]>incubation_period and X[0][rowid+1][colid] == 1:
				covid_cell += 1 
			if X[1][rowid][colid+1]>incubation_period and X[0][rowid][colid+1] == 1:
				covid_cell += 1 
			if X[1][rowid][colid-1]>incubation_period and X[0][rowid][colid-1] == 1:
				covid_cell += 1 
			if X[1][rowid-1][colid+1]>incubation_period and X[0][rowid-1][colid+1] == 1:
				covid_cell += 1 
			if X[1][rowid-1][colid-1]>incubation_period and X[0][rowid-1][colid-1] == 1:
				covid_cell += 1 
			if X[1][rowid+1][colid-1]>incubation_period and X[0][rowid+1][colid-1] == 1:
				covid_cell += 1 
			if X[1][rowid+1][colid+1]>incubation_period and X[1][rowid+1][colid+1] == 1:
				covid_cell += 1 
			
			if covid_cell > 0 and X[0][rowid][colid] == 0:
				infection_chance = random.randint(1,100)
				if infection_chance <= 25:
					X[0][rowid][colid] = sick_code
					day_positive = day_positive + 1
			if X[0][rowid][colid] == 1:
				death_chance = random.randint(1,100)
				if death_chance < 3 and X[1][rowid][colid] >= 14:
					X[2][rowid][colid] = death_code
					X[0][rowid][colid] = 0
					day_deceased = day_deceased + 1
				if death_chance >=3 and X[1][rowid][colid] >= 16:
					X[2][rowid][colid] = immune_code
					X[0][rowid][colid] = 0
					day_recovered = day_recovered + 1
	return X, day_positive,day_recovered,day_deceased


def visualize(plt, title):
	plt.title(title)
	plt.imshow(X[0][0:][0:], cmap="gray")
	plt.show(block=False)
	input()

if __name__ == "__main__":
	random.seed(sys.argv[1]) 
	n = int(sys.argv[2])+2
	total_day_to_observe = int(sys.argv[3])
	X = np.zeros([3,n,n],int)
	X[0][int(n/2)][int(n/2)] = 1
	fig=plt.figure()
	total_positive,total_recovered,total_deceased,total_active = 0,0,0,0
	for day in range(1,total_day_to_observe):
		X, day_positive,day_recovered,day_deceased = spread_covid19(X)
		total_positive = total_positive + day_positive
		total_deceased = total_deceased + day_deceased
		total_recovered = total_recovered + day_recovered
		total_active = total_positive-total_recovered
		
	visualize(plt, f"Day-{day}| positive: {total_positive}, active: {total_active}, recovered: {total_recovered}, deceased: {total_deceased}")

			




