import requests
import re
from bs4 import BeautifulSoup

'''
pulls the data from array and saves it into dictionary
'''
def createInfo(stats, playoffData):
	name = str(stats[1].text)
	team = str(stats[2].text).lower()
	threes = str(stats[8].text)
	assists = float(stats[15].text)
	steals = float(stats[16].text)
	rebounds = float(stats[18].text)
	blocks = float(stats[21].text)
	points = float(stats[22].text)
	playoffData[name+" "+team] = {
		'threes': threes,
		'assists': assists,
		'steals': steals,
		'rebounds': rebounds,
		'blocks': blocks,
		'points': points
	}

'''
webscrapes url for stats on playoffs
'''
def pullPlayoffData(url, playoffData):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	rows = soup.find_all('tr')
	for row in rows:
		player = row.find_all('td', attrs={'class':'rank'})
		if player:
			stats = row.find_all('td')
			createInfo(stats, playoffData)

'''
gets both pages and gets best 200 players
'''
def createPlayoffStats():
	playoffData = {}
	pullPlayoffData('http://basketball.realgm.com/nba/playoffs/stats', playoffData)
	pullPlayoffData('http://basketball.realgm.com/nba/playoffs/team/NBA/0/stats/2017/Averages/All/points/All/desc/2/Playoffs', playoffData)
	return playoffData

global playoffStats
playoffStats = createPlayoffStats()