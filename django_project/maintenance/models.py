from django.db import models


class Equipment(models.Model):
    class Status(models.TextChoices):
        IN_WORK = "in_work", "В работе"
        REPAIR = "repair", "На ремонте"
        RESERVE = "reserve", "Резерв"
        WRITTEN_OFF = "written_off", "Списано"

    inventory_number = models.CharField("Инвентарный номер", max_length=32, unique=True)
    name = models.CharField("Название", max_length=200)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.IN_WORK)

    class Meta:
        verbose_name = "оборудование"
        verbose_name_plural = "оборудование"
        ordering = ["inventory_number"]

    def __str__(self):
        return f"{self.inventory_number} — {self.name}"


class MaintenanceRequest(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"
        CRITICAL = "critical", "Критический"

    class Status(models.TextChoices):
        OPEN = "open", "Открыта"
        IN_PROGRESS = "in_progress", "В работе"
        CLOSED = "closed", "Закрыта"

    ACTIVE_STATUSES = (Status.OPEN, Status.IN_PROGRESS)

    equipment = models.ForeignKey(
        Equipment,
        verbose_name="Оборудование",
        on_delete=models.PROTECT,
        related_name="requests",
    )
    description = models.TextField("Описание")
    priority = models.CharField("Приоритет", max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField("Статус", max_length=15, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "заявку"
        verbose_name_plural = "заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка #{self.pk}: {self.equipment.inventory_number}"

    @property
    def is_open(self):
        return self.status != self.Status.CLOSED
