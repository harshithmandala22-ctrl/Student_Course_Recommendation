
import pandas as pd

# Read student dataset
students = pd.read_csv("dataset/students.csv")

# Read course dataset
courses = pd.read_csv("dataset/courses.csv")

print("========== STUDENT DATA ==========")
print(students.head())

print("\n========== COURSE DATA ==========")
print(courses.head())

print("\nStudent dataset shape:", students.shape)
print("Course dataset shape:", courses.shape)

print("\nMissing values in students:")
print(students.isnull().sum())

print("\nMissing values in courses:")
print(courses.isnull().sum())

print("\nDataset verification completed!")
