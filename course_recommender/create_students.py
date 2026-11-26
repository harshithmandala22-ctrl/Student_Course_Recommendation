
import pandas as pd
import random
import os

random.seed(42)

# Create dataset folder if it does not exist
os.makedirs("dataset", exist_ok=True)

interests = [
    "Artificial Intelligence",
    "Data Science",
    "Web Development",
    "Cyber Security",
    "Cloud Computing"
]

career_goals = [
    "AI Engineer",
    "Data Analyst",
    "Web Developer",
    "Security Analyst",
    "Cloud Engineer"
]

skills_list = [
    "Python;Mathematics;Problem Solving",
    "Python;Statistics;Data Analysis",
    "HTML;CSS;JavaScript",
    "Networking;Linux;Security",
    "Python;Cloud;Networking"
]

students = []

for i in range(1, 101):
    interest_index = random.randint(0, 4)

    students.append({
        "student_id": f"S{i:03d}",
        "python_marks": random.randint(40, 100),
        "maths_marks": random.randint(40, 100),
        "programming_marks": random.randint(40, 100),
        "interest": interests[interest_index],
        "skills": skills_list[interest_index],
        "career_goal": career_goals[interest_index]
    })

df = pd.DataFrame(students)

df.to_csv("dataset/students.csv", index=False)

print("Student dataset created successfully!")
print(df.head())
print("Total students:", len(df))
