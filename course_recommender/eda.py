
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find the project folder automatically
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load datasets
students = pd.read_csv(DATASET_DIR / "students.csv")
courses = pd.read_csv(DATASET_DIR / "courses.csv")

print("\n===== STUDENT DATASET =====")
print("Number of students:", len(students))
print("Dataset shape:", students.shape)

print("\nFirst 5 student records:")
print(students.head())

print("\nMissing values:")
print(students.isnull().sum())

print("\nDuplicate records:", students.duplicated().sum())

# Remove duplicate students
students = students.drop_duplicates(subset="student_id")

# Fill missing numerical values with the median
marks_columns = [
    "python_marks",
    "maths_marks",
    "programming_marks"
]

for column in marks_columns:
    students[column] = students[column].fillna(
        students[column].median()
    )

# Fill missing text values with the most common value
text_columns = ["interest", "skills", "career_goal"]

for column in text_columns:
    students[column] = students[column].fillna(
        students[column].mode()[0]
    )

# Calculate average marks
students["average_marks"] = students[marks_columns].mean(axis=1).round(2)

# Save cleaned student dataset
students.to_csv(DATASET_DIR / "cleaned_students.csv", index=False)

print("\n===== STUDENT MARKS ANALYSIS =====")
print(students[marks_columns + ["average_marks"]].describe())

print("\n===== STUDENT INTERESTS =====")
print(students["interest"].value_counts())

# Graph 1: Student interests
students["interest"].value_counts().plot(
    kind="bar", title="Student Interests"
)
plt.xlabel("Interest")
plt.ylabel("Number of Students")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "student_interests.png")
plt.show()
plt.close()

# Graph 2: Average marks distribution
students["average_marks"].plot(
    kind="hist", bins=10, title="Distribution of Average Marks"
)
plt.xlabel("Average Marks")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_marks.png")
plt.show()
plt.close()

# Analyse course dataset
print("\n===== COURSE DATASET =====")
print("Number of courses:", len(courses))
print("\nCourse categories:")
print(courses["category"].value_counts())

print("\nMissing course values:")
print(courses.isnull().sum())

print("\nCourse details:")
print(courses[["course_id", "course_name", "category"]])

# Save course category graph
courses["category"].value_counts().plot(
    kind="bar", title="Available Course Categories"
)
plt.xlabel("Course Category")
plt.ylabel("Number of Courses")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "course_categories.png")
plt.show()
plt.close()

print("\nEDA AND PREPROCESSING COMPLETED SUCCESSFULLY!")
print("Cleaned student dataset saved.")
print("Graphs saved inside the outputs folder.")
