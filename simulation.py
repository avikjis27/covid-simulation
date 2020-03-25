import matplotlib.pyplot as plt
import numpy as np
import random
import time

def spread_covid(X):
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
					X[0][rowid][colid] = 1
			if X[0][rowid][colid] == 1:
				death_chance = random.randint(1,100)
				if death_chance < 3 and X[1][rowid][colid] >= 7:
					X[2][rowid][colid] = death_code
					X[0][rowid][colid] = 0
				if death_chance >=3 and X[1][rowid][colid] >= 14:
					X[2][rowid][colid] = immune_code
					X[0][rowid][colid] = 0
	return X


if __name__ == "__main__":
	
	n = 22
	X = np.zeros([3,n,n],int)
	
	X[0][3][3] = 1
	X[0][4][6] = 1
	fig=plt.figure()
	for day in range(1,100):
		plt.title(f"Day-{day}")
		plt.imshow(X[0][0:][0:], cmap="gray")
		plt.show(block=False)
		plt.pause(1)
		X = spread_covid(X)

	plt.show(block=False)
	plt.title(f"Total Death and recovered")
	plt.imshow(X[2][0:][0:], cmap="gray")
	plt.show()

	

			




