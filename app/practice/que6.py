data = {
    "user": {
        "name": "John",
        "skills": ["Python", "C++", "SQL"],
        "address": {
            "city": "Pune",
            "pin": 411001
        }
    },
    "age": 22
}

result = {}

def flatten(data, parent=""):

    # Handle Dictionary
    if isinstance(data, dict):

        for key, value in data.items():

            new_key = key if parent == "" else f"{parent}.{key}"

            flatten(value, new_key)

    # Handle List
    elif isinstance(data, list):

        for index, value in enumerate(data):

            new_key = f"{parent}.{index}"

            flatten(value, new_key)

    # Handle Normal Value
    else:
        result[parent] = data


flatten(data)

print(result)