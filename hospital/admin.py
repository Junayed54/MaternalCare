from django.contrib import admin
from .models import Hospital, BloodBank, AmbulanceService

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'upazila', 'total_beds', 'available_beds', 'total_doctors', 'total_nurses', 'emergency_services')
    list_filter = ('upazila', 'emergency_services')
    search_fields = ('name', 'upazila__name')
    readonly_fields = ('created_at',)

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('health_complex', 'blood_group', 'total_units', 'last_updated')
    list_filter = ('blood_group',)
    search_fields = ('health_complex__name',)
    readonly_fields = ('last_updated',)

@admin.register(AmbulanceService)
class AmbulanceServiceAdmin(admin.ModelAdmin):
    list_display = ('ambulance_number', 'health_complex', 'driver_name', 'driver_phone', 'available')
    list_filter = ('available',)
    search_fields = ('ambulance_number', 'driver_name', 'driver_phone')
