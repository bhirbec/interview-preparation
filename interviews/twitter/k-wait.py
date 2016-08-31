# https://careercup.com/question?id=5723093194506240

# Given an array of task and k wait time for which a repeated task needs to wait k time to execute
# again. return overall unit time it will take to complete all the task.

# Example:
# A B C D and k = 3
# output: 4 (execute order A B C D)

# A B A D and k = 3
# output: 6 (execute order A B . . A D)

# A A A A and k =3
# output: 13 (A . . . A . . . A . . . A)

# A B C A C B D A and k = 4
# output: 10 (A B C . A . C B D A )

def main():
	tasks = ['A', 'B', 'C', 'D']
	print find_exec_time(tasks)

	tasks = ['A', 'B', 'A', 'D']
	print find_exec_time(tasks)

	tasks = ['A', 'A', 'A', 'A']
	print find_exec_time(tasks)

	tasks = ['A', 'B', 'C', 'A', 'C', 'B', 'D', 'A']
	print find_exec_time(tasks)


def find_exec_time(tasks, k=3):
	output = []
	times = {}
	c, t, n = 0, 0, len(tasks)

	while c < n:
		task = tasks[c]
		last_exec = times.get(task, -(k + 1))
		delta = t - last_exec
		if delta > k:
			output.append(task)
			times[task] = t
			c += 1
		else:
			output.append('.')
		t += 1

	return output, t

main()
