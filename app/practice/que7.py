def merge(d1, d2):

    result = d1.copy()

    for key, value in d2.items():

        if key not in result:
            result[key] = value

        else:

            # Nested dictionary
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge(result[key], value)

            # List
            elif isinstance(result[key], list) and isinstance(value, list):
                result[key].extend(value)

            # Number
            elif isinstance(result[key], (int, float)) and isinstance(value, (int, float)):
                result[key] += value

            # Otherwise overwrite
            else:
                result[key] = value

    return result


dict1 = {
    "user": {
        "marks": [90, 95]
    }
}

dict2 = {
    "user": {
        "marks": [80],
        "age": 22
    }
}

result = merge(dict1, dict2)

print(result)