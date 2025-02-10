from django.contrib import admin
from .models import (
    Division, District, Upazilla, Union, Village, PostOffice,
    Patient, PregnancyRecord, AncSchedule, CheckupReport
)

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
    list_display = ('full_name', 'phone_number', 'village', 'blood_group')
    search_fields = ('full_name', 'phone_number', 'nid_number', 'couple_no')
    list_filter = ('blood_group', 'district', 'upazilla', 'union')

@admin.register(PregnancyRecord)
class PregnancyRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'pregnancy_count', 'last_period_date', 'expected_delivery_date', 'preferred_delivery_place')
    list_filter = ('preferred_delivery_place', 'created_at')
    search_fields = ('patient__full_name', 'pregnancy_count')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AncSchedule)
class AncScheduleAdmin(admin.ModelAdmin):
    list_display = ('pregnancy_record', 'anc_date', 'status')
    list_filter = ('status', 'anc_date')
    search_fields = ('pregnancy_record__patient__full_name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CheckupReport)
class CheckupReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'checked_by', 'bp', 'rbs', 'created_at')
    search_fields = ('patient__full_name', 'checked_by__username')
    list_filter = ('diabetes', 'heart_disease', 'thyroid_disease', 'kidney_disease')

