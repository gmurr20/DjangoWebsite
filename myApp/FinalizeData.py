#!/usr/bin/python

import csv
from threading import Thread

import DefensiveRankings
import playoffData
from BasketballPlayer import Player
import os

def DownloadPlayers(fileName):
	allPlayers = {}
	threads = []
	with open(fileName, 'r') as file:
		fileReader = csv.reader(file)
		skipFirst = True
		for row in fileReader:
			if skipFirst:
				skipFirst = False
				continue
			position = row[0]
			name = row[1]
			salary = int(row[2])
			gameInfo = row[3]
			team = row[5]
			newPlayer = Player(salary, name, team, position, gameInfo)
			t = Thread(target=newPlayer.getPlayerStats)
			threads.append(t)
			key = name+" "+team
			allPlayers[key] = newPlayer
	print "Estimating projections"
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	print "Estimations complete"
	return allPlayers

'''
Get the defensive rankings and download the players
'''
def finalizeData():
	DefensiveRankings.requestDefensiveRankings()
	playoffData.createPlayoffStats()
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	ultimatePath = os.path.join(BASE_DIR, 'myApp/DKSalaries.csv')
	return DownloadPlayers(ultimatePath)

