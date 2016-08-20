// Fibonacci - each number equals the sum of the two preceding numbers.
// Fn = Fn-1 + Fn-2

// Input: the point in the sequence to take a fibonnaci number
// Output: the fibonnaci number at the point in a sequence starting a 0

// Ex:
// At position 0 the Fib number is 0.
// At position 4 the Fib number is 3 (adding 1, 2 which are the numbers before)

// Challenge:
// * Do it with only O(1) space (iteratively using a for loop)

#include "stdio.h"

int fibonnaci(int);

int main() {
	for (int i=0; i < 10; i++) {
		printf("%d\n", fibonnaci(i));
	}

	return 0;
}

int fibonnaci(int n) {
	if (n == 0) {
		return 0;
	}

	int first = 0;
	int second = 1;
	int sum = 0;
	int i = 0;

	while (i < n) {
		sum = first + second;
		first = second;
		second = sum;
		i++;
	}

	return sum;
}
