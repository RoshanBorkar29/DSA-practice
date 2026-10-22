filesystem={}
##create a folder

def mkdir(path):
    current=filesystem
    for folder in path.split("/"):
        current=current.setdefault(folder,{})


def touch(path):
    parts=path.split("/")
    current=filesystem
    for part in parts[:-1]:
        current=current.setdefault(part,{})

    current[parts[-1]]=None


def ls(path):
    parts=path.split("/")
    current=filesystem

    for folder in parts:
        current=current[folder]

    for item in current:
        print(item)


def rm(path):
    parts=path.split("/")
    current=filesystem

    for folder in parts[:-1]:
        current=current[folder]

    del current[parts[-1]]


# ------------------------

mkdir("docs")
mkdir("docs/python")
print(filesystem)
touch("docs/python/main.py")
touch("docs/python/test.py")
print(filesystem)
print("Before Delete:")
ls("docs/python")

rm("docs/python/test.py")

print("\nAfter Delete:")
ls("docs/python")