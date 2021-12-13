
FILENAME = 'results.csv'
DEFAULT_GAME_SCORE = 21
N = 3

adjustments = {}
with open('adjust.csv') as f:
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		cells = line.split(',')
		if len(cells) != 2:
			raise Exception('Parse failure in adjust.csv: ' + line)
		adjustments[cells[0]] = int(cells[1])

with open(FILENAME) as f:
	lines = f.readlines()

match_count = len(lines)
print(match_count, 'matches')

grid = {}
def process_player(player, opponent1, opponent2, score):
	if player not in grid:
		grid[player] = {}
	if opponent1 not in grid[player]:
		grid[player][opponent1] = []
	if opponent2 not in grid[player]:
		grid[player][opponent2] = []
	grid[player][opponent1].append(score)
	grid[player][opponent2].append(score)

for line in lines:
	line = line.strip()
	cells = line.split(',')

	if len(cells) != 6:
		raise Exception("Unexpected number of cells in line: " + line)

	p1,p2,s1,s2,p3,p4 = cells
	# print(line, cells)
	# print(p1,p2,s1,s2,p3,p4)

	process_player(p1, p3, p4, s2)
	process_player(p2, p3, p4, s2)
	process_player(p3, p1, p2, s1)
	process_player(p4, p1, p2, s1)

players = sorted(grid.keys())

output = []

# Header Row
header = 'Name,Games,Opponents,' + ','.join([p for p in players]) + ',Calc,Points'
print(header)
output.append(header)

for p1 in players:
	# print(p1)
	score_count = 0
	opponent_count = 0

	points = []
	opponent_cells = []
	for p2 in players:
		if p2 in grid[p1]:
			game_scores_against_opponent = grid[p1][p2]
			opponent_cells.append('|'.join(game_scores_against_opponent))
			opponent_count += 1
			score_count += len(game_scores_against_opponent)
			best_opponent_score = max(game_scores_against_opponent)
			points.append(best_opponent_score)
			# print(p2, game_scores_against_opponent, best_opponent_score)
		else:
			opponent_cells.append('')

	points = sorted(points)
	# print('points before defaults', points)
	while len(points) - N < 0:
		print('!!! ' + p1 + ' has not played against enough different opponents -> adding a default game score!')
		points.insert(0, DEFAULT_GAME_SCORE)
	# print('points after defaults', points)

	game_count = score_count / 2
	best_points = points[:N]
	if p1 in adjustments:
		best_points.append(adjustments[p1])
	# print(best_points)

	cells = [p1, game_count, opponent_count]
	cells += opponent_cells
	cells += [
		'+'.join([str(p) for p in best_points]),
		sum([int(p) for p in best_points])
	]

	line = ','.join(str(line) for line in cells)
	print(line)
	output.append(line)

with open('out.csv', 'w') as f:
	f.writelines([str(line) + "\n" for line in output])
