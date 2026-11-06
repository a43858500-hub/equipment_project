from pathlib import Path

from models import MaintenanceRequest
from report import build_report, urgent_open, PRIORITY_RU
from storage import load_equipment

BASE = Path(__file__).parent

def main():
    equipment = {e.inventory_number: e for e in load_equipment(BASE / "parsed_equipment.json")}

    requests = [
        MaintenanceRequest(1, equipment["INV-002"], "Не включается шпиндель", "critical"),
        MaintenanceRequest(2, equipment["INV-001"], "Повышенная вибрация", "high"),
        MaintenanceRequest(3, equipment["INV-003"], "Замена ремня", "low"),
        MaintenanceRequest(4, equipment["INV-005"], "Не держит заряд АКБ", "high", status="closed"),
    ]

    print("Открытые заявки с высоким/критическим приоритетом:")
    for r in urgent_open(requests):
        print(f"  #{r.id} [{PRIORITY_RU[r.priority]}] {r.equipment.name}: {r.description}")

    report_path = BASE / "report.txt"
    report_path.write_text(build_report(requests), encoding="utf-8")
    print(f"\nОтчёт сохранён: {report_path.name}")

if __name__ == "__main__":
    main()
