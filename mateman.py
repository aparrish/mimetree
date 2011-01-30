from BeautifulSoup import BeautifulStoneSoup
import sys
import pprint
from statlib import stats
import random
import portnameteau

statMinimum = 3

def parse_soup(soup):

	users = dict()
	attr_tags = set(['uid', 'first_name', 'last_name', 'name', 'religion', 'sex', 'political'])
	comma_split_tags = set(['activities', 'interests', 'music', 'tv', 'movies', 'books'])

	for user_tag in soup('user'):
		uid = user_tag('uid')[0].string
		this_user = dict()
		for tname in attr_tags:
			tag = user_tag.find(tname)
			if tag:
				this_user[tname] = tag.string
		for tname in comma_split_tags:
			tag = user_tag.find(tname)
			if tag:
				if tag.string:
					this_user[tname] = tag.string.split(', ')
		edhist = user_tag.find('education_history')
		if edhist:
			edhist_dict = dict()
			for edinfo_tag in edhist.findAll('education_info'):
				school_name_tag = edinfo_tag.find('name')
				if school_name_tag:
					school_name = school_name_tag.string
					edhist_dict[school_name] = list()
					concentration_tags = edinfo_tag.findAll('concentration')
					if len(concentration_tags) > 0:
						for ctag in concentration_tags:
							edhist_dict[school_name].append(ctag.string)
			this_user['education_history'] = edhist_dict
		workhist = user_tag.find('work_history')
		if workhist:
			workhist_list = list()
			for workinfo_tag in workhist.findAll('work_info'):
				company_name_tag = workinfo_tag.find('company_name')
				if company_name_tag:
					company_name = company_name_tag.string
					this_work = dict()
					this_work['name'] = company_name
					position_tag = workinfo_tag.find('position')
					if position_tag:
						this_work['position'] = position_tag.string
					city_tag = workinfo_tag.find('city')
					if city_tag:
						this_work['city'] = city_tag.string
					workhist_list.append(this_work)
			this_user['work_history'] = workhist_list
		users[uid] = this_user

	return users
	
def getStats(user, graphStats):
	
	userStats = {}
	#print user
	
	if ('interests' in user):
		userInterestCount = len(user['interests'])
	else: 
		userInterestCount = 0
	
	#print "intrigue: " + str(getStat(userInterestCount, 7, 7))
	userStats['intrigue'] = int(round(getStat(userInterestCount, graphStats['interests']['mean'], graphStats['interests']['stdev'])))
		
	if ('activities' in user):
		userActivityCount = len(user['activities'])
	else: 
		userActivityCount = 0
	
	#print "enthusiasm: " + str(getStat(userActivityCount, 4, 4))	
	userStats['enthusiasm'] = int(round(getStat(userActivityCount, graphStats['activities']['mean'], graphStats['activities']['stdev'])))

	if ('books' in user):
		userBookCount = len(user['books'])
	else: 
		userBookCount = 0	
	
	if ('movies' in user):
		userMovieCount = len(user['movies'])
	else: 
		userMovieCount = 0
	
	if ('music' in user):
		userMusicCount = len(user['music'])
	else: 
		userMusicCount = 0		

	if ('tv' in user):
		userTVCount = len(user['tv'])
	else: 
		userTVCount = 0
		
	mediaCounts = {'Books': userBookCount, 'Movies': userMovieCount, 'Music': userMusicCount, 'TV': userTVCount}
	#pprint.pprint(mediaCounts)
	#print "proficiency: " + getProficiency(mediaCounts)
	userStats['proficiency'] = getProficiency(mediaCounts)	

	userMediaCount = userTVCount + userMusicCount + userMovieCount + userBookCount
	
	#print "literacy: " + str(getStat(userMediaCount, 24, 36))
	userStats['literacy'] = int(round(getStat(userMediaCount, graphStats['media']['mean'], graphStats['media']['stdev'])))
	
	if ('work_history' in user):
		userWorkCount = len(user['work_history'])
	else: 
		userWorkCount = 0		

	if ('education_history' in user):
		userEduCount = len(user['education_history'])
	else: 
		userEduCount = 0
	
	userContribCount = userWorkCount + userEduCount
	
	#print "usefulness: " + str(getStat(userContribCount, 2, 2))
	userStats['usefulness'] = int(round(getStat(userContribCount, graphStats['useful']['mean'], graphStats['useful']['stdev'])))
	
	userTotalCount = userContribCount + userMediaCount + userActivityCount + userInterestCount
	
	#print "privacy: " + str(getPrivacy(userTotalCount, 26, 38))
	userStats['privacy'] = int(round(getPrivacy(userTotalCount, graphStats['totals']['mean'], graphStats['totals']['stdev'])))
	
	return userStats
	

def getStat(count, mean, stdev):
	#print count
	if (count == 0):				#auto 3
		return statMinimum
	elif (count < mean):			#max 9
		return statMinimum + (6 * count / mean)
	elif (count == mean):
		return 10
	elif (count < (mean + stdev)): #11-14
		return 10 + (count * 4 / (mean + stdev))#round(count/stdev)
	elif (count < (mean + stdev + stdev)): #15-18
		return 14 + (count * 4 / (mean + stdev + stdev))#round(count/stdev)
	else:
		return 18
		
def getPrivacy(count, mean, stdev):
	#print count
	if (count == 0):
		return 18
	elif (count < mean):
		return 18 - (9 * count / mean)
	elif (count == mean):
		return 10
	elif (count < mean + stdev):
		return 10 - (count * 3 / (mean + stdev))
	elif (count < (mean + stdev + stdev)):
		return 10 - (count * 3 / (mean + stdev + stdev))
	else:
		return statMinimum

def getProficiency(mediaCounts):
	maxNumber = 0
	maxType = ''
	
	if (mediaCounts['Books'] > maxNumber):
		maxNumber = mediaCounts['Books']
		maxType = 'Books'
	
	if (mediaCounts['TV'] > maxNumber):
		maxNumber = mediaCounts['TV']
		maxType = 'TV'
	
	if (mediaCounts['Music'] > maxNumber):
		maxNumber = mediaCounts['Music']
		maxType = 'Music'
		
	if (mediaCounts['Movies'] > maxNumber):
		maxNumber = mediaCounts['Movies']
		maxType = 'Movies'
	
	if (maxType == ''):
		maxType = 'Meditation'
	
	return maxType

def crunchNumbers(users):
	interestCounts = []
	activityCounts = []
	mediaCounts = []
	usefulCounts = []
	totalCounts = []
	
	graphStats = {}
	
	for user in users:

		userWorkCount = 0
		userEducationCount = 0
		
		if ('interests' in users[user]):
			userInterestCount = len(users[user]['interests'])
		else: 
			userInterestCount = 0
	
		if ('activities' in users[user]):
			userActivityCount = len(users[user]['activities'])
		else: 
			userActivityCount = 0
			
		if ('books' in users[user]):
			userBookCount = len(users[user]['books'])
		else: 
			userBookCount = 0	
		
		if ('movies' in users[user]):
			userMovieCount = len(users[user]['movies'])
		else: 
			userMovieCount = 0
		
		if ('music' in users[user]):
			userMusicCount = len(users[user]['music'])
		else: 
			userMusicCount = 0		

		if ('tv' in users[user]):
			userTVCount = len(users[user]['tv'])
		else: 
			userTVCount = 0


		if ('work_history' in users[user]):
			userWorkCount = len(users[user]['work_history'])
		else: 
			userWorkCount = 0		

		if ('education_history' in users[user]):
			userEduCount = len(users[user]['education_history'])
		else: 
			userEduCount = 0
		
		#print users[user]['last_name']
					
		interestCounts.append(userInterestCount)
		activityCounts.append(userActivityCount)
		usefulCounts.append(userWorkCount + userEduCount)
		mediaCounts.append(userMovieCount + userTVCount + userBookCount + userMusicCount)
	
		totalCounts.append(userInterestCount + userActivityCount + userWorkCount + userEduCount + userMovieCount + userTVCount + userBookCount + userMusicCount)
	

	#compute stats for interests
	nonzeroInterest = [item for item in interestCounts if item != 0]
	
	graphStats['interests'] = {}
	graphStats['interests']['mean'] = stats.mean(nonzeroInterest)
	graphStats['interests']['stdev'] = stats.stdev(nonzeroInterest)

	#stats for activities
	nonzeroActivities = [item for item in activityCounts if item != 0]

	graphStats['activities'] = {}
	graphStats['activities']['mean'] = stats.mean(nonzeroActivities)
	graphStats['activities']['stdev'] = stats.stdev(nonzeroActivities)

	#stats for media
	nonzeroMedia = [item for item in mediaCounts if item != 0]

	graphStats['media'] = {}
	graphStats['media']['mean'] = stats.mean(nonzeroMedia)
	graphStats['media']['stdev'] = stats.stdev(nonzeroMedia)
	
	#stats for work/education

	nonzeroUseful = [item for item in usefulCounts if item != 0]
	
	graphStats['useful'] = {}
	graphStats['useful']['mean'] = stats.mean(nonzeroUseful)
	graphStats['useful']['stdev'] = stats.stdev(nonzeroUseful)

	#stats for totals

	nonzeroTotals = [item for item in totalCounts if item != 0]

	graphStats['totals'] = {}
	graphStats['totals']['mean'] = stats.mean(nonzeroTotals)
	graphStats['totals']['stdev'] = stats.stdev(nonzeroTotals)

	return graphStats

def coinFlip (parent1, parent2, attribute):
	coin = random.randint(0,1)
	if (coin == 0):
		return parent1[attribute]
	else:
		return parent2[attribute]
		
def statMeld (parent1, parent2, attribute):
	babyStats = []
	
	if (attribute in parent1):
		for item in parent1[attribute]:
			if (random.randint(0,1)):
				babyStats.append(item)
	
	if (attribute in parent2):
		for item in parent2[attribute]:
			if (random.randint(0,1)):
				babyStats.append(item)
	
	return babyStats
	
def dictMeld (parent1, parent2, attribute):
	babyStats = {}
	
	if (attribute in parent1):
		for key in parent1[attribute].keys():
			if (random.randint(0,1)):
				babyStats[key] = parent1[attribute][key]

	if (attribute in parent2):
		for key in parent2[attribute].keys():
			if (random.randint(0,1)):
				if not (key in babyStats):
					babyStats[key] = parent2[attribute][key]
	
	return babyStats

def findSimilarity(baby, parent):
	
	options = [k for k in baby.keys() if k in ('activities', 'interests', 'music', 'books', 'tv', 'movies', 'work_history', 'education_history') and baby[k] and k in parent.keys() and parent[k]]

	random.shuffle(options)
	
	foundIt = -1
	
	if (len(options) == 0):
		return -1
	
	while (foundIt == -1):		
		category = options.pop()
		
		if (category == 'education_history'):
			candidates = [c for c in baby[category].keys() if c in parent[category].keys()]
			
		else:
			candidates = [c for c in baby[category] if c in parent[category]]
		
		if (len(candidates) > 0):
			result = [category, random.choice(candidates)]
		
			if (category == 'work_history'):
				result[1] = result[1]['name']
				
			return result
		else:
			if (len(options) == 0) or (len(candidates) == 0):
				return -1
	
	return
	
def findDifference(baby, parent):
	
	options = [k for k in parent.keys() if k in ('activities', 'interests', 'music', 'books', 'tv', 'movies', 'work_history') and parent[k]]

	random.shuffle(options)
	
	foundIt = -1
	
	if (len(options) == 0):
		return -1
	
	while (foundIt == -1):		
		category = options.pop()
		candidates = [c for c in parent[category] if baby[category] and c not in baby[category]]
		if (len(candidates) > 0):
			result = [category, random.choice(candidates)]
			if (category == 'work_history'):
				result[1] = result[1]['name']
			
			return result
		else:
			if (len(options) == 0) or (len(candidates) == 0):
				return -1
	
	return
			
	

def assessBaby(babyStats):
	
	descriptors = {'enthusiasm': [['apathetic', 'disinterested', 'indifferent', 'lethargic', 'lazy'],
			['outgoing', 'ardent', 'exuberant', 'spirited', 'ebullient']],
		'intrigue': [['boring', 'dull', 'uninteresting', 'wearisome', 'tedious'],
			['captivating', 'enchanting', 'fascinating', 'compelling', 'magnetic']],
		'literacy': [['ignorant', 'cretinous', 'moronic', 'imbecilic', 'oblivious'],
			['erudite', 'well-read', 'cultured', 'scholarly', 'sophisticated']],
		'usefulness': [['clumsy', 'incompetent', 'unskilled', 'ponderous', 'bungling'],
			['capable', 'skillful', 'well-qualified', 'proficient', 'accomplished']],
		'privacy': [['forthright', 'honest', 'open', 'aboveboard', 'trusting'],
			['secretive', 'furtive', 'reticent', 'cryptic', 'withdrawn']]}
	
	middlers = ['middlingly', 'just-shy-of-', 'nearly ', 'almost-', 'in-the-ballpark-of-', 'practically ', 'virtually ', 'within-shouting-distance-of-', 'approaching ', 'not-quite-']
	
	stat = random.choice(descriptors.keys())
		
	if not (stat == 'proficiency'):
		if (babyStats[stat] < 9):
			if (stat == 'privacy'):
				check = [2]
			else:
				check = [0]
			check.append(random.choice(descriptors[stat][0]))
			return check
		elif (babyStats[stat] < 11):
			check = [1]
			check.append(random.choice(middlers) + random.choice(descriptors[stat][0]))
			return check
		elif (babyStats[stat] < 14):
			check = [1]
			check.append(random.choice(middlers) + random.choice(descriptors[stat][1]))
			return check
		else:
			if (stat == 'privacy'):
				check = [0]
			else:
				check = [2]
			check.append(random.choice(descriptors[stat][1]))
			return check	
	else:
		return -1
	
	
	
	
					

def makeBaby(parent1, parent2):
	
	baby = dict()
	
	baby['first_name'] = portnameteau.portnameteau([parent1['first_name'], parent2['first_name']])
	
	surnameType = random.randint(0,2)
	if (surnameType == 0):
		baby['last_name'] = coinFlip(parent1, parent2, 'last_name')
	elif (surnameType == 1):
		baby['last_name'] = parent1['last_name'] + "-" + parent2['last_name']
	else:
		baby['last_name'] = portnameteau.portnameteau([parent1['last_name'], parent2['last_name']])
	
	if (random.randint(0,1) == 0):
		baby['sex'] = 'female'
	else:
		baby['sex'] = 'male'

	baby['activities'] = statMeld(parent1, parent2, 'activities')
	baby['interests'] = statMeld(parent1, parent2, 'interests')
	baby['music'] = statMeld(parent1, parent2, 'music')
	baby['tv'] = statMeld(parent1, parent2, 'tv')
	baby['books'] = statMeld(parent1, parent2, 'books')
	baby['movies'] = statMeld(parent1, parent2, 'movies')	

	baby['work_history'] = statMeld(parent1, parent2, 'work_history')
	baby['education_history'] = dictMeld(parent1, parent2, 'education_history')

	
	return baby

def getName(baby):
	return baby['first_name'] + " " + baby['last_name']


def getBio(baby, parent1, parent2):
	
	madLib = {'impression': '',
			'parentAdj': ''}
	
	#intro sentence templates
	introTemplates = ["%(baby)s would be the %(impression)s child of %(p1)s and %(p2)s. ", 
					"The %(parentAdj)s union of %(p1)s and %(p2)s would result in the birth of %(baby)s."]
	
	
	
	bio = ""
	
	getName(parent1)
	
	bio = bio + getName(baby) + " is the child of proud parents " + getName(parent1) + " and " + getName(parent2) + ". "	
	
	if (random.randint(0,1)):
		check = findSimilarity(baby, parent1)
		if (check == -1):
			bio += baby['first_name'] + " and " + parent1['first_name'] + " have nothing in common. "
		else:
			bio += "When it comes to " + check[0] + ", " + baby['first_name'] + " and " + parent1['first_name'] + " share a love of " + check[1] + ". "
	else:
		check = findDifference(baby, parent1)
		if (check == -1):
			bio += baby['first_name'] + " wishes " + parent1['first_name'] + " had at least one characteristic to rebel against. "
		else:
			bio += baby['first_name'] + " rejects " + parent1['first_name'] + "'s lame affection for " + check[1] + ". "

	if (random.randint(0,1)):
		check = findSimilarity(baby, parent2)
		if (check == -1):
			bio += baby['first_name'] + " and " + parent2['first_name'] + " have nothing in common. "
		else:
			bio += "When it comes to " + check[0] + ", " + baby['first_name'] + " and " + parent2['first_name'] + " share a love of " + check[1] + ". "
	else:
		check = findDifference(baby, parent2)
		if (check == -1):
			bio += baby['first_name'] + " wishes " + parent2['first_name'] + " had at least one characteristic to rebel against. "
		else:
			bio += baby['first_name'] + " rejects " + parent2['first_name'] + "'s lame affection for " + check[1] + ". "
	
	bio += "Baby is " + assessBaby(baby['stats'])[1] + " and " + assessBaby(baby['stats'])[1] + ". "
	
	if (random.randint(0,1000000) == 999999):
		bio += "It's a miracle! Baby is genetically immune to the space fungus!"
	else:
		bio += "It should come as no surprise that " + baby['first_name'] + " is not genetically immune to the space fungus."
	
	return bio
	
	
	
	

if __name__ == '__main__':

	trials = 20
	
	soup = BeautifulStoneSoup(open(sys.argv[1]).read())
	users = parse_soup(soup)
	
	genepool = users.keys()
	graphStats = crunchNumbers(users)
		
	
	for x in range(trials):
		parent2 = -1
	
		parent1 = random.randint(0, len(users) - 1)
	
		while (parent2 == -1):
			parent2 = random.randint(0, len(users) - 1)
			if (parent2 == parent1):
				parent2 = -1

	
	
		baby = makeBaby(users[genepool[parent1]], users[genepool[parent2]])
	

	
		baby['stats'] = getStats(baby, graphStats)
		users[genepool[parent1]]['stats'] = getStats(users[genepool[parent1]], graphStats)
		users[genepool[parent2]]['stats'] = getStats(users[genepool[parent2]], graphStats)	
	
		print getBio(baby, users[genepool[parent1]], users[genepool[parent2]])
		print	
	
	
	
	
