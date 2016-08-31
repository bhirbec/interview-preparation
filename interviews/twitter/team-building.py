# https://careercup.com/question?id=5673924747591680

# Some comments suggest that the answer is n/2 + 1. The code below seems to
# to confirm that.

def main():
	n = 10
	print find_k(n)

def find_k(n):
	selected_team = []
	for k in xrange(1, n+1):
		ok = False
		for team, score in iter_team_score(n, k):
			if score == 0:
				ok = True
				selected_team = team
				break

		if not ok:
			return k, selected_team

	return None

def iter_team_score(n, k):
	team = [0] * k

	def f(count, score, prev_i):
		if count == k or score > 0:
			yield '-'.join(str(p) for p in team), score
			return

		for i in xrange(prev_i, n - (k - count) + 1):
			team[count] = i
			player_score = sum(1 for j in xrange(count) if i % team[j] == 0)
			for s in f(count+1, score+player_score, i+1):
				yield s

	return f(0, 0, 1)

main()
