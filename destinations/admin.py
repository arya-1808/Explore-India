from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "state",
        "city",
        "category",
        "avg_budget_per_day",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "name",
        "city",
        "state",
        "category",
    )

    list_filter = (
        "state",
        "category",
        "is_featured",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "category",
                    "state",
                    "city",
                )
            },
        ),
        (
            "Travel Information",
            {
                "fields": (
                    "best_time_to_visit",
                    "avg_budget_per_day",
                    "image",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_featured",
                )
            },
        ),
        (
            "Record",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )