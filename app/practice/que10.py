data = {
    "company": {
        "employees": [
            {
                "name": "Alice",
                "skills": ["Python", "SQL"]
            },
            {
                "name": "Bob",
                "skills": ["Java", "Spring"]
            }
        ]
    }
}
query = "company.employees.1.skills.0"

current=data

for part in query.split("."):
    if isinstance(current,dict):
        current=current[part]
    elif isinstance(current,list):
        current=current[int(part)]

print(current)

