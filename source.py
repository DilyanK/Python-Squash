import csv
import math
import random
import itertools 
import matplotlib.pyplot as plt

# All of the functions are in the same order as in the Coursework brief

def game(ra, rb):
	# random.seed(57) # only needed for answer of 1a
	p = ra / (ra + rb) # probability of player A winning
	score_a = 0
	score_b = 0
	game_over = False

	while game_over == False:			
		r = random.uniform(0, 1) # assigns a random floating point number between 0 an 1 to r
		if r < p: 
			score_a += 1
		else: 
			score_b += 1
		eleven = (score_a >= 11) or (score_b >= 11) # checks if either of the players has reached 11 points
		difference2 = abs(score_a-score_b) > 1 # checks if the difference in the points is 2
		if eleven and difference2: # if both are true ends the game
			game_over = True

	return score_a, score_b

def winProbability(ra, rb, n):
	wins_a = 0
	wins_b = 0
	rallies = 0

	for match in range(0, n):
		score_a, score_b = game(ra, rb)
		rallies += (score_a + score_b)
		if score_a > score_b: 
			wins_a += 1
		else: 
			wins_b += 1 		
	pa = wins_a / (wins_a + wins_b) 
	pa = round(pa, 2)
	rallies = rallies / n

	return pa, rallies # returns the number of rallies too, needed further in the code

def player_abilities(file):
	with open(file) as csvfile:
		rdr = csv.reader(csvfile)
		lot = []
		next(rdr)
		for row in rdr:
			lot.append((int(row[0]), int(row[1])))

	return lot

def firstD(playerlist):
	pa = [] # probability of player A beating player B
	ra_rb = [] # ra/rb

	for player in playerlist:
		pa.append(winProbability(player[0], player[1], 1000)[0])
		ra_rb.append(player[0] / player[1])

	ra_rb, pa = zip(*sorted(zip(ra_rb, pa))) # sorts out false display of values
	plt.plot(ra_rb, pa)
	plt.axis([0, 3.5, 0, 1])
	plt.ylabel('Probability of A winning')
	plt.xlabel('Ability of A / Ability of B')
	plt.title('The probability of Player A beating Player B (1000 games)')
	plt.show()

def firstE(ra, rb, min_probability):
	n = 0
	min_probability = 0
	while min_probability <= 0.9:
		n += 1
		fl = (math.factorial(2*n-1)) / ((math.factorial(n)) * math.factorial(n-1))
		fm = (fl * ((0.6) ** n)) *(0.4) ** (n-1) # binomial distribution formula

		min_probability += fm

	return n

def engl_game(ra, rb):
	p = ra / (ra + rb)
	score_a = 0
	score_b = 0
	rallies = 0
	points_to = 9
	server = None
	game_over = False

	while game_over == False:			
		r = random.uniform(0, 1)
		if r < p:
			if  server == 'a': 
				score_a += 1
			else: 
				server = 'a'
		else:
			if server == 'b': 
				score_b += 1
			else: 
				server = 'b'				
		if score_a == 8 and score_b == 8: # checks if the result is 8-8
			if r < 0.5:	
				points_to = 10 # if yes, it decides to play either to 9 or 10   
		rallies += 1        
		new_points_to = (score_a == points_to) or (score_b == points_to)
		if new_points_to: 
			game_over = True

	return score_a, score_b, rallies

def engl_winProbability(ra, rb, n):
	rallies = 0

	for match in range(0, n):
		rallies2 = engl_game(ra, rb)[2]
		rallies += rallies2	
	rallies = rallies / n

	return rallies

def second():
	playerlist2 = player_abilities('players.csv') # at 0.1 intervals, abilities go from 0.1 to 9.9

	rarb = []
	pars_rallies = []
	engl_rallies = []

	for player in playerlist2:
		rarb.append(player[0] / player[1])
		pars_rallies.append(winProbability(player[0], player[1], 1000)[1])
		engl_rallies.append(engl_winProbability(player[0], player[1], 1000))

	pars_plot, = plt.plot(rarb, pars_rallies)
	engl_plot, = plt.plot(rarb, engl_rallies)

	plt.axis([0, 10, 10, 30])
	plt.ylabel('Average time for each match (minutes)')
	plt.xlabel('Relative abilities for players A and B')
	plt.title('Relative abilities against time for matches for the English and PARS scoring systems (1000 games)')
	plt.legend([pars_plot, engl_plot], ['PARS SCORING SYSTEM', 'ENGLISH SCORING SYSTEM'])
	plt.show()