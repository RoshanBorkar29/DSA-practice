import json
from pathlib import Path
from typing import List,Dict
from pydantic import BaseModel

students = [
    {
        "id": 1,
        "name": "Alice",
        "role": "student",
        "age": 21,
        "active": True,
        "city": "Delhi",
        "email": "alice@example.com",
        "skills": ["python", "fastapi"],
        "marks": {
            "math": 88,
            "science": 91
        }
    },
    {
        "id": 2,
        "name": "Bob",
        "role": "developer",
        "age": 26,
        "active": True,
        "city": "Mumbai",
        "email": "bob@example.com",
        "skills": ["javascript", "api"],
        "marks": {
            "math": 74,
            "science": 85
        }
    },
    {
        "id": 3,
        "name": "Charlie",
        "role": "designer",
        "age": 24,
        "active": False,
        "city": "Pune",
        "email": "charlie@example.com",
        "skills": ["ui", "figma"],
        "marks": {
            "math": 69,
            "science": 77
        }
    },
    {
        "id": 4,
        "name": "Diana",
        "role": "student",
        "age": 22,
        "active": True,
        "city": "Bangalore",
        "email": "diana@example.com",
        "skills": ["python", "data analysis"],
        "marks": {
            "math": 95,
            "science": 89
        }
    },
    {
        "id": 5,
        "name": "Ethan",
        "role": "tester",
        "age": 28,
        "active": True,
        "city": "Hyderabad",
        "email": "ethan@example.com",
        "skills": ["testing", "automation"],
        "marks": {
            "math": 81,
            "science": 83
        }
    }
]
# DATA_FILE=Path(__file__).parent.parent/"data"/"practice_data.json"



def get_all_students()->List[Dict]:
    return students


class Student(BaseModel):
    id: int
    name: str
    role: str
    age: int
    active: bool
    city: str
    email: str
    skills: list[str]
    marks: dict


def create_student(student:Student):
    students.append(student.model_dump())
    return{
        "message": "Student Added Successfully",
        "student": student
    }
