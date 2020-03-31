import matplotlib.pyplot as plt
import numpy as np
import random
import time
import sys

#class covid19

DEATH_CODE = 4
IMMUNE_CODE = 3
SICK_CODE = 2
ASYMPTOMATIC_CODE = 1
HEALTHY_CODE = 0

FREE = 0
ISOLATION = 1
# After 11 days.https://www.sciencedaily.com/releases/2020/03/200317175438.htm

# Possible Halth states transition	
# HEALTHY -> ASYMPTOMATIC -> SICK -> DEATH or IMMUNE
								
H = None # Health plane, possible value HEALTHY(0), ASYMPTOMATIC(1), SICK(2), DEATH(4), IMMUNE(3)
Q = None # Quarantine plane, possible value ISOLATION(1), FREE(0)
A = None # Age plane, possible value Infant 0-5years(0), Young 5-14years(1), Adult 15-29(2), Mid aged 29-59(3), Old above 60(4) Refer demographic data of India https://en.wikipedia.org/wiki/Demographics_of_India 
D = None # Day passed after infection 0 - 30
ICU = None # No of ICUs available
#ISOLATION = None # No of ISOLATION units available

total_positive, total_recovered, total_deceased, total_active = 0,0,0,0
total_positive_arr=[]
total_recovered_arr=[]
total_deceased_arr=[]
day_wise_count=[]
day_wise_recovered=[]
day_wise_deceased=[]


def create_population(grid_length, stage):
	global H, Q, A, D
	n = grid_length + 2
	A = np.random.choice([0,1,2,3,4], size=(n,n), p=[0.1,0.2,0.4,0.22,0.08])
	Q = np.zeros([n,n],int)
	D = np.zeros([n,n],int)
	if stage == 1:
		H = np.random.choice([0,1], size=(n,n), p=[0.99,0.01])
		np.put(Q, [0,1,2,3,4], [0,0,0,0,1])
		np.put(D, [0,1], [0,1])
	if stage == 2:
		H = np.random.choice([0,1], size=(n,n), p=[0.96,0.04])
		np.put(Q, [0,1,2,3,4], [0,0,1,1,1])
		np.put(D, [0,1], [0,3])
	if stage == 3:
		H = np.random.choice([0,1,2], size=(n,n), p=[0.9,0.08,0.02])
		np.put(Q, [0,1,2,3,4], [0,0,1,1,1])
		np.put(D, [0,1,2], [0,3,5])
	if stage == 4:
		H = np.random.choice([0,1,2], size=(n,n), p=[0.8,0.15,0.05])
		np.put(Q, [0,1,2,3,4], [1,1,1,2,2])
		np.put(D, [0,1,2], [0,4,6])

def gather_data(day_positive, day_recovered, day_deceased):
	global total_positive, total_deceased, total_recovered, total_active 
	total_positive = total_positive + day_positive
	total_positive_arr.append(total_positive)
	day_wise_count.append(day_positive)

	total_deceased = total_deceased + day_deceased
	day_wise_deceased.append(day_deceased)
	total_deceased_arr.append(total_deceased)
	
	total_recovered = total_recovered + day_recovered
	total_recovered_arr.append(total_recovered)
	day_wise_recovered.append(day_recovered)

	total_active = total_positive - total_recovered

def draw_picture(data, title, subplot_cor):
	plt.subplot(subplot_cor[0],subplot_cor[1],subplot_cor[2])
	plt.title(title)
	plt.imshow(data, cmap="gray")

def draw_graph(data_map, title, subplot_cor):
	plt.subplot(subplot_cor[0],subplot_cor[1],subplot_cor[2])
	plt.title(title)
	for key in data_map:
		plt.plot(data_map[key], label=key)
	plt.legend()

def visualize():
	global total_positive, total_deceased, total_recovered, total_active 
	aggregate_data = {
		"total_positive": total_positive_arr,
		"total_deceased": total_deceased_arr,
		"total_recovered": total_recovered_arr
	}
	daily_data = {
		"daily_positive": day_wise_count,
		"daily_deceased": day_wise_deceased,
		"daily_recovered": day_wise_recovered
	}
	plt.figure()
	draw_picture(H[0:][0:], f"Day-{day}| positive: {total_positive}, active: {total_active}, recovered: {total_recovered}, deceased: {total_deceased}", (2,2,1))
	draw_graph(aggregate_data, "Aggregate data", (2,2,3))
	draw_graph(daily_data, "Per day data",(2,2,4))	
	plt.show()
	plt.close()

def spread_covid19():
	global H, Q, A, D, incubation_period
	day_positive,day_recovered,day_deceased = 0,0,0
	incubation_period = 2
	row, col = H.shape
	for rowid in range(1, row-1):
		for colid in range(1, col-1):
			if H[rowid][colid] == IMMUNE_CODE or H[rowid][colid] == DEATH_CODE:
				continue
			if H[rowid][colid] in (1, 2):
				D[rowid][colid] = D[rowid][colid] + 1 
			
			covid_cell = 0
			if (H[rowid-1][colid] in (1,2) and Q[rowid-1][colid] == 0) or (H[rowid+1][colid] in (1,2) and Q[rowid+1][colid] == 0) or (H[rowid][colid+1] in (1,2) and Q[rowid][colid+1] == 0) or (H[rowid][colid-1] in (1,2) and Q[rowid][colid-1] == 0) or (H[rowid-1][colid+1] in (1,2) and Q[rowid-1][colid+1] == 0) or (H[rowid-1][colid-1] in (1,2) and Q[rowid-1][colid-1] == 0) or (H[rowid+1][colid-1] in (1,2) and Q[rowid+1][colid-1] == 0) or (H[rowid+1][colid+1] in (1,2) and Q[rowid+1][colid+1] == 0) :
				covid_cell = 1 
			
			if covid_cell > 0 and H[rowid][colid] == 0:
				infection_chance = random.randint(1,100)
				if 	(A[rowid][colid] == 4  and infection_chance <= 85) or (A[rowid][colid] == 3  and infection_chance <= 75) or (A[rowid][colid] == 2  and infection_chance <= 45) or (A[rowid][colid] == 1  and infection_chance <= 15):
					
					H[rowid][colid] = ASYMPTOMATIC_CODE
					D[rowid][colid] = 1
					day_positive = day_positive + 1
			
			if H[rowid][colid] == 1:
				sick_chance = random.randint(1,100)
				if sick_chance <= 90 and D[rowid][colid] >= 7:
					H[rowid][colid] = SICK_CODE
					Q[rowid][colid] = ISOLATION
			if H[rowid][colid] == 2:
				death_chance = random.randint(1,100)
				if death_chance < 4 and D[rowid][colid] >= 14:
					if A[rowid][colid] == 4 or (A[rowid][colid] == 3 and death_chance < 3):
						H[rowid][colid] = DEATH_CODE
						day_deceased = day_deceased + 1
				if death_chance >=4 and D[rowid][colid] >= 20:
					immune_chance = random.randint(1,100)
					if immune_chance > 70:
						H[rowid][colid] = IMMUNE_CODE
						Q[rowid][colid] = FREE
						day_recovered = day_recovered + 1
	return day_positive,day_recovered,day_deceased


if __name__ == "__main__":
	global day_positive, day_recovered, day_deceased
	random.seed(sys.argv[1])
	create_population(int(sys.argv[2]), 1)
	total_day_to_observe = int(sys.argv[3])
	for day in range(total_day_to_observe):
		day_positive, day_recovered, day_deceased = spread_covid19()
		gather_data(day_positive, day_recovered, day_deceased)

	visualize()


	

		
	
			




