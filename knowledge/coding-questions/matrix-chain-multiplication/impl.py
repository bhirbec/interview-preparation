# Matrix Chain Multiplication
#
# Matrix multiplication is associative: A @ B @ C can be computed as (A @ B) @ C
# or A @ (B @ C) — the result is the same, but the amount of work is not.
# Multiplying a p x q matrix by a q x r matrix costs p * q * r scalar
# multiplications.
#
# You are given the chain's dimensions as a list `dims` of length n + 1, where
# matrix i (0-based) has shape dims[i] x dims[i + 1]. Return the minimum total
# number of scalar multiplications needed to compute the full product.
#
# Constraints:
#   - 2 <= len(dims) <= 100
#   - dimensions are positive integers
#
# Examples:
#   min_multiplications([10, 20, 30])     == 6000
#     # a single 10x20 @ 20x30 product
#   min_multiplications([10, 20, 30, 40]) == 18000
#     # (A @ B) @ C: 6000 + 12000; the other order costs 32000
#   min_multiplications([30, 35, 15, 5, 10, 20, 25]) == 15125  # classic CLRS
#   min_multiplications([5, 10])          == 0
#     # one matrix, nothing to multiply


def min_multiplications(dims):
  # TODO: implement
  raise NotImplementedError
