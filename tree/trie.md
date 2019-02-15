# Trie 


Tree data use to store a collection of string. If two strings have the same prefix then they share the same ancestor. 

Example of applications:
- store a dictionnary (less space than a hash table)
- need to do prefix-based search
- sorted lexographically

Trie is made up of Trie Node. A Trie Node has two components:
- a map[string]Node (could be a array if you know the number of different characters)
- boolean to indicate end of work

Insertion: O(length of word)
Search: O(length of word)
