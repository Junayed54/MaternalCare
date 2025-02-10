from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("phone_number", "full_name", "role", "is_active", "is_staff", "created_at")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("phone_number", "full_name", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")  # Fix: Make timestamps read-only

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("full_name", "hospital", "id_card_number", "father_name", "husband_name", "mother_name", "date_of_birth", "email", "address")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("created_at", "updated_at")}),  # Fix: Kept inside fieldsets but marked read-only
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "full_name", "password1", "password2", "role", "is_active", "is_staff", "is_superuser"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
