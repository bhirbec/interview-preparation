# Coding Interview University import backlog

Source: https://github.com/jwasham/coding-interview-university (mined from the
raw `README.md` on `main`). That repo is a study curriculum rather than a
question list, so the concrete, testable problems are almost all the
"Implement: …" exercise checklists (data structures, sorts, graph algorithms,
string searching) plus the handful of explicitly linked practice problems.

Deduped against every folder under `knowledge/coding-questions/` (including
`CTCI/`) and against every URL in every `meta.json` `sources` array. The sibling
backlog `grind-169-backlog.md` was also treated as claimed territory: anything
already listed there is cross-referenced below instead of listed twice.
`leetcode-patterns-backlog.md` did not exist at the time of writing.

Because the curriculum's exercises are given as bullet lists of methods rather
than as problem statements, closely-related bullets are grouped into one
problem (e.g. the whole vector API is one `dynamic-array` question).

Format: `- [ ] Title — difficulty — <source url> — <proposed-folder-name>`.
`[x]` = authored in this repo.

## Arrays

- [x] Implement a Vector (Dynamic Array with Automatic Resizing) — medium — https://github.com/jwasham/coding-interview-university#arrays — dynamic-array

## Linked lists

- [x] Implement a Singly Linked List — medium — https://github.com/jwasham/coding-interview-university#linked-lists — singly-linked-list

## Queue

- [x] Implement a Queue with a Fixed-Size Circular Buffer — easy — https://github.com/jwasham/coding-interview-university#queue — queue-circular-buffer
- [ ] Implement a Queue with a Linked List and Tail Pointer — easy — https://www.coursera.org/lecture/data-structures/queues-EShpq — queue-from-linked-list

## Hash table

- [x] Implement a Hash Table with Linear Probing — medium — https://github.com/jwasham/coding-interview-university#hash-table — hash-table-linear-probing

## Bitwise operations

- [ ] Swap Two Values Without a Temporary Variable — easy — https://bits.stephan-brumme.com/swap.html — xor-swap
- [ ] Absolute Value Without Branching — easy — https://bits.stephan-brumme.com/absInteger.html — absolute-value-no-branch

## Binary search trees

- [ ] Insert into a Binary Search Tree — easy — https://leetcode.com/problems/insert-into-a-binary-search-tree/ — bst-insert
- [ ] Delete a Value from a Binary Search Tree — medium — https://www.youtube.com/watch?v=gcULXE7ViZw — bst-delete-node
- [ ] Find the Min and Max of a Binary Search Tree — easy — https://www.youtube.com/watch?v=Ut90klNN264 — bst-min-max
- [ ] Print BST Values in Sorted Order (in-order traversal) — easy — https://www.youtube.com/watch?v=gm8DUJJhmY4 — bst-inorder-values
- [ ] Count the Nodes in a Binary Tree — easy — https://github.com/jwasham/coding-interview-university#binary-search-trees-bsts — binary-tree-node-count

## Heap / priority queue

- [x] Implement a Max-Heap — medium — https://github.com/jwasham/coding-interview-university#heap--priority-queue--binary-heap — max-heap
- [ ] Heap Sort — medium — https://www.coursera.org/lecture/data-structures/heap-sort-hSzMO — heap-sort

## Sorting

The curriculum's Sorting section has no per-algorithm anchor, so each entry
below cites the specific reference the README links for that algorithm where
one exists, and the section anchor otherwise -- that keeps every `sources` URL
in the catalog unique.

- [x] Merge Sort — medium — https://github.com/jwasham/practice-python/blob/master/merge_sort/merge_sort.py — merge-sort
- [x] Quicksort — medium — https://github.com/jwasham/practice-python/blob/master/quick_sort/quick_sort.py — quicksort
- [x] Insertion Sort — easy — https://github.com/jwasham/coding-interview-university#sorting — insertion-sort
- [ ] Selection Sort — easy — https://youtu.be/g-PGLbMth_g — selection-sort
- [ ] Counting Sort — medium — https://www.youtube.com/watch?v=Nz1KZXbghj8 — counting-sort
- [ ] Radix Sort (LSD) — medium — http://www.cs.yale.edu/homes/aspnes/classes/223/notes.html#radixSort — radix-sort
- [ ] Merge Sort on a Linked List — medium — http://www.geeksforgeeks.org/merge-sort-for-linked-list/ — merge-sort-linked-list

## Graphs

Same story as Sorting: the `#graphs` section lists eleven exercises behind one
anchor, so entries below cite the README's own per-algorithm link where there
is one.

- [x] Breadth-First Search on an Adjacency List — easy — https://github.com/jwasham/coding-interview-university#graphs — graph-bfs-traversal
- [ ] Depth-First Search on an Adjacency List (recursive and iterative) — easy — https://www.youtube.com/watch?v=IBfWDYSffUU — graph-dfs-traversal
- [ ] Detect a Cycle in a Directed Graph — medium — https://www.youtube.com/watch?v=ufj5_bppBsA — detect-cycle-directed-graph
- [ ] Single-Source Shortest Path (Dijkstra) — medium — https://www.youtube.com/watch?v=NSHizBK9JD8 — dijkstra-shortest-path
- [ ] Minimum Spanning Tree (Kruskal or Prim) — medium — https://www.youtube.com/watch?v=tKwnms5iRBU — minimum-spanning-tree
- [ ] Check Whether a Graph is Bipartite — medium — https://www.youtube.com/watch?v=DiedsPsMKXc — check-bipartite-graph
- [ ] List Strongly Connected Components (Kosaraju) — hard — https://www.youtube.com/watch?v=RpgcYiky7uw — strongly-connected-components
- [ ] A* Pathfinding on a Weighted Grid — medium — https://github.com/jwasham/coding-interview-university#a — a-star-pathfinding
- [ ] Maximum Flow (Ford-Fulkerson) — hard — https://github.com/jwasham/coding-interview-university#network-flows — ford-fulkerson-max-flow

## Disjoint sets

- [x] Union-Find with Union by Rank and Path Compression — medium — https://github.com/jwasham/coding-interview-university#disjoint-sets--union-find — union-find-disjoint-set

## String searching

- [ ] Rabin-Karp Substring Search — medium — https://www.coursera.org/lecture/data-structures/rabin-karps-algorithm-c0Qkw — rabin-karp-substring-search
- [ ] Knuth-Morris-Pratt Substring Search — hard — https://www.youtube.com/watch?v=5i7oKodCRJo — kmp-substring-search
- [ ] Boyer-Moore-Horspool Substring Search — hard — https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string_search_algorithm — boyer-moore-horspool-search

## Advanced / probabilistic data structures

- [ ] Bloom Filter — medium — https://github.com/jwasham/coding-interview-university#bloom-filter — bloom-filter
- [ ] Skip List (search, insert, delete) — hard — https://github.com/jwasham/coding-interview-university#skip-lists — skip-list
- [ ] AVL Tree Insertion with Rotations — hard — https://www.coursera.org/learn/data-structures/lecture/PKEBC/avl-tree-implementation — avl-tree-insert
- [ ] Splay Tree (search, insert, delete) — hard — https://github.com/jwasham/coding-interview-university#balanced-search-trees — splay-tree

## Cross-references — claimed by `grind-169-backlog.md`

These curriculum exercises map onto entries already listed in the sibling
backlog, so they are not repeated above:

- Binary search, iterative *and* recursive (`#binary-search`) → `binary-search`.
  The recursive variant is the same problem with a different control flow, so it
  is not split out.
- Count set bits (`#bitwise-operations`) → `number-of-1-bits`.
- `get_height` on a tree (`#binary-search-trees-bsts`, linked to
  geeksforgeeks) → `maximum-depth-binary-tree`.
- `get_successor` on a BST (`#binary-search-trees-bsts`) →
  `inorder-successor-bst`.

## Excluded — already in this catalog

- `is_binary_search_tree` (linked to LeetCode 98) → `CTCI/4.5-validate-bst`.
- Topological sort, and the cycle check that precedes it on a DAG →
  `CTCI/4.7-build-order`.
- Count connected components in a graph → `number-of-provinces`.
- LRU cache (`#caches`) → `lru-cache`.
- Tries (`#tries`) → `implement-trie`.
- Stack implementation (`#stack`) → `min-stack` / `queue-from-stacks`. The
  curriculum itself says "will not implement".
- The DP problems the curriculum's lectures work through — Fibonacci, text
  justification, edit distance, knapsack, parenthesization — are all present as
  `fibonacci-number`, `text-justification`, `edit-distance`, `knapsack`,
  `matrix-chain-multiplication`.

## Skipped — conservative near-duplicates or not implementable

- Linked-list `reverse()` → `reverse-linked-list`; `value_n_from_end(n)` →
  `CTCI/2.2-return-kth-to-last`. Both are folded into the `singly-linked-list`
  API question rather than listed on their own.
- Doubly-linked list: the curriculum explicitly says "no need to implement".
- Design patterns, SOLID, concurrency, testing, networking, system design,
  Big-O analysis, flashcards: knowledge topics with no testable coding output.
- van Emde Boas trees, treaps, k-d trees, HyperLogLog, locality-sensitive
  hashing, FFT, B-trees, red-black and 2-3 trees: listed as reading/watching
  only in the optional-extras section, with no implementation exercise attached.
