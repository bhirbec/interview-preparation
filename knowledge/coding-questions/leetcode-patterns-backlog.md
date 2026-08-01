# LeetCode Patterns import backlog

Source: https://github.com/seanprashad/leetcode-patterns
(`src/data/questions.json`, 179 questions, snapshot dated 2026-07-26).

Deduped against every folder under `knowledge/coding-questions/` (including
`CTCI/`) and against every LeetCode URL appearing in a `meta.json` `sources`
array. Questions that already exist in the catalog are listed at the bottom for
traceability, as are the entries that were skipped because a duplicate was
plausible but not certain — neither group is a candidate for import.

Entries also listed in a sibling backlog (`grind-169-backlog.md`,
`coding-interview-university-backlog.md`) are tagged `[also: sibling backlog]`;
author them from whichever list you pick up first, not twice.

`old/` was grepped too (it holds legacy solutions, not catalog questions, so a
hit there does not disqualify a candidate). The only overlaps are
`old/sort/binary-search.go` (Binary Search) and `old/tree/trie.go` +
`old/tree/trie.md` (Implement Trie, already in the catalog as `implement-trie`).

Format: `- [ ] Title — difficulty — <leetcode url> — <proposed-folder-name>`.
`[x]` = authored in this repo.

Patterns flagged **(gap)** are underrepresented in the current catalog.

## Sliding Window **(gap — only `longest-substring-without-repeats` and `longest-subarray-sum-at-most-k`)**

- [x] Maximum Average Subarray I — easy — https://leetcode.com/problems/maximum-average-subarray-i/ — maximum-average-subarray-i  [fixed-size window, distinct from `maximum-subarray`]
- [ ] Find K Closest Elements — medium — https://leetcode.com/problems/find-k-closest-elements/ — find-k-closest-elements  [distinct from `k-closest-points` (1-D binary search, not a heap of points)]
- [x] Fruit Into Baskets — medium — https://leetcode.com/problems/fruit-into-baskets/ — fruit-into-baskets
- [x] Longest Repeating Character Replacement — medium — https://leetcode.com/problems/longest-repeating-character-replacement/ — longest-repeating-character-replacement
- [ ] Minimum Size Subarray Sum — medium — https://leetcode.com/problems/minimum-size-subarray-sum/ — minimum-size-subarray-sum  [distinct from `longest-subarray-sum-at-most-k` and `subarray-sum-to-target`]
- [ ] Permutation in String — medium — https://leetcode.com/problems/permutation-in-string/ — permutation-in-string
- [ ] Subarray Product Less Than K — medium — https://leetcode.com/problems/subarray-product-less-than-k/ — subarray-product-less-than-k
- [ ] Minimum Window Substring — hard — https://leetcode.com/problems/minimum-window-substring/ — minimum-window-substring  [also: sibling backlog]
- [ ] Sliding Window Maximum — hard — https://leetcode.com/problems/sliding-window-maximum/ — sliding-window-maximum
- [ ] Sliding Window Median — hard — https://leetcode.com/problems/sliding-window-median/ — sliding-window-median
- [ ] Smallest Range Covering Elements from K Lists — hard — https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/ — smallest-range-covering-elements-from-k-lists
- [ ] Substring with Concatenation of All Words — hard — https://leetcode.com/problems/substring-with-concatenation-of-all-words/ — substring-with-concatenation-of-all-words

## Two Pointers

- [ ] Backspace String Compare — easy — https://leetcode.com/problems/backspace-string-compare/ — backspace-string-compare  [also: sibling backlog]
- [ ] Is Subsequence — easy — https://leetcode.com/problems/is-subsequence/ — is-subsequence
- [ ] Linked List Cycle — easy — https://leetcode.com/problems/linked-list-cycle/ — linked-list-cycle  [also: sibling backlog]
- [ ] Middle of the Linked List — easy — https://leetcode.com/problems/middle-of-the-linked-list/ — middle-of-the-linked-list  [also: sibling backlog]
- [ ] Move Zeroes — easy — https://leetcode.com/problems/move-zeroes/ — move-zeroes  [also: sibling backlog]
- [ ] Palindrome Linked List — easy — https://leetcode.com/problems/palindrome-linked-list/ — palindrome-linked-list  [also: sibling backlog]
- [x] Squares of a Sorted Array — easy — https://leetcode.com/problems/squares-of-a-sorted-array/ — squares-of-a-sorted-array
- [ ] 3Sum Closest — medium — https://leetcode.com/problems/3sum-closest/ — three-sum-closest  [distinct objective from the existing `three-sum` / `three-sum-zero`]
- [ ] Container With Most Water — medium — https://leetcode.com/problems/container-with-most-water/ — container-with-most-water  [also: sibling backlog]
- [ ] Find the Duplicate Number — medium — https://leetcode.com/problems/find-the-duplicate-number/ — find-the-duplicate-number
- [ ] Interval List Intersections — medium — https://leetcode.com/problems/interval-list-intersections/ — interval-list-intersections
- [ ] Linked List Cycle II — medium — https://leetcode.com/problems/linked-list-cycle-ii/ — linked-list-cycle-ii
- [ ] Longest Palindromic Substring — medium — https://leetcode.com/problems/longest-palindromic-substring/ — longest-palindromic-substring  [also: sibling backlog; distinct from the existing `longest-palindrome` (which rearranges characters)]
- [ ] Reorder List — medium — https://leetcode.com/problems/reorder-list/ — reorder-list
- [ ] Rotate Array — medium — https://leetcode.com/problems/rotate-array/ — rotate-array
- [ ] Rotate List — medium — https://leetcode.com/problems/rotate-list/ — rotate-list
- [ ] Sort Colors — medium — https://leetcode.com/problems/sort-colors/ — sort-colors  [also: sibling backlog]
- [ ] Sort List — medium — https://leetcode.com/problems/sort-list/ — sort-list
- [ ] Find Median from Data Stream — hard — https://leetcode.com/problems/find-median-from-data-stream/ — find-median-from-data-stream  [also: sibling backlog]

## Binary Search

- [ ] Binary Search — easy — https://leetcode.com/problems/binary-search/ — binary-search  [also: sibling backlog; a Go version exists at `old/sort/binary-search.go`, but not in the catalog]
- [ ] Find Smallest Letter Greater Than Target — easy — https://leetcode.com/problems/find-smallest-letter-greater-than-target/ — find-smallest-letter-greater-than-target
- [ ] Missing Number — easy — https://leetcode.com/problems/missing-number/ — missing-number  [also: sibling backlog]
- [ ] Find Minimum in Rotated Sorted Array — medium — https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/ — find-minimum-in-rotated-sorted-array  [distinct objective from `CTCI/10.3-search-in-rotated-array`]
- [x] Find Peak Element — medium — https://leetcode.com/problems/find-peak-element/ — find-peak-element
- [ ] Kth Smallest Element in a Sorted Matrix — medium — https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/ — kth-smallest-element-in-a-sorted-matrix  [distinct from `kth-smallest-element` (sorted-matrix binary search)]
- [ ] Peak Index in a Mountain Array — medium — https://leetcode.com/problems/peak-index-in-a-mountain-array/ — peak-index-in-a-mountain-array
- [ ] Search a 2D Matrix — medium — https://leetcode.com/problems/search-a-2d-matrix/ — search-a-2d-matrix
- [ ] Search a 2D Matrix II — medium — https://leetcode.com/problems/search-a-2d-matrix-ii/ — search-a-2d-matrix-ii
- [ ] Count of Range Sum — hard — https://leetcode.com/problems/count-of-range-sum/ — count-of-range-sum

## Backtracking

- [ ] Binary Tree Paths — easy — https://leetcode.com/problems/binary-tree-paths/ — binary-tree-paths
- [ ] Combination Sum II — medium — https://leetcode.com/problems/combination-sum-ii/ — combination-sum-ii  [each number used at most once; distinct from `combination-sum`]
- [ ] Combination Sum III — medium — https://leetcode.com/problems/combination-sum-iii/ — combination-sum-iii  [fixed count of distinct digits 1-9; distinct from `combination-sum`]
- [ ] Combinations — medium — https://leetcode.com/problems/combinations/ — combinations
- [ ] Factor Combinations — medium — https://leetcode.com/problems/factor-combinations/ — factor-combinations  [LeetCode premium]
- [ ] Generalized Abbreviation — medium — https://leetcode.com/problems/generalized-abbreviation/ — generalized-abbreviation  [LeetCode premium]
- [ ] Letter Combinations of a Phone Number — medium — https://leetcode.com/problems/letter-combinations-of-a-phone-number/ — letter-combinations-of-a-phone-number  [also: sibling backlog]
- [ ] Palindrome Partitioning — medium — https://leetcode.com/problems/palindrome-partitioning/ — palindrome-partitioning
- [ ] Partition to K Equal Sum Subsets — medium — https://leetcode.com/problems/partition-to-k-equal-sum-subsets/ — partition-to-k-equal-sum-subsets
- [ ] Path Sum II — medium — https://leetcode.com/problems/path-sum-ii/ — path-sum-ii
- [ ] Permutations II — medium — https://leetcode.com/problems/permutations-ii/ — permutations-ii  [duplicate-tolerant variant of `CTCI/8.7-permutations-without-dups`]
- [ ] Subsets II — medium — https://leetcode.com/problems/subsets-ii/ — subsets-ii  [duplicate-tolerant variant of `CTCI/8.4-power-set`]
- [ ] Target Sum — medium — https://leetcode.com/problems/target-sum/ — target-sum
- [ ] Sudoku Solver — hard — https://leetcode.com/problems/sudoku-solver/ — sudoku-solver
- [ ] Word Search II — hard — https://leetcode.com/problems/word-search-ii/ — word-search-ii  [trie-backed multi-word variant of `word-search-grid`]
- [ ] Word Squares — hard — https://leetcode.com/problems/word-squares/ — word-squares  [LeetCode premium]

## Trie **(gap — only `implement-trie`)**

- [ ] Index Pairs of a String — easy — https://leetcode.com/problems/index-pairs-of-a-string/ — index-pairs-of-a-string  [LeetCode premium]
- [ ] Design Add and Search Words Data Structure — medium — https://leetcode.com/problems/design-add-and-search-words-data-structure/ — design-add-and-search-words-data-structure  [also: sibling backlog]
- [x] Longest Word in Dictionary — medium — https://leetcode.com/problems/longest-word-in-dictionary/ — longest-word-in-dictionary
- [ ] Word Break — medium — https://leetcode.com/problems/word-break/ — word-break  [also: sibling backlog]
- [ ] Concatenated Words — hard — https://leetcode.com/problems/concatenated-words/ — concatenated-words
- [ ] Design Search Autocomplete System — hard — https://leetcode.com/problems/design-search-autocomplete-system/ — design-search-autocomplete-system  [LeetCode premium]
- [ ] Prefix and Suffix Search — hard — https://leetcode.com/problems/prefix-and-suffix-search/ — prefix-and-suffix-search

## Heap (Priority Queue) **(gap — only `max-heap`, `k-closest-points`, `merge-m-sorted-arrays`)**

- [ ] Find K Pairs with Smallest Sums — medium — https://leetcode.com/problems/find-k-pairs-with-smallest-sums/ — find-k-pairs-with-smallest-sums
- [ ] Reorganize String — medium — https://leetcode.com/problems/reorganize-string/ — reorganize-string
- [ ] Sort Characters By Frequency — medium — https://leetcode.com/problems/sort-characters-by-frequency/ — sort-characters-by-frequency
- [x] Top K Frequent Elements — medium — https://leetcode.com/problems/top-k-frequent-elements/ — top-k-frequent-elements
- [ ] Employee Free Time — hard — https://leetcode.com/problems/employee-free-time/ — employee-free-time  [LeetCode premium]
- [ ] Rearrange String k Distance Apart — hard — https://leetcode.com/problems/rearrange-string-k-distance-apart/ — rearrange-string-k-distance-apart  [LeetCode premium]

## Union-Find **(gap — only `union-find-disjoint-set` and `number-of-provinces`)**

- [ ] Graph Valid Tree — medium — https://leetcode.com/problems/graph-valid-tree/ — graph-valid-tree  [LeetCode premium; also: sibling backlog]
- [x] Longest Consecutive Sequence — medium — https://leetcode.com/problems/longest-consecutive-sequence/ — longest-consecutive-sequence

## Topological Sort **(gap — only `CTCI/4.7-build-order`)**

- [ ] Course Schedule — medium — https://leetcode.com/problems/course-schedule/ — course-schedule  [also: sibling backlog]
- [ ] Minimum Height Trees — medium — https://leetcode.com/problems/minimum-height-trees/ — minimum-height-trees  [also: sibling backlog]
- [ ] Alien Dictionary — hard — https://leetcode.com/problems/alien-dictionary/ — alien-dictionary  [LeetCode premium]

## Monotonic Stack **(gap — only `daily-temperatures`)**

- [ ] Maximum Binary Tree — medium — https://leetcode.com/problems/maximum-binary-tree/ — maximum-binary-tree

## Prefix Sum **(gap — nothing in the catalog uses a prefix-sum array explicitly)**

- [x] Range Sum Query - Immutable — easy — https://leetcode.com/problems/range-sum-query-immutable/ — range-sum-query-immutable

## Dynamic Programming

- [ ] Counting Bits — easy — https://leetcode.com/problems/counting-bits/ — counting-bits  [also: sibling backlog; distinct from `bit-strings-by-popcount`]
- [ ] Best Time to Buy and Sell Stock with Cooldown — medium — https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/ — best-time-to-buy-and-sell-stock-with-cooldown
- [ ] Combination Sum IV — medium — https://leetcode.com/problems/combination-sum-iv/ — combination-sum-iv  [counts ordered permutations (a DP, not backtracking)]
- [ ] Decode Ways — medium — https://leetcode.com/problems/decode-ways/ — decode-ways
- [ ] House Robber II — medium — https://leetcode.com/problems/house-robber-ii/ — house-robber-ii
- [ ] Jump Game — medium — https://leetcode.com/problems/jump-game/ — jump-game
- [ ] Maximum Product Subarray — medium — https://leetcode.com/problems/maximum-product-subarray/ — maximum-product-subarray  [also: sibling backlog]
- [x] Non-overlapping Intervals — medium — https://leetcode.com/problems/non-overlapping-intervals/ — non-overlapping-intervals
- [ ] Number of Longest Increasing Subsequence — medium — https://leetcode.com/problems/number-of-longest-increasing-subsequence/ — number-of-longest-increasing-subsequence
- [ ] Binary Tree Maximum Path Sum — hard — https://leetcode.com/problems/binary-tree-maximum-path-sum/ — binary-tree-maximum-path-sum
- [ ] Count Unique Characters of All Substrings of a Given String — hard — https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/ — count-unique-characters-of-all-substrings-of-a-given-string

## Greedy **(gap — only `merge-intervals` / `task-cooldown` lean greedy)**

- [ ] Gas Station — medium — https://leetcode.com/problems/gas-station/ — gas-station  [also: sibling backlog]
- [ ] Minimum Number of Arrows to Burst Balloons — medium — https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/ — minimum-number-of-arrows-to-burst-balloons

## Divide and Conquer **(gap — only `merge-sort`, `quicksort`, `median-of-two-sorted-arrays`)**

- [ ] Majority Element — easy — https://leetcode.com/problems/majority-element/ — majority-element  [also: sibling backlog]
- [ ] Number of 1 Bits — easy — https://leetcode.com/problems/number-of-1-bits/ — number-of-1-bits  [also: sibling backlog]
- [ ] Reverse Bits — easy — https://leetcode.com/problems/reverse-bits/ — reverse-bits  [also: sibling backlog]
- [ ] Construct Binary Tree from Preorder and Inorder Traversal — medium — https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/ — construct-binary-tree-from-preorder-and-inorder-traversal  [also: sibling backlog]

## Depth-First Search

- [ ] Average of Levels in Binary Tree — easy — https://leetcode.com/problems/average-of-levels-in-binary-tree/ — average-of-levels-in-binary-tree
- [ ] Invert Binary Tree — easy — https://leetcode.com/problems/invert-binary-tree/ — invert-binary-tree  [also: sibling backlog]
- [ ] Maximum Depth of Binary Tree — easy — https://leetcode.com/problems/maximum-depth-of-binary-tree/ — maximum-depth-of-binary-tree  [also: sibling backlog]
- [ ] Merge Two Binary Trees — easy — https://leetcode.com/problems/merge-two-binary-trees/ — merge-two-binary-trees
- [ ] Minimum Depth of Binary Tree — easy — https://leetcode.com/problems/minimum-depth-of-binary-tree/ — minimum-depth-of-binary-tree
- [ ] Path Sum — easy — https://leetcode.com/problems/path-sum/ — path-sum
- [ ] Same Tree — easy — https://leetcode.com/problems/same-tree/ — same-tree  [distinct from `isomorphic-trees` (no child swapping allowed)]
- [ ] All Nodes Distance K in Binary Tree — medium — https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/ — all-nodes-distance-k-in-binary-tree
- [ ] Binary Tree Right Side View — medium — https://leetcode.com/problems/binary-tree-right-side-view/ — binary-tree-right-side-view  [also: sibling backlog]
- [ ] Clone Graph — medium — https://leetcode.com/problems/clone-graph/ — clone-graph  [also: sibling backlog]
- [ ] Kth Smallest Element in a BST — medium — https://leetcode.com/problems/kth-smallest-element-in-a-bst/ — kth-smallest-element-in-a-bst  [also: sibling backlog; distinct from `kth-smallest-element` (BST in-order walk)]
- [ ] Lowest Common Ancestor of a Binary Search Tree — medium — https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/ — lowest-common-ancestor-of-a-binary-search-tree  [also: sibling backlog]
- [ ] Lowest Common Ancestor of a Binary Tree — medium — https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/ — lowest-common-ancestor-of-a-binary-tree  [also: sibling backlog]
- [ ] Maximum Width of Binary Tree — medium — https://leetcode.com/problems/maximum-width-of-binary-tree/ — maximum-width-of-binary-tree
- [ ] Pacific Atlantic Water Flow — medium — https://leetcode.com/problems/pacific-atlantic-water-flow/ — pacific-atlantic-water-flow
- [ ] Path Sum III — medium — https://leetcode.com/problems/path-sum-iii/ — path-sum-iii
- [ ] Serialize and Deserialize Binary Tree — hard — https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ — serialize-and-deserialize-binary-tree  [also: sibling backlog]

## Breadth-First Search

- [ ] Binary Tree Level Order Traversal II — medium — https://leetcode.com/problems/binary-tree-level-order-traversal-ii/ — binary-tree-level-order-traversal-ii
- [ ] Binary Tree Zigzag Level Order Traversal — medium — https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/ — binary-tree-zigzag-level-order-traversal

## Linked List

- [ ] Remove Linked List Elements — easy — https://leetcode.com/problems/remove-linked-list-elements/ — remove-linked-list-elements
- [ ] Odd Even Linked List — medium — https://leetcode.com/problems/odd-even-linked-list/ — odd-even-linked-list
- [ ] Reverse Linked List II — medium — https://leetcode.com/problems/reverse-linked-list-ii/ — reverse-linked-list-ii  [sublist reversal, distinct from the existing `reverse-linked-list`]
- [ ] Swap Nodes in Pairs — medium — https://leetcode.com/problems/swap-nodes-in-pairs/ — swap-nodes-in-pairs
- [ ] Reverse Nodes in k-Group — hard — https://leetcode.com/problems/reverse-nodes-in-k-group/ — reverse-nodes-in-k-group

## Stack

- [ ] Maximum Frequency Stack — hard — https://leetcode.com/problems/maximum-frequency-stack/ — maximum-frequency-stack

## Matrix

- [ ] Convert 1D Array Into 2D Array — easy — https://leetcode.com/problems/convert-1d-array-into-2d-array/ — convert-1d-array-into-2d-array
- [ ] Set Matrix Zeroes — medium — https://leetcode.com/problems/set-matrix-zeroes/ — set-matrix-zeroes

## Bit Manipulation

- [ ] Single Number — easy — https://leetcode.com/problems/single-number/ — single-number  [also: sibling backlog]

## Design **(gap — only `lru-cache`, `min-stack`, `implement-trie`)**

- [ ] Encode and Decode Strings — medium — https://leetcode.com/problems/encode-and-decode-strings/ — encode-and-decode-strings  [LeetCode premium]

## Sorting

- [ ] Find All Duplicates in an Array — medium — https://leetcode.com/problems/find-all-duplicates-in-an-array/ — find-all-duplicates-in-an-array

## Hash Table

- [ ] Find All Numbers Disappeared in an Array — easy — https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/ — find-all-numbers-disappeared-in-an-array
- [ ] Two Sum — easy — https://leetcode.com/problems/two-sum/ — two-sum  [also: sibling backlog]
- [ ] First Missing Positive — hard — https://leetcode.com/problems/first-missing-positive/ — first-missing-positive  [also: sibling backlog]

## Array

- [ ] Insert Interval — medium — https://leetcode.com/problems/insert-interval/ — insert-interval  [also: sibling backlog]

## Skipped — already in the catalog

Matched by folder name (loosely, allowing for renames) or by an identical
LeetCode URL in an existing `meta.json`. Do not import.

- 3Sum — https://leetcode.com/problems/3sum/ — already: `three-sum-zero (and three-sum)`
- Add Two Numbers — https://leetcode.com/problems/add-two-numbers/ — already: `CTCI/2.5-sum-lists`
- Combination Sum — https://leetcode.com/problems/combination-sum/ — already: `combination-sum`
- Generate Parentheses — https://leetcode.com/problems/generate-parentheses/ — already: `CTCI/8.9-parens`
- Group Anagrams — https://leetcode.com/problems/group-anagrams/ — already: `CTCI/10.2-group-anagrams`
- House Robber — https://leetcode.com/problems/house-robber/ — already: `max-non-adjacent-sum`
- Implement Trie (Prefix Tree) — https://leetcode.com/problems/implement-trie-prefix-tree/ — already: `implement-trie (same URL in sources)`
- K Closest Points to Origin — https://leetcode.com/problems/k-closest-points-to-origin/ — already: `k-closest-points (same URL in sources)`
- Kth Largest Element in an Array — https://leetcode.com/problems/kth-largest-element-in-an-array/ — already: `kth-smallest-element`
- Longest Common Subsequence — https://leetcode.com/problems/longest-common-subsequence/ — already: `longest-common-subsequence`
- Longest Increasing Subsequence — https://leetcode.com/problems/longest-increasing-subsequence/ — already: `longest-increasing-subsequence`
- Longest Substring Without Repeating Characters — https://leetcode.com/problems/longest-substring-without-repeating-characters/ — already: `longest-substring-without-repeats`
- Maximum Subarray — https://leetcode.com/problems/maximum-subarray/ — already: `maximum-subarray`
- Median of Two Sorted Arrays — https://leetcode.com/problems/median-of-two-sorted-arrays/ — already: `median-of-two-sorted-arrays`
- Meeting Rooms — https://leetcode.com/problems/meeting-rooms/ — already: `meeting-rooms (same URL in sources)`
- Merge Intervals — https://leetcode.com/problems/merge-intervals/ — already: `merge-intervals`
- N-Queens — https://leetcode.com/problems/n-queens/ — already: `CTCI/8.12-eight-queens`
- Number of Connected Components in an Undirected Graph — https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/ — already: `number-of-provinces`
- Palindromic Substrings — https://leetcode.com/problems/palindromic-substrings/ — already: `count-palindromic-substrings`
- Permutations — https://leetcode.com/problems/permutations/ — already: `CTCI/8.7-permutations-without-dups`
- Product of Array Except Self — https://leetcode.com/problems/product-of-array-except-self/ — already: `product-of-array-except-self`
- Reverse Linked List — https://leetcode.com/problems/reverse-linked-list/ — already: `reverse-linked-list`
- Rotate Image — https://leetcode.com/problems/rotate-image/ — already: `CTCI/1.7-rotate-matrix`
- Search in Rotated Sorted Array — https://leetcode.com/problems/search-in-rotated-sorted-array/ — already: `CTCI/10.3-search-in-rotated-array`
- Spiral Matrix — https://leetcode.com/problems/spiral-matrix/ — already: `spiral-matrix`
- Subsets — https://leetcode.com/problems/subsets/ — already: `CTCI/8.4-power-set`
- Subtree of Another Tree — https://leetcode.com/problems/subtree-of-another-tree/ — already: `CTCI/4.10-check-subtree`
- Sum of Two Integers — https://leetcode.com/problems/sum-of-two-integers/ — already: `CTCI/17.1-add-without-plus`
- Trapping Rain Water — https://leetcode.com/problems/trapping-rain-water/ — already: `trapping-rain-water`
- Valid Anagram — https://leetcode.com/problems/valid-anagram/ — already: `CTCI/1.2-check-permutation`
- Valid Parentheses — https://leetcode.com/problems/valid-parentheses/ — already: `valid-braces`
- Validate Binary Search Tree — https://leetcode.com/problems/validate-binary-search-tree/ — already: `CTCI/4.5-validate-bst`
- Word Search — https://leetcode.com/problems/word-search/ — already: `word-search-grid`

## Skipped — possible duplicate, judgement call

Close enough to an existing folder that importing would likely duplicate
practice value. Listed rather than imported; revisit if you decide the variant
is worth its own question.

- Best Time to Buy and Sell Stock — easy — https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ — mirror image of `biggest-loss`
- Binary Tree Level Order Traversal — medium — https://leetcode.com/problems/binary-tree-level-order-traversal/ — same traversal as `CTCI/4.3-list-of-depths`
- Climbing Stairs — easy — https://leetcode.com/problems/climbing-stairs/ — the Fibonacci recurrence already covered by `fibonacci-number`
- Coin Change — medium — https://leetcode.com/problems/coin-change/ — overlaps `CTCI/8.11-coins` (also claimed by grind-169-backlog.md)
- Contains Duplicate — easy — https://leetcode.com/problems/contains-duplicate/ — same core check as `CTCI/1.1-is-unique`
- Course Schedule II — medium — https://leetcode.com/problems/course-schedule-ii/ — same output as `CTCI/4.7-build-order` (topological order)
- Letter Case Permutation — medium — https://leetcode.com/problems/letter-case-permutation/ — same shape as `binary-wildcard-combinations`
- Meeting Rooms II — medium — https://leetcode.com/problems/meeting-rooms-ii/ — same max-concurrency sweep as `peak-traffic-time`
- Merge Two Sorted Lists — easy — https://leetcode.com/problems/merge-two-sorted-lists/ — overlaps `CTCI/10.1-sorted-merge` and `merge-m-sorted-arrays`
- Merge k Sorted Lists — hard — https://leetcode.com/problems/merge-k-sorted-lists/ — overlaps `merge-m-sorted-arrays` (heap merge of k sorted sequences)
- Number of Islands — medium — https://leetcode.com/problems/number-of-islands/ — very close to `biggest-island` (same flood fill; counts islands instead of sizing the largest)
- Partition Equal Subset Sum — medium — https://leetcode.com/problems/partition-equal-subset-sum/ — subset-sum variant of `knapsack` (also claimed by grind-169-backlog.md)
- Remove Duplicates from Sorted List — easy — https://leetcode.com/problems/remove-duplicates-from-sorted-list/ — overlaps `remove-duplicates-linked-list` and `CTCI/2.1-remove-dups`
- Remove Nth Node From End of List — medium — https://leetcode.com/problems/remove-nth-node-from-end-of-list/ — same two-pointer trick as `CTCI/2.2-return-kth-to-last`
- Search in Rotated Sorted Array II — medium — https://leetcode.com/problems/search-in-rotated-sorted-array-ii/ — duplicates-allowed variant of `CTCI/10.3-search-in-rotated-array`
- Task Scheduler — medium — https://leetcode.com/problems/task-scheduler/ — overlaps `task-cooldown`
- Unique Paths — medium — https://leetcode.com/problems/unique-paths/ — overlaps `CTCI/8.2-robot-in-a-grid` (also claimed by grind-169-backlog.md)
- Valid Palindrome — easy — https://leetcode.com/problems/valid-palindrome/ — overlaps `check-palindrome`

Totals: 179 source questions — 33 already in the catalog, 18 skipped as possible duplicates, 128 candidates above (10 authored so far).
