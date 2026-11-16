import csv
from pathlib import Path

root = Path(__file__).resolve().parent.parent
csv_path = root / "data" / "arithmetic-tasks-medium-5-6.csv"
sql_path = root / "data" / "insert-arithmetic-medium-5-6.sql"
rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))


def esc(value):
    return (value or "").replace("'", "''")


values = []
for row in rows:
    values.append(
        "  ('{subject}', '{class_name}', '{level}', '{question}', '{answer}', '{image}', '{explanation}')".format(
            subject=esc(row["subject"]),
            class_name=esc(row["class_name"]),
            level=esc(row["level"]),
            question=esc(row["question"]),
            answer=esc(row["answer"]),
            image=esc(row["image"]),
            explanation=esc(row["explanation_of_the_answer"]),
        )
    )

sql = "\n".join(
    [
        "-- 50 задач арифметики, 5-6 класс, Средний.",
        "-- Вставьте в SQL Editor в Supabase. Базовые строки не удаляет.",
        "INSERT INTO arithmetic_tasks (subject, class_name, level, question, answer, image, explanation_of_the_answer)",
        "VALUES",
        ",\n".join(values) + ";",
        "",
    ]
)
sql_path.write_text(sql, encoding="utf-8")
print(len(rows), sql_path)
