from BeautifulSoup import BeautifulStoneSoup
import sys
import pprint

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

if __name__ == '__main__':

	soup = BeautifulStoneSoup(open(sys.argv[1]).read())
	users = parse_soup(soup)
	pprint.pprint(users)

