
import pandas as pd
import joblib
from pathlib import Path

# 1. Set project paths
BASE_DIR = Path(__file__).resolve().parent

COURSE_FILE = BASE_DIR / "dataset" / "courses.csv"
MODEL_FILE = BASE_DIR / "outputs" / "best_course_model.pkl"

# 2. Load course data and trained model
courses = pd.read_csv(COURSE_FILE)
model = joblib.load(MODEL_FILE)


# 3. Function to get student details
def get_student_details():

    print("\n===== STUDENT DETAILS =====")

    python_marks = float(input("Enter Python marks (0-100): "))
    maths_marks = float(input("Enter Mathematics marks (0-100): "))
    programming_marks = float(input("Enter Programming marks (0-100): "))

    for mark in [python_marks, maths_marks, programming_marks]:
        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    print("\nAvailable interests:")
    interests = [
        "Artificial Intelligence",
        "Data Science",
        "Web Development",
        "Cyber Security",
        "Cloud Computing"
    ]

    for i, interest in enumerate(interests, 1):
        print(i, ".", interest)

    choice = int(input("Choose your interest (1-5): "))

    if choice not in range(1, 6):
        raise ValueError("Please choose a number from 1 to 5.")

    interest = interests[choice - 1]

    career_goal = input("Enter your career goal: ")

    skills = input(
        "Enter your skills separated by semicolons: "
    )

    return {
        "python_marks": python_marks,
        "maths_marks": maths_marks,
        "programming_marks": programming_marks,
        "interest": interest,
        "career_goal": career_goal,
        "skills": skills
    }


# 4. Recommendation function
def recommend_courses(student):

    average_marks = (
        student["python_marks"]
        + student["maths_marks"]
        + student["programming_marks"]
    ) / 3

    student_skills = set(
        str(student["skills"]).lower().split(";")
    )

    records = []

    # Create one student-course record for every course
    for _, course in courses.iterrows():

        course_skills = set(
            str(course["required_skills"]).lower().split(";")
        )

        skill_overlap = len(
            student_skills.intersection(course_skills)
        )

        interest_match = int(
            student["interest"] == course["domain"]
        )

        records.append({
            "python_marks": student["python_marks"],
            "maths_marks": student["maths_marks"],
            "programming_marks": student["programming_marks"],
            "average_marks": average_marks,
            "min_average_marks": course["min_average_marks"],
            "credits": course["credits"],
            "skill_overlap": skill_overlap,
            "interest_match": interest_match,
            "interest": student["interest"],
            "career_goal": student["career_goal"],
            "course_name": course["course_name"],
            "category": course["category"],
            "domain": course["domain"]
        })

    student_courses = pd.DataFrame(records)

    # Predict recommendation probabilities
    probabilities = model.predict_proba(student_courses)

    positive_class_index = list(model.classes_).index(1)

    student_courses["recommendation_score"] = (
        probabilities[:, positive_class_index] * 100
    ).round(2)

    # Add course details
    student_courses["course_id"] = courses["course_id"].values
    student_courses["eligible"] = (
        average_marks >= courses["min_average_marks"]
    ).values

    # Only recommend courses meeting the marks requirement
    recommendations = student_courses[
        student_courses["eligible"] == True
    ].copy()

    recommendations = recommendations.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return recommendations


# 5. Run the recommendation system
if __name__ == "__main__":

    try:
        student = get_student_details()

        recommendations = recommend_courses(student)

        print("\n===== YOUR COURSE RECOMMENDATIONS =====")

        print("Average Marks:", round(
            (student["python_marks"]
             + student["maths_marks"]
             + student["programming_marks"]) / 3, 2
        ))

        if recommendations.empty:
            print("No courses meet the minimum marks requirement.")
        else:
            print(
                recommendations[
                    [
                        "course_id",
                        "course_name",
                        "category",
                        "recommendation_score"
                    ]
                ].head(5).to_string(index=False)
            )

        print("\nRecommendation process completed!")

    except ValueError as error:
        print("\nInput error:", error)

    except Exception as error:
        print("\nSomething went wrong:", error)
