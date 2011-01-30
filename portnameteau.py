import re
import random

def vtoc_idx(s):
	match_obj = re.search(r'[aeiou][^aeiou]', s.lower())
	if match_obj:
		return match_obj.start() + 1
	else:
		return 0

def portnameteau(name_list):
	random.shuffle(name_list)
	s1 = name_list[0]
	s2 = name_list[1]
	end_s1 = vtoc_idx(s1)
	start_s2 = vtoc_idx(s2)
	return s1[:end_s1] + s2[start_s2:]

if __name__ == '__main__':
	first_names = ['Nick','Lisa','Nathan','Peter','Jason','Yasmin','Lesley','Florica','Eric','Tom','Mike','Hondo','Jeff','Scott','Elim','Caleb','Brooke','Mooshir','Sinan','Matthew','Rob','Michael','Corey','Kara','Catherine','Caleb','Anderson','Alejandro','Shelly','Tymm','Steven','Jelani','Sonaar','Jason','Kevin','Hyeki','Yan','Andrea','Steven','Charlotte','Andrew','Fiction','Diego','Kalle','John','Amy','Kacie','Nathan','Adam','Marina','Eldin','Mitch','Steven','Michael','Jeff','Corrine','Viceroy','Neilson','Rory','Ozge','Rucyl','Patricia','Jason','Ruth','Michael','Adam','J.R.', 'Amelia','ChoRong','Kate','Aaron','Doug','Robert','Michael','Calista','Brendan','Emily','Rachelle','Kristin','Celina','Claire','Jaymes','Benjamin','Joshua','Scott','Ohad','Preston','Jason','Samuel','Scott','Tim','Sanjay','Suzan','Derek','Benedetta','Mike','Heather','Jaewook','Lisa','Lauren','Philippe','Vikram','Evan','Casey','Emery','Daniel','Patty','Fitzgorilla','Edward','John','Adam','Steven','Mushon','Emma','Lee-Sean','Peter','Alex','Bree','Eugene','Nathan','Kevin','Leah','Gian','Yonatan','Jorge','Max','Tom','Joora','Josh','Ameya','Nicholas','Greg','Jody','Charles','John','Brian','Zeeshan','Piama','Michael','Brian','Ithai','Denisse','Carolina','Xiaoyang','Shawn','Derek','Ben','Luke','Preston','Eric','Ilan','Timothy','Brenton','Tonio','Marco','Kati','Tristan','Ben','Robert','Shinyoung','George','Yasser','Oscar','Joseph','Zannah','Lois','Susan','Sabrina','Chris']
	last_names = ['Luthra','Tea','Carter','Min','Cao','Dulko','Litt','Parrish','Doro','Circus','Rioja','Vilbaste','Schimmel','Khoshbin','Kinzer','Olsen','Nash','Zurkow','Chester','Said','Lehrburger','Clemow','Gray','Brown','Grampapants','Abeel','Sandberg','Kirimlioglu','Mills','Oakim','Scott','Sergel','Fisher','Blackham','Birch','Johnston','Monahan','Brown','Parrish','Carlsen','Yount','Burbank','Berg','Smith','Neshkes','O\'Friel','Alvarado','Parrish','Dec','Farrar','Noble','Hammack','Folman','Parrish','Krugman','Hurst','Hoffer','Szetela','Papinazath','Eraslan','Omori','Piantella','Dory','Bridges-Parrish','Shin','Lurie','Parrish','Pierre','Tank','Furchtgott','Kolderup','Martin','Shiffman','Friend','Fitzwilliam','Gordon','Simon','Jackson','Zer-Aviv','Piper-Burket','Huang','Horvath','Kauffmann','Lang','Ahn','Banks','Vance','Wechsler','Villamil','Kelib','Just','Vernacular','Igoe','Song','Berry','Mhatre','Gordon','Stringer','Caldwell','Pratt','Dimatos','Parke','Lakhani','Habibullah','Chladil','Heslop','Benjamin','Mancia','Vallejo','Feng','Every','Duarte','Leduc-Mills','DuBois','Noon','Beug','Schifter','Stutts','Stone','Jung']

	for i in range(20):
		first_name1 = random.choice(first_names)
		last_name1 = random.choice(last_names)
		first_name2 = random.choice(first_names)
		last_name2 = random.choice(last_names)
		print "%s %s + %s %s = %s %s" % (first_name1, last_name1, first_name2, last_name2, portnameteau([first_name1, first_name2]), portnameteau([last_name1, last_name2]))

