from rest_framework import serializers
from .models import (
    Division, District, Upazilla, Union, Village, PostOffice, Patient, PregnancyRecord,
    AncSchedule, CheckupReport
)
from django.db import models

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class UpazilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upazilla
        fields = '__all__'


class UnionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Union
        fields = '__all__'


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'


class PostOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = '__all__'

class AncScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AncSchedule
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    anc_schedules = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'full_name', 'phone_number', 'husband_name', 'husband_phone',
            'couple_no', 'nid_number', 'village', 'union',
            'upazilla', 'district', 'division', 'blood_group',
            'husband_blood_group', 'husband_earning', 'image',
            'anc_schedules'  # Include ANC schedule field
        ]

    # def get_anc_schedules(self, obj):
    #     # Fetch the latest pregnancy record for this patient
    #     pregnancy_record = PregnancyRecord.objects.filter(patient=obj).order_by('-created_at').first()
    #     print(pregnancy_recor)
    #     if pregnancy_record:
    #         # anc_schedules = AncSchedule.objects.filter(pregnancy_record=pregnancy_record).order_by('-created_at')[:4]
    #         anc_schedules = AncSchedule.objects.all()
    #         print(anc_schedules)
    #         return AncScheduleSerializer(anc_schedules, many=True).data
    #     return []
    
    
    def get_anc_schedules(self, obj):
        # Fetch all pregnancy records and pick the latest one that has ANC schedules
        pregnancy_record = (
            PregnancyRecord.objects.filter(patient=obj)
            .order_by('-created_at')
            .annotate(anc_count=models.Count('ancschedule'))
            .filter(anc_count__gt=0)  # Ensure it has ANC schedules
            .first()
        )
        

        if pregnancy_record:
            # Fetch the latest 4 ANC schedules for the selected pregnancy record
            anc_schedules = (
                AncSchedule.objects.filter(pregnancy_record=pregnancy_record)
                .order_by('-created_at')[:4]
            )
            
            return AncScheduleSerializer(anc_schedules, many=True).data
        
        return []


    


    def validate_phone_number(self, value):
        if Patient.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value
    
    def validate_phone_number(self, value):
        # Check if the patient with this phone number already exists
        if Patient.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value



class PregnancyRecordSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)
    class Meta:
        model = PregnancyRecord
        fields = '__all__'


class PatientWithPregnancySerializer(serializers.ModelSerializer):
    pregnancies = PregnancyRecordSerializer(many=True, required=False)

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        pregnancies_data = validated_data.pop('pregnancies', [])
        patient = Patient.objects.create(**validated_data)
        
        for pregnancy_data in pregnancies_data:
            PregnancyRecord.objects.create(patient=patient, **pregnancy_data)

        return patient


class AncScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AncSchedule
        fields = '__all__'


class CheckupReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)  # Include full patient details in response
    patient_phone = serializers.CharField(write_only=True)  # Accept phone number for lookup
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)  # Derived from hospital
    checked_by_name = serializers.CharField(source='checked_by.full_name', read_only=True)  # Derived from checked_by (User)
    anc_checkup_number_display = serializers.CharField(source='get_anc_checkup_number_display', read_only=True)
    class Meta:
        model = CheckupReport
        fields = '__all__'
        extra_kwargs = {'patient': {'read_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('patient_phone')  # Get phone number
        try:
            patient = Patient.objects.get(phone_number=phone_number)  # Lookup patient
        except Patient.DoesNotExist:
            raise serializers.ValidationError({"patient": "Patient not found with this phone number."})

        validated_data['patient'] = patient  # Assign patient

        # Save checkup report
        checkup_report = super().create(validated_data)

        # Update ANC status if ANC is linked
        anc = validated_data.get("anc")
        if anc:
            anc.status = "Completed"  # Update ANC status (change to your desired status)
            anc.save()

        return checkup_report




