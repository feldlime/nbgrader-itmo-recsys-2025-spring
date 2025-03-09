import pandas as pd
from pathlib import Path
from nbgrader.api import Gradebook

COURSE_ID = "itmo_recsys_2025_spring"
DB_URL = "sqlite:////app/gradebook.db"
EXCHANGE_DIR = "/usr/local/share/nbgrader/exchange"
STUDENTS_TSV_FILENAME = "students.tsv"


def main() -> None:
    students_tsv_path = Path(EXCHANGE_DIR) / COURSE_ID / STUDENTS_TSV_FILENAME
    students_df = pd.read_csv(students_tsv_path, sep="\t")
    print(f"Students in file: {len(students_df)}")

    students_df = students_df.loc[students_df["Github repo"].notnull()].copy()
    students_df["student_id"] = students_df["Github repo"].str.removeprefix("https://github.com/").str.split("/", expand=True)[0]
    names = students_df["ФИО"].str.split(" ", expand=True, n=1)
    students_df["last_name"] = names[0]
    students_df["first_name"] = names[1]
    print(f"Valid students in file: {len(students_df)}")
    
    gradebook = Gradebook(db_url=DB_URL, course_id=COURSE_ID)
    
    existing_students = gradebook.students
    existing_student_ids = set(student.id for student in existing_students)
    print(f"Existing students in DB: {len(existing_student_ids)}")

    students_to_add_df = students_df.loc[~students_df["student_id"].isin(existing_student_ids)]
    print(f"New students to add: {len(students_to_add_df)}")
    
    for _, student in students_to_add_df.iterrows():
        print(student, flush=True)
        gradebook.add_student(student["student_id"], first_name=student["first_name"], last_name=student["last_name"])

    print(f"New students adding finished")


if __name__ == "__main__":
    main()
