import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).parent

def main():
    con = sqlite3.connect(":memory:")
    con.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))

    for e in json.loads((BASE / "parsed_equipment.json").read_text(encoding="utf-8")):
        con.execute("INSERT INTO equipment(inventory_number, name, status) VALUES (?,?,?)",
                    (e["inventory_number"], e["name"], e["status"]))

    con.executemany(
        "INSERT INTO maintenance_request(equipment_id, description, priority, status) VALUES (?,?,?,?)",
        [(2, "Не включается шпиндель", "critical", "open"),
         (2, "Течь СОЖ", "medium", "closed"),
         (1, "Повышенная вибрация", "high", "in_progress"),
         (3, "Замена ремня", "low", "open"),
         (5, "Не держит заряд АКБ", "high", "closed")])

    for sql, args in [("INSERT INTO equipment(inventory_number,name,status) VALUES (?,?,?)", ("INV-001", "Дубль", "x")),
                      ("INSERT INTO maintenance_request(equipment_id,description) VALUES (?,?)", (999, "нет такого"))]:
        try:
            con.execute(sql, args)
        except sqlite3.IntegrityError as err:
            print("Ограничение сработало:", err)

    titles = [
        "1. Заявки по приоритету",
        "2. Количество заявок по статусам",
        "3. Оборудование без активных заявок",
        "4. Самые проблемные единицы оборудования",
    ]
    blocks = [b.strip() for b in (BASE / "queries.sql").read_text(encoding="utf-8").split(";") if b.strip()]
    for title, block in zip(titles, blocks):
        print(f"\n{title}")
        for row in con.execute(block):
            print("  ", row)

if __name__ == "__main__":
    main()
