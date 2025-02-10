
from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('api/divisions/', DivisionListView.as_view(), name='get_divisions'),
    path('api/districts/<int:division_id>/', get_districts, name='get_districts'),
    path('api/upazilas/<int:district_id>/', get_upazilas, name='get_upazilas'),
    path('api/unions/<int:upazila_id>/', get_unions, name='get_unions'),
    path('api/villages/<int:union_id>/', get_villages, name='get_villages'),
    
    
    path('api/get_division_name/<int:id>/', GetDivisionNameView.as_view(), name='get_division_name'),
    path('api/get_district_name/<int:id>/', GetDistrictNameView.as_view(), name='get_district_name'),
    path('api/get_upazilla_name/<int:id>/', GetUpazillaNameView.as_view(), name='get_upazilla_name'),
    path('api/get_union_name/<int:id>/', GetUnionNameView.as_view(), name='get_union_name'),
    path('api/get_village_name/<int:id>/', GetVillageNameView.as_view(), name='get_village_name'),
    
    
    
    path('api/check_patient/', CheckPatientAPIView.as_view(), name="check_patient"),
    path("api/patient/", PatientCreateOrRetrieveAPIView.as_view(), name="patient-create-retrieve"),
    path("api/pregnancy/", PregnancyRecordCreateAPIView.as_view(), name="pregnancy-create"),
    path('api/create_patient_and_pregnancy/', CreatePatientAndPregnancy.as_view(), name='create_patient_and_pregnancy'),
    path('api/cre-checkup-report/', CheckupReportCreateView.as_view(), name="create-checkup-report"),

]

# Template urls
urlpatterns += [
    path('patient_create/', TemplateView.as_view(template_name='Html/html/custom/patient_create.html'), name='patient-create'),
    path('patient_create2/', TemplateView.as_view(template_name='Html/html/custom/patient_create2.html'), name='patient-create'),
    path('report_create/', TemplateView.as_view(template_name='Html/html/custom/checkup_reports.html'), name='checkup_report'),
    path('uhfpo-dashboard/', TemplateView.as_view(template_name='Html/html/custom/uhfpo_dashboard.html'), name='uhfpo_dashboard'),
    path('ch_and_mother/', TemplateView.as_view(template_name='Html/html/custom/childbirth_motherdeath_form.html'), name='child_and_mother'),
    path('checkup_detail/', TemplateView.as_view(template_name='Html/html/custom/checkup_details.html'), name='chekup_details'),
]
