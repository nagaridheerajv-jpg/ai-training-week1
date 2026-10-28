import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_employees(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"name", "salary"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        employees = [row for row in reader if row["name"] and row["salary"]]
        if not employees:
            raise ValueError("The CSV does not contain any employee rows")
        return employees


def create_chart(csv_path: Path, output_path: Path, limit: int) -> None:
    employees = read_employees(csv_path)
    employees.sort(key=lambda row: int(row["salary"]), reverse=True)
    employees = employees[:limit]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(
        [row["name"] for row in employees],
        [int(row["salary"]) for row in employees],
        color="#4C78A8",
    )
    ax.invert_yaxis()
    ax.set_title("Employee salaries")
    ax.set_xlabel("Salary")
    ax.set_ylabel("Employee")
    ax.set_xlim(left=0)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a bar chart of employee salaries")
    parser.add_argument("csv", nargs="?", type=Path, default=Path("employees.csv"))
    parser.add_argument("-o", "--output", type=Path, default=Path("employee-salaries.png"))
    parser.add_argument("-n", "--limit", type=int, default=10)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be greater than zero")
    return args


if __name__ == "__main__":
    arguments = parse_args()
    create_chart(arguments.csv, arguments.output, arguments.limit)
