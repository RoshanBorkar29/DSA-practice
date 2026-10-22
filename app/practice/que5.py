words = ["eat", "tea", "bat", "ate", "cat", "tac"]

anagrams={}

for word in words:
    key=sorted(word)
    key=''.join(sorted(key))
    if key not in anagrams:
        anagrams[key]=[]
        
    anagrams[key].append(word)

print(list(anagrams.values()))



