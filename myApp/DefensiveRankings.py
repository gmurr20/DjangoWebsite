#!/usr/bin/python
import requests
import re
from bs4 import BeautifulSoup

global teamMap
teamMap = {"Memphis": "Mem", "Golden State": "GS", "Utah": "Uta", "San Antonio": "SA", 
			"Atlanta": "Atl", "Charlotte": "Cha", "Detroit": "Det", "Oklahoma City": "OKC", 
			"Milwaukee": "Mil", "LA Clippers": "LAC", "New Orleans": "NO ", "Miami": "Mia", 
			"Chicago": "Chi", "Indiana": "Ind", "Toronto": "TOR", "Cleveland": "Cle", 
			"Houston": "Hou", "Boston": "Bos", "Orlando": "Orl", "Washington":"Was", 
			"Philadelphia": "Phi", "Dallas": "Dal", "Phoenix":"Pho", "Sacramento": "Sac", 
			"New York": "NY ", "Minnesota": "Min", "Denver":"Den", "Brooklyn":"Bkn", 
			"Portland":"Por", "LA Lakers":"LAL"}
global defenseRankings
defensiveRankings = {}
def requestDefensiveRankings():
	print "getting defensive rankings"
	url = "http://www.espn.com/nba/hollinger/teamstats/_/sort/defensiveEff/order/false"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	tds = soup.find_all('td', align='left')
	teams = []
	count = 0
	for td in tds:
		teamName = td.find('a')
		if teamName:
			pointChange = ((count-14.5)/14.5) * 5
			abreviationName = teamMap[teamName.text]
			abreviationName = str(abreviationName).lower()
			defensiveRankings[abreviationName] = pointChange
			count+=1
	print "defensive rankings complete"