# Hashtable

Source: [Coursera - Algorithm Design & Analysis](https://www.coursera.org/learn/algorithm-design-analysis/lecture/b2Uee/hash-tables-operations-and-applications)

## Introduction
Purpose: maintain a possibly evolving set of data. 

| Operations | Running Time |
| --- | --- |
| Insert | O(1) |
| Delete | O(1) |
| Lookup | O(1) |

Applications:
- de-duplication problem (distinct visitor, distinct documents...)
- 2-sum problem
- symbol tables in compilers
- blocking network traffic (black list IP address)

## High-level Idea

**Setup:**
Universe U (all IPs, all names, all chess board configurations...)

**Goal:**
Want to maintain an evolving set S &sube; U 

**Solution:**
- pick n = # of bucket with n = |S| (for simplification we assume that |S| doesn't change)
- choose a Hash function h: U -> {0, 1, 2, ..., n-1}
- use array A of length n, store x in A[h(x)]

**Collision:** distinct x, y &isin; U such that h(x) == h(y)

**Solution:**
- chaining: keep a list list in each bucket (take more space). Insert new object at the beginning 
of the linked list.
- open addressing: only one object per bucket (deletion is more complex here)
    - linear probing: probe the hash table by incrementing by one 
    - double hashing: probe the hash table with an offset given by another hash function

## Hash Function

### Property of a good hash table

- we want the hash function to spread the data uniformly amongs the buckets (performance depends on the hash function). Gold standard (complety random hashing)
- should be easy to solve / very fast to evaluate

### Bad Hash Function (very easy to do :):

keys = phone numbers (10-digits) 
size of U = 10^10
choose 1000 buckets 

terrible: take the first 3 digits of x

mediocre: take the last 3 digits of x

### Quick-and-Dirty Hash Function

```
Object -------------> Int -----------> bucket {0, 1, 2, ... n-1}
         Hash code        Compression
```

Hash code ex: running sum of each char of a string

Compression: mod function

How to choose n with mod:
- choose n to be prime number 
- do not choose a power of 2
- do not choose a power of 10


### The Load Factor (&Alpha;)

```
         # of objects
Alpha =  ------------
         # of buckets
```

Note about Chaining: If load factor is greater than 1 then only Chainingg is possible. However, we need &Alpha; << 1 to have good performance so we need to control the load factor.

### Pathological Sata Set 

For all hash functions there is a pathological data set which maps to a single bucket.

Solution:
- use a cryptographic hash function (SHA-2). It almost impossible to find what is the pathological data set
- use randomization: design a family H of hash function and choose one randomly at run time (we can still publish 
the code but no one will be able to find the one that will be used)

## Universal Hashing
