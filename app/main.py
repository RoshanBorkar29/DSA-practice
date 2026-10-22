from fastapi import FastAPI,HTTPException,Query
from app.students import get_all_students,create_student as add_student,Student

app = FastAPI()
@app.get("/")
def root():
    return {
    "project": "Student Management API",
    "version": "1.0",
    "developer": "Your Name",
    "total_students": 5
}


""""
1.Get apis-done 
2.Get all students-done
3.get student by id-done
4.student not found-done
5.filter by city-done
6.filter by activve-done
7.search by name-done
8.pagination -first two student-done
9.create studetnt-done
10.update students-done
11.delete student-done
12.multiple path parameters-done
13.mixedpath+query-done
14.sorting-done
15.highest marks-done
16.statistics
17.skill filter
18.city+role
19.emaillookup
"""

@app.get("/students")
def get_students(city:str=None,name:str=None,limit:int=None,
                 sort:str=None):
    students = get_all_students()

    if city is None and name is None and limit is None and sort is None:
        return students

    filtered_students=[]

    for s in students:
        if city is not None and s["city"].lower() != city.lower():
            continue

        if name is not None and s["name"].lower() != name.lower():
            continue

 
        filtered_students.append(s)

    if limit is not None:
            filtered_students=filtered_students[:limit]
    if sort == "age":
        filtered_students=sorted(filtered_students,key=lambda s:s["age"])
    

    return filtered_students
    

##student by id(path parameter)
@app.get("/students/{student_id}")
def get_student(student_id:int):
    students = get_all_students()

    for student in students:
        if student["id"]==student_id:
            return student

    return {
        "message":"Student not found with that id!!"
    }


@app.post("/students")
def create_student(student: Student):
    return add_student(student)

@app.delete("/students/{student_id}")
def remove_student(student_id:int):
    students = get_all_students()

    for index, student in enumerate(students):
        if student["id"] == student_id:
            students.pop(index)
            return {
                "message": "Student deleted successfully"
            }

    return {
        "message":"Student not found with that id!!"
    }


@app.get("/students/{student_id}/marks/{subject}")
def get_marks(student_id:int,subject:str):
    students=get_all_students()
    for s in students:
        if s["id"]==student_id:
            return{
                subject:s["marks"].get(subject)

            }
    return{
        "message":"Student not found"
    }

@app.get("/topper")
def get_topper(subject:str):
    students=get_all_students()
    topper=max(students,key=lambda student: student["marks"][subject])
    return{
        "id":topper["id"],
        "name":topper["name"],
        f"{subject}_marks":topper["marks"][subject]
    }


@app.get("/stats")
def statistics():
    students=get_all_students()
    total_students=len(get_all_students())
    active_students=len([s for s in students if s["active"]])   
    inactive_students=total_students-active_students

    average_age=(
        sum(student["age"] for student in students)/total_students
    )

    return{
        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": inactive_students,
        "average_age": round(average_age,2)
    }

@app.get("/students/skill/{skill}")
def get_students_by_skill(skill:str):
    students=get_all_students()
    result=[]
    for student in students:
        skills=[
            s.lower()
            for s in student["skills"]

        ]
        if skill.lower() in skills:
            result.append({
                "id": student["id"],
                "name": student["name"]
            })

    return result