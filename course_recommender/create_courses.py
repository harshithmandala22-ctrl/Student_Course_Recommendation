
import pandas as pd

courses = [
    {
        "course_id": "C01",
        "course_name": "Artificial Intelligence",
        "category": "Major",
        "domain": "Artificial Intelligence",
        "required_skills": "Python;Mathematics",
        "prerequisites": "Programming",
        "min_average_marks": 60,
        "credits": 4
    },
    {
        "course_id": "C02",
        "course_name": "Machine Learning",
        "category": "Minor",
        "domain": "Artificial Intelligence",
        "required_skills": "Python;Mathematics;Statistics",
        "prerequisites": "Python",
        "min_average_marks": 65,
        "credits": 4
    },
    {
        "course_id": "C03",
        "course_name": "Data Science",
        "category": "Minor",
        "domain": "Data Science",
        "required_skills": "Python;Statistics;Data Analysis",
        "prerequisites": "Mathematics",
        "min_average_marks": 60,
        "credits": 4
    },
    {
        "course_id": "C04",
        "course_name": "Web Development",
        "category": "Core Elective",
        "domain": "Web Development",
        "required_skills": "HTML;CSS;JavaScript",
        "prerequisites": "Basic Programming",
        "min_average_marks": 50,
        "credits": 3
    },
    {
        "course_id": "C05",
        "course_name": "Cyber Security",
        "category": "Major",
        "domain": "Cyber Security",
        "required_skills": "Networking;Linux;Security",
        "prerequisites": "Computer Networks",
        "min_average_marks": 60,
        "credits": 4
    },
    {
        "course_id": "C06",
        "course_name": "Cloud Computing",
        "category": "Core Elective",
        "domain": "Cloud Computing",
        "required_skills": "Python;Cloud;Networking",
        "prerequisites": "Computer Networks",
        "min_average_marks": 55,
        "credits": 3
    },
    {
        "course_id": "C07",
        "course_name": "Deep Learning",
        "category": "Minor",
        "domain": "Artificial Intelligence",
        "required_skills": "Python;Mathematics",
        "prerequisites": "Machine Learning",
        "min_average_marks": 70,
        "credits": 4
    },
    {
        "course_id": "C08",
        "course_name": "Database Management Systems",
        "category": "Core Elective",
        "domain": "Database",
        "required_skills": "SQL;Database",
        "prerequisites": "Basic Programming",
        "min_average_marks": 50,
        "credits": 3
    },
    {
        "course_id": "C09",
        "course_name": "Natural Language Processing",
        "category": "Minor",
        "domain": "Artificial Intelligence",
        "required_skills": "Python;Statistics",
        "prerequisites": "Machine Learning",
        "min_average_marks": 70,
        "credits": 4
    },
    {
        "course_id": "C10",
        "course_name": "Computer Networks",
        "category": "Core Elective",
        "domain": "Networking",
        "required_skills": "Networking;Linux",
        "prerequisites": "Basic Computer Knowledge",
        "min_average_marks": 50,
        "credits": 3
    }
]

df = pd.DataFrame(courses)

df.to_csv("dataset/courses.csv", index=False)

print("Course dataset created successfully!")
print(df[["course_id", "course_name", "category"]])
print("\nTotal courses:", len(df))
