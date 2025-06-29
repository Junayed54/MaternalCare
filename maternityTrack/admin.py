from django.contrib import admin
from .models import *


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('division',)

@admin.register(Upazilla)
class UpazillaAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('district',)

@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    list_display = ('name', 'upazilla', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('upazilla',)

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'union', 'word_no', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('union', 'word_no')

@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'union', 'post_code', 'created_at', 'updated_at')
    search_fields = ('name', 'post_code')
    list_filter = ('union',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'village', 'blood_group', 'created_by')
    search_fields = ('full_name', 'phone_number', 'nid_number', 'couple_no')
    list_filter = ('blood_group', 'district', 'upazilla', 'union')

@admin.register(PregnancyRecord)
class PregnancyRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'pregnancy_count', 'last_period_date', 'expected_delivery_date', 'preferred_delivery_place')
    list_filter = ('preferred_delivery_place', 'created_at')
    search_fields = ('patient__full_name', 'pregnancy_count')
    readonly_fields = ('created_at', 'updated_at')

# @admin.register(AncSchedule)
# class AncScheduleAdmin(admin.ModelAdmin):
#     list_display = ('pregnancy_record', 'anc_date', 'status')
#     list_filter = ('status', 'anc_date')
#     search_fields = ('pregnancy_record__patient__full_name',)
#     readonly_fields = ('created_at', 'updated_at')

@admin.register(AncSchedule)
class AncScheduleAdmin(admin.ModelAdmin):
    list_display = ('pregnancy_record', 'anc_date', 'status', 'get_anc_number')
    list_filter = ('status', 'anc_date')
    search_fields = ('pregnancy_record__patient__full_name',)
    readonly_fields = ('created_at', 'updated_at')

    def get_anc_number(self, obj):
        # Try to get related CheckupReport's anc_checkup_number if exists
        checkup_report = getattr(obj, 'checkupreport', None)
        if checkup_report:
            return dict(checkup_report.ANC_CHOICES).get(checkup_report.anc_checkup_number, 'Unknown')
        return 'Not checked'

    get_anc_number.short_description = 'ANC Number'

@admin.register(CheckupReport)
class CheckupReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'checked_by', 'bp', 'rbs', 'created_at')
    search_fields = ('patient__full_name', 'checked_by__username')
    list_filter = ('diabetes', 'heart_disease', 'thyroid_disease', 'kidney_disease')

@admin.register(DeliveryRecord)
class DeliveryRecordAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'created_by', 'delivery_date',
        'mother_status', 'baby_name', 'baby_gender', 'baby_status',
        'delivery_type', 'actual_delivery_place'
    )
    
    list_filter = (
        'mother_status', 'baby_status', 'baby_gender',
        'delivery_type', 'actual_delivery_place', 'delivery_date'
    )
    
    search_fields = (
        'patient__name', 'baby_name', 'created_by__username',
    )
    
    readonly_fields = ('created_by',)

    def save_model(self, request, obj, form, change):
        """ Automatically set the created_by field to the current user """
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
