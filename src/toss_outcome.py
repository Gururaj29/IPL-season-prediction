def batting_prob(climate_keywords):
	
	#returns the probability of the winner choosing batting
	climate_keywords=''.join(climate_keywords)
	climate_keywords=climate_keywords.lower()
	if "sun" in climate_keywords and "cloud" in climate_keywords:
		return 0.45
	elif "rain" in climate_keywords or "shower" in climate_keywords or "thunderstorm" in climate_keywords or "t-storm" in climate_keywords:
		return 0.2
	elif "sun" in climate_keywords:		
		return 0.8
	elif "overcast" in climate_keywords or "cloud" in climate_keywords:
		return 0.35
def toss_outcome(venue,date):
	with open(path+venue+"_climates.txt") as file:
		for line in file:
			l=line.split(" ")
			if l[1]==date:
				index_of_cm=l.index("CM")
				climate_keywords=l[index_of_cm+1:-1]
	climate_keywords[0]=climate_keywords[0][1:]
	prob_of_bat=batting_prob(climate_keywords)
	return prob_of_bat
path="climates/"
