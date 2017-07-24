#!/usr/bin/python
#idea from: http://sambrady3.github.io/knapsack.html

import random
import time
from BasketballPlayer import Player
from FinalizeData import finalizeData
from operator import add

# global allEligiblePlayers
global pg, sg, sf, pf, c, g, f, util

'''
Initialize all the players
'''
def initialize():
	allPlayers = finalizeData()
	global pg, sg, sf, pf, c, g, f, util
	pg = [allPlayers[player] for player in allPlayers if "PG" in allPlayers[player].position]
	sg = [allPlayers[player] for player in allPlayers if "SG" in allPlayers[player].position]
	sf = [allPlayers[player] for player in allPlayers if "SF" in allPlayers[player].position]
	pf = [allPlayers[player] for player in allPlayers if "PF" in allPlayers[player].position]
	c = [allPlayers[player] for player in allPlayers if "C" in allPlayers[player].position]
	g = [allPlayers[player] for player in allPlayers if "SG" in allPlayers[player].position or "PG" in allPlayers[player].position]
	f = [allPlayers[player] for player in allPlayers if "SF" in allPlayers[player].position or "PF" in allPlayers[player].position]
	util = [allPlayers[player] for player in allPlayers]

'''
Generate a random team with bball specifications
'''
def generateRandomTeam():
	team = {'pg' : random.sample(pg,1),
	'sg' : random.sample(sg,1),
	'sf' : random.sample(sf,1),
	'pf' : random.sample(pf,1),
	'c' : random.sample(c,1),
	'g' : random.sample(g,1),
	'f' : random.sample(f,1),
	'util' : random.sample(util,1)
	}
	while (team['pg'][0] in team['sg'] or team['pg'][0] in team['sf']):
		team['pg'] = random.sample(pg,1)
	while (team['sg'][0] in team['sf'] or team['sg'][0] in team['pf'] or team['sg'][0] in team['c']):
		team['sg'] = random.sample(sg,1)
	while (team['sf'][0] in team['pf'] or team['sf'][0] in team['c']):
		team['sf'] = random.sample(sf,1)
	while (team['pf'][0] in team['c']):
		team['pf'] = random.sample(pf,1)

	while (team['g'][0] in team['pg'] or team['g'][0] in team['sg'] or team['g'][0] in team['sf'] or team['g'][0] in team['pf'] or team['g'][0] in team['c']):
		team['g'] = random.sample(g,1)
	while (team['f'][0] in team['pg'] or team['f'][0] in team['sg'] or team['f'][0] in team['sf'] or team['f'][0] in team['pf'] or team['f'][0] in team['c'] or team['f'][0] in team['g']):
		team['f'] = random.sample(f,1)
	while (team['util'][0] in team['f'] or team['util'][0] in team['g'] or team['util'][0] in team['c'] or team['util'][0] in team['pf'] or team['util'][0] in team['sf'] or team['util'][0] in team['sg'] or team['util'][0] in team['pg']):
		team['util'] = random.sample(util,1)
	return team

'''
Create a bunch of teams in a list
'''
def createPopulation(count):
	population = []
	for i in range(count):
		population.append(generateRandomTeam())
	return population

'''
Get the projected points for a team
'''
def teamStrength(team):
    points = 0
    salary = 0
    for key in team:
        for player in team[key]:
            points += player.projected
            salary += player.salary
    if salary > 50000:
    	return 0
    return points

'''
Sum up the team salary
'''
def getTeamSalary(team):
    salary = 0
    for key in team:
        for player in team[key]:
            salary += player.salary
    return salary

'''
Print out the team
'''
def printTeam(team):
    print "PG: ", team['pg'][0]
    print "SG: ", team['sg'][0]
    print "SF: ", team['sf'][0]
    print "PF: ", team['pf'][0]
    print "C:  ", team['c'][0]
    print "G:  ", team['g'][0]
    print "F:  ", team['f'][0]
    print "Ut: ", team['util'][0]

'''
Mix and match two teams
'''
def breed(mom, dad):
	children = []
	for i in range(2):
		child = {}
		pgList = set(mom['pg'] + dad['pg'])
		child['pg'] = random.sample(pgList, 1)
		
		sgList = set(mom['sg'] + dad['sg'])
		child['sg'] = random.sample(sgList, 1)
		while child['sg'][0] in child['pg']:
			sgList = set(sgList)-set(child['sg'])
			child['sg'] = random.sample(sgList, 1)

		sfList = set(mom['sf'] + dad['sf'])
		child['sf'] = random.sample(sfList, 1)
		while child['sf'][0] in child['pg'] or child['sf'][0] in child['sg']:
			sfList = set(sfList)-set(child['sf'])
			child['sf'] = random.sample(sfList, 1)

		pfList = set(mom['pf'] + dad['pf'])
		child['pf'] = random.sample(pfList, 1)
		while child['pf'][0] in child['pg'] or child['pf'][0] in child['sg'] or child['pf'][0] in child['sf']:
			pfList = set(pfList)-set(child['pf'])
			child['pf'] = random.sample(pfList, 1)
		
		cList = set(mom['c'] + dad['c'])
		child['c'] = random.sample(cList, 1)
		while child['c'][0] in child['sf'] or child['c'][0] in child['sg'] or child['c'][0] in child['pf']:
			cList = set(cList)-set(child['c'])
			child['c'] = random.sample(cList, 1)

		gList = set(mom['g']+dad['g'])|set(pgList|sgList)
		child['g'] = random.sample(gList, 1)
		while child['g'][0] in child['pg'] or child['g'][0] in child['sg'] or child['g'][0] in child['sf'] or child['g'][0] in child['pf']:
			gList = gList-set(child['g'])
			child['g'] = random.sample(gList,1)

		fList = set(mom['f']+dad['f'])|set(pfList|sfList)
		child['f'] = random.sample(fList, 1)
		flag = True
		while child['f'][0] in child['pg'] or child['f'][0] in child['sg'] or child['f'][0] in child['sf'] or child['f'][0] in child['pf'] or child['f'][0] in child['c'] or child['f'][0] in child['g']:
			fList = fList-set(child['f'])
			try:
				child['f'] = random.sample(fList,1)
			except:
				print "Forward Issue"
				if flag:
					child['f'] = random.sample(cList,1)
					flag = False
				else:
					child['f'] = random.sample(f,1)

		utilList = set(mom['util'] + dad['util'])|set(fList|gList|cList)
		child['util'] = random.sample(utilList, 1)
		while (child['util'][0] in child['f'] or child['util'][0] in child['g'] or child['util'][0] in child['c'] or child['util'][0] in child['pf'] or child['util'][0] in child['sf'] or child['util'][0] in child['sg'] or child['util'][0] in child['pg']):
			utilList = utilList-set(child['util'])
			child['util'] = random.sample(util,1)
		children.append(child)
	return children

'''
Change one position on a team
'''
def mutate(team):
	positions = ['pg', 'sg', 'sf', 'pf', 'c', 'f', 'g', 'util']
	posMap = {'pg': pg, 'sg': sg, 'sf': sf, 'pf': pf, 'c':c, 'f':f, 'g':g, 'util':util}
	pos = random.sample(positions,1)[0]
	team[pos] = random.sample(posMap[pos],1)
	flag = True
	while flag:
		flag = False
		for p in positions:
			if p != pos and team[pos][0] in team[p]:
				flag = True
				break
		if flag:
			team[pos] = random.sample(posMap[pos],1)
	return team

'''
Evolve the population to get the best team
'''
def evolution(population, keep=.3, selectProbability=.1, mutateProbability=.05):
	bestTeams = [ (teamStrength(team), team) for team in population]
	bestTeams = [ x[1] for x in sorted(bestTeams, reverse=True) ]
	numKeep = int(keep*len(population))
	parents = bestTeams[0:numKeep]

	for team in bestTeams[numKeep:]:
		if selectProbability > random.random():
			parents.append(team)

	for team in parents:
		if mutateProbability > random.random():
			team = mutate(team)

	parentsLength = len(parents)
	desiredLength = len(population) - parentsLength
	children = []
	while len(children) < desiredLength:
	    dad = random.randint(0, parentsLength-1)
	    mom = random.randint(0, parentsLength-1)
	    if dad != mom:
	        dad = parents[dad]
	        mom = parents[mom]
	        kids = breed(mom,dad)
	        for kid in kids:
	            children.append(kid)
	newPopulation = parents + children
	return newPopulation

'''
Get the grade of the population
'''
def grade(pop):
    summed = reduce(add, (teamStrength(team) for team in pop))
    return summed / (len(pop) * 1.0)

'''
Run the genetic knapsack
'''
def runScript():
	initialize()
	best_teams=[]
	history = []
	p = createPopulation(2000)
	fitness_history = [grade(p)]
	for i in range(40):
		print str(i)
		p = evolution(p)
		fitness_history.append(grade(p))
		valid_teams = [ team for team in p if getTeamSalary(team) <= 50000]
		valid_teams = sorted(valid_teams, key=teamStrength, reverse=True)
		if len(valid_teams) > 0:
			best_teams.append(valid_teams[0])
	for datum in fitness_history:
		history.append(datum)
	best_teams = sorted(best_teams, key=teamStrength, reverse=True)
	return best_teams[0]