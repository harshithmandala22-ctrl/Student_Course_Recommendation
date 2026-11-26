
import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

# 1. Set project paths
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Load datasets
students = pd.read_csv(DATASET_DIR / "cleaned_students.csv")
courses = pd.read_csv(DATASET_DIR / "courses.csv")

# 3. Create student-course training records
records = []

for _, student in students.iterrows():
    student_skills = set(str(student["skills"]).split(";"))

    for _, course in courses.iterrows():
        course_skills = set(str(course["required_skills"]).split(";"))

        skill_overlap = len(student_skills.intersection(course_skills))

        interest_match = int(
            student["interest"] == course["domain"]
        )

        eligible = int(
            student["average_marks"] >= course["min_average_marks"]
        )

        # Sample recommendation rule for this prototype
        recommended = int(
            eligible == 1 and
            (interest_match == 1 or skill_overlap >= 1)
        )

        records.append({
            "python_marks": student["python_marks"],
            "maths_marks": student["maths_marks"],
            "programming_marks": student["programming_marks"],
            "average_marks": student["average_marks"],
            "min_average_marks": course["min_average_marks"],
            "credits": course["credits"],
            "skill_overlap": skill_overlap,
            "interest_match": interest_match,
            "interest": student["interest"],
            "career_goal": student["career_goal"],
            "course_name": course["course_name"],
            "category": course["category"],
            "domain": course["domain"],
            "recommended": recommended
        })

data = pd.DataFrame(records)

# Save training dataset
data.to_csv(OUTPUT_DIR / "training_data.csv", index=False)

print("Training records created:", len(data))
print("\nRecommendation label counts:")
print(data["recommended"].value_counts())

# 4. Select input features and target
X = data.drop(columns=["recommended"])
y = data["recommended"]

# 5. Identify numerical and categorical columns
numeric_features = [
    "python_marks",
    "maths_marks",
    "programming_marks",
    "average_marks",
    "min_average_marks",
    "credits",
    "skill_overlap",
    "interest_match"
]

categorical_features = [
    "interest",
    "career_goal",
    "course_name",
    "category",
    "domain"
]

# 6. Preprocessing: encoding and scaling
preprocessor = ColumnTransformer(
    transformers=[
        ("numbers", StandardScaler(), numeric_features),
        ("categories", OneHotEncoder(handle_unknown="ignore"),
         categorical_features)
    ]
)

# 7. Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 8. Define six ML algorithms
models = {
    "Decision Tree": DecisionTreeClassifier(
        random_state=42, class_weight="balanced"
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    ),

    "SVM": SVC(
        probability=True,
        class_weight="balanced",
        random_state=42
    ),

    "KNN": KNeighborsClassifier(n_neighbors=5),

    "MLP": MLPClassifier(
        hidden_layer_sizes=(50, 25),
        max_iter=1000,
        random_state=42
    )
}

# 9. Train and compare models
results = []
best_model = None
best_score = -1
best_name = ""

for name, algorithm in models.items():

    pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("model", algorithm)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, zero_division=0)

    results.append({
        "Model": name,
        "Accuracy": round(accuracy, 4),
        "F1 Score": round(f1, 4)
    })

    print("\nModel:", name)
    print("Accuracy:", round(accuracy, 4))
    print("F1 Score:", round(f1, 4))

    if f1 > best_score:
        best_score = f1
        best_model = pipeline
        best_name = name

# 10. Display comparison
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(
    by="F1 Score", ascending=False
)

print("\n===== MODEL COMPARISON =====")
print(results_df.to_string(index=False))

# 11. Save the best model
joblib.dump(best_model, OUTPUT_DIR / "best_course_model.pkl")

print("\nBest model:", best_name)
print("Best F1 Score:", round(best_score, 4))
print("\nBest model saved successfully!")
print("Training completed!")
