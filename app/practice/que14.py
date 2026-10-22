docs = {
    1: "Python is easy",
    2: "Java is powerful",
    3: "Python and Java",
    4: "Python Java SQL"
}

index={}

for id,text in docs.items():
    words=text.lower().split()
    for word in words:
        if word not in index:
            index[word]=set()
        index[word].add(id)


def search(query):
    words=query.lower().split()
    if words[0] not in index:
        return []

    result=index[words[0]]

    for word in words:
        
            if word not in index:
                return []
        
            result=result.intersection(index[word])
    return sorted(result)

print(search("python"))

print(search("python java"))