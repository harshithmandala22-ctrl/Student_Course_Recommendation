
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Course Recommendation System",
    page_icon="🎓",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

# Load course dataset and trained model
@st.cache_resource
def load_model():
    model_path = BASE_DIR / "outputs" / "best_course_model.pkl"
    return joblib.load(model_path)

@st.cache_data
def load_courses():
    courses_path = BASE_DIR / "dataset" / "courses.csv"
    return pd.read_csv(courses_path)

model = load_model()
courses = load_courses()

st.title("🎓 Student Course Recommendation System")

st.write(
    "Find suitable Major, Minor and Core Elective courses "
    "based on your marks, interests and skills."
)

st.divider()

st.header("Enter Your Details")

with st.form("student_form"):

    col1, col2 = st.columns(2)

    with col1:
        python_marks = st.number_input(
            "Python Marks",
            min_value=0,
            max_value=100,
            value=70
        )

        maths_marks = st.number_input(
            "Mathematics Marks",
            min_value=0,
            max_value=100,
            value=70
        )

    with col2:
        programming_marks = st.number_input(
            "Programming Marks",
            min_value=0,
            max_value=100,
            value=70
        )

        interest = st.selectbox(
            "Your Interest",
            [
                "Artificial Intelligence",
                "Data Science",
                "Web Development",
                "Cyber Security",
                "Cloud Computing"
            ]
        )

    career_goal = st.text_input(
        "Your Career Goal",
        placeholder="Example: Data Scientist"
    )

    skills = st.text_input(
        "Your Skills (separate using semicolons)",
        placeholder="Example: Python; Mathematics; Statistics"
    )

    submitted = st.form_submit_button(
        "Recommend Courses",
        type="primary"
    )

if submitted:

    average_marks = (
        python_marks + maths_marks + programming_marks
    ) / 3

    student_skills = set(
        skill.strip()
        for skill in skills.split(";")
        if skill.strip()
    )

    st.subheader("Your Academic Summary")

    col1, col2 = st.columns(2)

    col1.metric("Average Marks", f"{average_marks:.2f}%")
    col2.write(f"**Interest:** {interest}")

    # Create one prediction row for each course
    input_rows = []

    for _, course in courses.iterrows():

        course_skills = set(
    skill.strip()
    for skill in str(course["required_skills"]).split(";")
    if skill.strip()
)
        

        skill_overlap = len(
            student_skills.intersection(course_skills)
        )

        interest_match = int(
            interest == course["domain"]
        )

        input_rows.append({
            "python_marks": python_marks,
            "maths_marks": maths_marks,
            "programming_marks": programming_marks,
            "average_marks": average_marks,
            "min_average_marks": course["min_average_marks"],
            "credits": course["credits"],
            "skill_overlap": skill_overlap,
            "interest_match": interest_match,
            "interest": interest,
            "career_goal": career_goal,
            "course_name": course["course_name"],
            "category": course["category"],
            "domain": course["domain"]
        })

    input_data = pd.DataFrame(input_rows)

    # Get recommendation scores from trained model
    probabilities = model.predict_proba(input_data)

    positive_class_index = list(model.classes_).index(1)

    courses["recommendation_score"] = (
        probabilities[:, positive_class_index] * 100
    )

    courses["eligible"] = (
        average_marks >= courses["min_average_marks"]
    )

    recommendations = courses[
        courses["eligible"] == True
    ].sort_values(
        by="recommendation_score",
        ascending=False
    ).head(5)

    st.divider()
    st.header("🌟 Your Recommended Courses")

    if not recommendations.empty:

        st.success(
            f"We found {len(recommendations)} suitable courses for you!"
        )

        for rank, (_, course) in enumerate(
            recommendations.iterrows(), start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"{rank}. {course['course_name']}"
                )

                col1, col2, col3 = st.columns(3)

                col1.write(
                    f"**Category:** {course['category']}"
                )

                col2.write(
                    f"**Credits:** {course['credits']}"
                )

                col3.write(
                    f"**Recommendation score:** "
                    f"{course['recommendation_score']:.2f}%"
                )

                st.write(
                    f"**Domain:** {course['domain']}"
                )

                st.write(
                    f"**Required skills:** {course['required_skills']}"
                )

    else:

        st.warning(
            "No courses meet the minimum marks requirement. "
            "Try improving your marks or checking the course requirements."
        )

    st.caption(
        "Note: This is an academic demonstration using synthetic training "
        "data. Recommendation scores are model scores, not guaranteed "
        "success probabilities."
    )
