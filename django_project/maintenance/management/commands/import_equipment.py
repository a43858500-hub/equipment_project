import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from maintenance.models import Equipment, MaintenanceRequest

DEMO_REQUESTS = [
    ("INV-002", "Не включается шпиндель", "critical", "open"),
    ("INV-001", "Повышенная вибрация", "high", "in_progress"),
    ("INV-003", "Замена ремня", "low", "open"),
    ("INV-005", "Не держит заряд АКБ", "high", "closed"),
]


class Command(BaseCommand):
    help = "Загружает оборудование из parsed_equipment.json"

    def add_arguments(self, parser):
        parser.add_argument("--path", default=str(Path(settings.BASE_DIR) / "parsed_equipment.json"))
        parser.add_argument("--demo", action="store_true")

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Файл не найден: {path}")

        status_by_label = {label: value for value, label in Equipment.Status.choices}
        items = json.loads(path.read_text(encoding="utf-8"))

        for item in items:
            status = status_by_label.get(item["status"])
            if status is None:
                raise CommandError(f"Неизвестный статус: {item['status']}")
            Equipment.objects.update_or_create(
                inventory_number=item["inventory_number"],
                defaults={"name": item["name"], "status": status},
            )
        self.stdout.write(self.style.SUCCESS(f"Оборудования загружено: {len(items)}"))

        if options["demo"] and not MaintenanceRequest.objects.exists():
            for inventory_number, description, priority, status in DEMO_REQUESTS:
                MaintenanceRequest.objects.create(
                    equipment=Equipment.objects.get(inventory_number=inventory_number),
                    description=description,
                    priority=priority,
                    status=status,
                )
            self.stdout.write(self.style.SUCCESS(f"Заявок создано: {len(DEMO_REQUESTS)}"))
