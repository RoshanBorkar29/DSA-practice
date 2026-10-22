text = """
Python is easy.
Python is powerful.
Python is easy to learn.
Learning Python is fun.
"""


"""
You need to find-
1.Frequency of every word
2.Most common word
3.Unique words
4.Words appearing exactly once
"""

freq={}
text=text.lower()
text=text.replace(".","")
words=text.split()

for word in words:
    freq[word]=freq.get(word,0)+1

most_common=max(freq,key=freq.get)
unique_words=set(words)

once=[]
for word in words:
    if freq[word]==1:
        once.append(word)


print(freq)
print(most_common)
print(unique_words)
print(once)

