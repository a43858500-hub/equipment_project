from collections import Counter

from models import MaintenanceRequest

PRIORITY_RU = {"low": "низкий", "medium": "средний", "high": "высокий", "critical": "критический"}
STATUS_RU = {"open": "открыта", "in_progress": "в работе", "closed": "закрыта"}

def urgent_open(requests: list[MaintenanceRequest]) -> list[MaintenanceRequest]:
    return [r for r in requests if r.is_open and r.priority in ("high", "critical")]

def build_report(requests: list[MaintenanceRequest]) -> str:
    lines = ["ОТЧЁТ ПО ЗАЯВКАМ НА ОБСЛУЖИВАНИЕ", "-" * 40,
             f"Всего заявок: {len(requests)}", "", "По статусам:"]
    for st, n in Counter(r.status for r in requests).items():
        lines.append(f"  {STATUS_RU[st]}: {n}")

    lines += ["", "Открытые заявки с высоким/критическим приоритетом:"]
    urgent = urgent_open(requests)
    if not urgent:
        lines.append("  нет")
    for r in urgent:
        lines.append(f"  #{r.id} [{PRIORITY_RU[r.priority]}] {r.equipment.inventory_number} "
                     f"{r.equipment.name} — {r.description}")
    return "\n".join(lines) + "\n"
