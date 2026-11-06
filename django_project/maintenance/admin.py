from django.contrib import admin
from django.db.models import Count, Q

from .models import Equipment, MaintenanceRequest


class MaintenanceRequestInline(admin.TabularInline):
    model = MaintenanceRequest
    extra = 0
    fields = ("description", "priority", "status", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("inventory_number", "name", "status", "active_requests")
    list_filter = ("status",)
    search_fields = ("inventory_number", "name")
    ordering = ("inventory_number",)
    inlines = [MaintenanceRequestInline]

    def get_queryset(self, request):
        active = Q(requests__status__in=MaintenanceRequest.ACTIVE_STATUSES)
        return super().get_queryset(request).annotate(active_count=Count("requests", filter=active))

    @admin.display(description="Активные заявки", ordering="active_count")
    def active_requests(self, obj):
        return obj.active_count


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "equipment", "priority", "status", "short_description", "created_at")
    list_filter = ("priority", "status", "created_at")
    search_fields = ("description", "equipment__inventory_number", "equipment__name")
    list_select_related = ("equipment",)
    autocomplete_fields = ("equipment",)
    date_hierarchy = "created_at"
    actions = ["close_requests"]

    @admin.display(description="Описание")
    def short_description(self, obj):
        return obj.description[:60]

    @admin.action(description="Закрыть выбранные заявки")
    def close_requests(self, request, queryset):
        updated = queryset.update(status=MaintenanceRequest.Status.CLOSED)
        self.message_user(request, f"Закрыто заявок: {updated}")
