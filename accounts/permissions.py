from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Permission class to allow only Admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsUHFPO(BasePermission):
    """Permission class to allow only Upazila Health & Family Planning Officer (UHFPO)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "UHFPO"


class IsFieldAssistant(BasePermission):
    """Permission class to allow only Field Assistant users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "FS"


class IsMidwife(BasePermission):
    """Permission class to allow only Midwife users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "MIDWIFE"
