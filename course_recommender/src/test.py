print("====================================")
print(" STUDENT COURSE RECOMMENDATION SYSTEM")
print("====================================")

student_name = input("Enter student name: ")
python_marks = float(input("Enter Python marks: "))
maths_marks = float(input("Enter Mathematics marks: "))

print("\nStudent Details")
print("Name:", student_name)
print("Python Marks:", python_marks)
print("Mathematics Marks:", maths_marks)

average = (python_marks + maths_marks) / 2

print("Average Marks:", average)

if average >= 80:
    print("Academic Performance: Excellent")
elif average >= 60:
    print("Academic Performance: Good")
else:
    print("Academic Performance: Needs Improvement")
