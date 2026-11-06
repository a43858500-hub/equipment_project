from dataclasses import dataclass, field
from datetime import date

PRIORITIES = ("low", "medium", "high", "critical")
STATUSES = ("open", "in_progress", "closed")

@dataclass
class Equipment:
    inventory_number: str
    name: str
    status: str

@dataclass
class MaintenanceRequest:
    id: int
    equipment: Equipment
    description: str
    priority: str = "medium"
    status: str = "open"
    created_at: date = field(default_factory=date.today)

    def __post_init__(self):
        if self.priority not in PRIORITIES:
            raise ValueError(f"Недопустимый приоритет: {self.priority}")
        if self.status not in STATUSES:
            raise ValueError(f"Недопустимый статус: {self.status}")

    @property
    def is_open(self) -> bool:
        return self.status != "closed"
