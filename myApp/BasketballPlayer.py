from threading import Thread, Lock
import requests
import re
from bs4 import BeautifulSoup
import math
import DefensiveRankings
import playoffData

global mutex
mutex = Lock()

class Player:
	salary = 0
	name = ""
	team = ""
	position = ""
	gameInfo = ""
	projected = float(0.0)

	threePointers = 0.0
	rebounds = 0.0
	assists = 0.0
	steals = 0.0
	blocks = 0.0
	points = 0.0

	def __init__(self, salary, name, team, position, gameInfo):
		self.salary = salary
		self.name = name
		self.team = team
		self.position = position
		self.gameInfo = gameInfo

	'''
	Weigh playoffs more heavily
	'''
	def weightPlayoffsHeavily(self):
		searchKey = self.name.lstrip()+" "+str(self.team).lower()
		if str(self.team).lower() == 'sa':
			searchKey = self.name.lstrip()+" "+"sas"
		if searchKey in playoffData.playoffStats:
			myPlayer = playoffData.playoffStats[searchKey]
			self.threePointers = self.threePointers * .25 + float(myPlayer['threes']) *.75
			self.rebounds = self.rebounds * .25 + float(myPlayer['rebounds']) * .75
			self.assists = self.assists * .25 + float(myPlayer['assists']) * .75
			self.steals = self.steals * .25 + float(myPlayer['steals']) * .75
			self.blocks = self.blocks * .25 + float(myPlayer['blocks']) * .75
			self.points = self.points * .25 + float(myPlayer['points']) * .75

	'''
	Request a search on the player for last stats in 7 games and parse through that
	-thread safe
	'''
	def getPlayerStats(self):
		url = "http://games.espn.com/fba/freeagency?leagueId=434300&teamId=1&avail=-1&slotCategoryGroup=-1&version=last7&search="
		specific_url = url+self.name
		try:
			r = requests.get(specific_url)
			soup = BeautifulSoup(r.content, "html.parser")
			playerRow = soup.find_all('tr', attrs={'class':'pncPlayerRow', 'class':'playerTableBgRow0'})
			stats = playerRow[0].find_all('td', attrs={'class':'playertableStat'})
			otherStats = playerRow[0].find_all('td', attrs={'class': 'playertableData'})
		except:
			try:
				last_name = self.name.split(" ")
				last_name = last_name[len(last_name)-1]
				url += last_name
				r = requests.get(url)
				soup = BeautifulSoup(r.content, "html.parser")
				playerRow = soup.find_all('tr', attrs={'class':'pncPlayerRow', 'class':'playerTableBgRow0'})
			except:
				mutex.acquire()
				print "Could not get data for "+self.name
				mutex.release()
				self.projected = 0
				return
		try:
			playerRating = float(otherStats[0].text)
		except:
			playerRating = 0
		try:
			percentageOwned = float(otherStats[1].text)
			if percentageOwned < .8:
				stats = []
		except:
			percentageOwned = 0
		try:
			self.threePointers = float(stats[4].text)
		except:
			self.threePointers = 0
		try:
			self.rebounds = float(stats[5].text)
		except:
			self.rebounds = 0
		try:
			self.assists = float(stats[6].text)
		except:
			self.assists = 0
		try:
			self.steals = float(stats[7].text)
		except:
			self.steals = 0
		try:
			self.blocks = float(stats[8].text)
		except:
			self.blocks = 0
		try:
			self.points = float(stats[9].text)
		except:
			self.points = 0
		#playoff weights
		self.weightPlayoffsHeavily()
		#project the points
		self.getProjected()
		#add player rating
		self.projected += playerRating
		if self.salary < 3500:
			self.projected -= 5
		else:
			self.projected -= 2

	'''
	Gets the projected points based on the rules for daily fantasy
	'''
	def getProjected(self):
		score = 0.0
		score += self.points
		score += self.threePointers * .5
		score += self.rebounds * 1.25
		score += self.assists *1.5
		score += self.steals * 2
		score += self.blocks * 2
		doubleCount = 0
		if self.points >= 10:
			doubleCount +=1
		if self.rebounds >= 10:
			doubleCount +=1
		if self.assists >= 10:
			doubleCount +=1
		if self.steals >= 10:
			doubleCount += 1
		if self.blocks >=10:
			doubleCount +=1
		score += doubleCount * 1.25
		#add or subtract based on home or away
		game = self.gameInfo.split("@")
		opponent = ""
		if self.team not in game[0]:
			score += 1
			opponent = game[1][:3]
		else:
			score -= 1
			opponent = game[0][:3]
		opponent = str(opponent).lower().rstrip()
		score += DefensiveRankings.defensiveRankings[opponent]
		self.projected = score
		mutex.acquire()
		#print self.name, opponent, DefensiveRankings.defensiveRankings[opponent]
		mutex.release()

	def __str__(self):
		return "{} {} {} {} {}".format(self.name, self.team, self.position, self.salary, self.projected)
