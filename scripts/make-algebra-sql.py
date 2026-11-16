import csv
from pathlib import Path

root = Path(__file__).resolve().parent.parent


def esc(value):
    return (value or "").replace("'", "''")


def convert(csv_name, sql_name, title):
    rows = list(csv.DictReader((root / "data" / csv_name).open(encoding="utf-8")))
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
            f"-- {title}",
            "INSERT INTO arithmetic_tasks (subject, class_name, level, question, answer, image, explanation_of_the_answer)",
            "VALUES",
            ",\n".join(values) + ";",
            "",
        ]
    )
    # User may want a separate algebra_tasks table later; same columns as arithmetic_tasks
    out = root / "data" / sql_name
    out.write_text(sql, encoding="utf-8")
    print(len(rows), out)


convert("algebra-7-basic.csv", "insert-algebra-7-basic.sql", "Алгебра, 7 класс, Базовый, 70 задач.")
convert("algebra-7-medium.csv", "insert-algebra-7-medium.sql", "Алгебра, 7 класс, Средний, 80 задач.")
convert("algebra-7-high.csv", "insert-algebra-7-high.sql", "Алгебра, 7 класс, Высокий, 100 задач.")
