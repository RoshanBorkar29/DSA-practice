students = {
    "Alice": [90, 85, 88],
    "Bob": [70, 80, 75],
    "Charlie": [95, 91, 99]
}
"""
1.Display all student-done
2.Topper 
3.average of each student
4.students scoring above class average
5.class average


"""
avg_marks={}

for name,marks in students.items():
    print(f"Name of student = {name} ->Marks:{marks} -> Highest Marks :{max(marks)}")
    total=sum(marks)
    average=total/len(marks)
    avg_marks[name]=round(average,2)
    
print(avg_marks)
topper=max(avg_marks,key=avg_marks.get)
# print(topper)
average=sum(avg_marks.values())/len(students)
print(average)


for name,avg in avg_marks.items():
    if avg>=average:
        print(f"Student {name}  has an average of {avg}")


