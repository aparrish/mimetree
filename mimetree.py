import random

mu = 10
sigma = 0.33
column_count = 4
extinguish_die = 12
multiplier = 2
running_total = 0
columns = list()

for i in range(column_count):
	columns.append(mu + abs(random.gauss(0, 8)))

while True:
	print '\t'.join([str(x) for x in columns])
	choice = int(raw_input("choose which column: "))
	this_round_vals = [x * multiplier if i == choice else x for i, x in enumerate(columns)]
	print 'calculated val after pick: ' + '\t'.join([str(x) for x in this_round_vals])
	round_score = int(sum(this_round_vals))
	print "sum: " + str(round_score)

	# choose index to extinguish
	choose_indices = [i for i, x in enumerate(columns) if x > 0]
	print "\tchoosing among indices to extinguish" + str(choose_indices)
	if random.randrange(extinguish_die) == 0:
		extinguish_index = random.choice(choose_indices)
		columns[extinguish_index] = 0

	columns = [x + random.gauss(0, sigma) if x != 0 else 0 for x in columns]

	running_total += round_score
	print "running total score: " + str(running_total)

