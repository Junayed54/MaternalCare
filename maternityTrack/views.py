from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from django.db.models.functions import TruncMonth
from datetime import date, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
import calendar
from django.db.models import Count, Q
from accounts.permissions import * 
from django.utils.timezone import now
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db import transaction



class DivisionListView(generics.ListAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

@api_view(['GET'])
def get_districts(request, division_id):
    districts = District.objects.filter(division_id=division_id)
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_upazilas(request, district_id):
    upazilas = Upazilla.objects.filter(district_id=district_id)
    serializer = UpazilaSerializer(upazilas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_unions(request, upazila_id):
    unions = Union.objects.filter(upazilla_id=upazila_id)
    serializer = UnionSerializer(unions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_villages(request, union_id):
    villages = Village.objects.filter(union_id=union_id)
    serializer = VillageSerializer(villages, many=True)
    return Response(serializer.data)



class GetDivisionNameView(APIView):
    permission_classes = [IsFieldAssistant | IsMidwife]

    def get(self, request, id):
        try:
            division = Division.objects.get(id=id)
            return Response({'id': id, 'name': division.name})
        except District.DoesNotExist:
            return Response({'error': 'District not found'}, status=404)


class GetDistrictNameView(APIView):
    permission_classes = [IsFieldAssistant | IsMidwife]

    def get(self, request, id):
        try:
            district = District.objects.get(id=id)
            return Response({'id': id, 'name': district.name})
        except District.DoesNotExist:
            return Response({'error': 'District not found'}, status=404)

class GetUpazillaNameView(APIView):
    permission_classes = [IsFieldAssistant | IsMidwife]

    def get(self, request, id):
        try:
            upazilla = Upazilla.objects.get(id=id)
            return Response({'id': id, 'name': upazilla.name})
        except Upazilla.DoesNotExist:
            return Response({'error': 'Upazilla not found'}, status=404)

class GetUnionNameView(APIView):
    permission_classes = [IsFieldAssistant | IsMidwife]

    def get(self, request, id):
        try:
            union = Union.objects.get(id=id)
            return Response({'id': id, 'name': union.name})
        except Union.DoesNotExist:
            return Response({'error': 'Union not found'}, status=404)

class GetVillageNameView(APIView):
    permission_classes = [IsFieldAssistant | IsMidwife]

    def get(self, request, id):
        try:
            village = Village.objects.get(id=id)
            return Response({'id': id, 'name': village.name})
        except Village.DoesNotExist:
            return Response({'error': 'Village not found'}, status=404)
        
        
        
        
        
        
        


class CheckPatientAPIView(APIView):
    permission_classes = [IsFieldAssistant | IsMidwife]
    def post(self, request):
        phone_number = request.data.get('phone_number', None)
        
        if phone_number:
            try:
                patient = Patient.objects.get(phone_number=phone_number)
                # Serializing the patient object to return it as JSON response
                serializer = PatientSerializer(patient)
                return Response({'exists': True, 'patient': serializer.data})
            except Patient.DoesNotExist:
                return Response({'exists': False})
        
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class PatientCreateOrRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsFieldAssistant | IsMidwife]
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        patient, created = Patient.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "full_name": request.data.get("full_name"),
                "husband_name": request.data.get("husband_name"),
                "husband_phone": request.data.get("husband_phone"),
                # "couple_no": request.data.get("couple_no"),
                "nid_number": request.data.get("nid_number"),
                "village_id": request.data.get("village"),
                "ward_number": request.data.get("ward_number"),
                "union_id": request.data.get("union"),
                "upazilla_id": request.data.get("upazilla"),
                "district_id": request.data.get("district"),
                "age": request.data.get("age"),
                "husband_age": request.data.get("husband_age"),
                "blood_group": request.data.get("blood_group"),
                "husband_blood_group": request.data.get("husband_blood_group"),
                "husband_earning": request.data.get("husband_earning"),
                # "created_by": request.user,
            }
        )

        serializer = PatientSerializer(patient)
        if created:
            return Response({"message": "New patient created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Return the patient's details, including the full name for existing patients
            return Response({"message": "Existing patient retrieved.", "data": serializer.data}, status=status.HTTP_200_OK)

        
class PregnancyRecordCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsFieldAssistant | IsMidwife]
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.filter(phone_number=phone_number).first()
        if not patient:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new pregnancy record linked to the patient
        serializer = PregnancyRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(
                {"message": "New pregnancy record created.", "data": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None 


def to_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


# class CreatePatientAndPregnancy(APIView):
#     permission_classes = [IsAuthenticated, IsFieldAssistant | IsMidwife]

#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone_number')
#         if not phone_number:
#             return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

#         mutable_data = request.data.copy()
#         family_planning_value = mutable_data.get("family_planning_after_delivery")
#         mutable_data["family_planning_after_delivery"] = family_planning_value in ["1", 1, "true", "True"]

#         patient = Patient.objects.filter(phone_number=phone_number).first()
#         village = union = upazilla = district = division = None

#         if not patient:
#             try:
#                 village = Village.objects.get(id=mutable_data.get("village"))
#                 union = Union.objects.get(id=mutable_data.get("union"))
#                 upazilla = Upazilla.objects.get(id=mutable_data.get("upazila"))
#                 district = District.objects.get(id=mutable_data.get("district"))
#                 division = Division.objects.get(id=mutable_data.get("division"))
#             except (Village.DoesNotExist, Union.DoesNotExist, Upazilla.DoesNotExist, District.DoesNotExist, Division.DoesNotExist):
#                 return Response({"error": "Invalid location data provided."}, status=status.HTTP_400_BAD_REQUEST)

#             patient = Patient.objects.create(
#                 full_name=mutable_data.get("full_name"),
#                 phone_number=phone_number,
#                 date_of_birth=to_date(mutable_data.get("date_of_birth")),

#                 husband_name=mutable_data.get("husband_name"),
#                 husband_phone=mutable_data.get("husband_phone"),
#                 couple_no=mutable_data.get("couple_no"),
#                 nid_number=mutable_data.get("nid_number"),
#                 village=village,
#                 union=union,
#                 upazilla=upazilla,
#                 district=district,
#                 division=division,
#                 blood_group=mutable_data.get("blood_group"),
#                 husband_blood_group=mutable_data.get("husband_blood_group"),
#                 husband_earning=mutable_data.get("husband_earning"),
#                 created_by=request.user
#             )
#             patient_message = "Patient created successfully."
#         else:
#             try:
#                 if mutable_data.get("village"):
#                     village = Village.objects.get(id=mutable_data.get("village"))
#                 if mutable_data.get("union"):
#                     union = Union.objects.get(id=mutable_data.get("union"))
#                 if mutable_data.get("upazila"):
#                     upazilla = Upazilla.objects.get(id=mutable_data.get("upazila"))
#                 if mutable_data.get("district"):
#                     district = District.objects.get(id=mutable_data.get("district"))
#                 if mutable_data.get("division"):
#                     division = Division.objects.get(id=mutable_data.get("division"))
#             except (Village.DoesNotExist, Union.DoesNotExist, Upazilla.DoesNotExist, District.DoesNotExist, Division.DoesNotExist):
#                 return Response({"error": "Invalid location data provided."}, status=status.HTTP_400_BAD_REQUEST)

#             patient.full_name = mutable_data.get("full_name", patient.full_name)
#             patient.husband_name = mutable_data.get("husband_name", patient.husband_name)
#             patient.husband_phone = mutable_data.get("husband_phone", patient.husband_phone)
#             patient.couple_no = mutable_data.get("couple_no", patient.couple_no)
#             patient.nid_number = mutable_data.get("nid_number", patient.nid_number)
#             patient.blood_group = mutable_data.get("blood_group", patient.blood_group)
#             patient.husband_blood_group = mutable_data.get("husband_blood_group", patient.husband_blood_group)
#             patient.husband_earning = mutable_data.get("husband_earning", patient.husband_earning)

#             if village: patient.village = village
#             if union: patient.union = union
#             if upazilla: patient.upazilla = upazilla
#             if district: patient.district = district
#             if division: patient.division = division

#             patient.save()
#             patient_message = "Patient updated successfully."

#         # 🔁 Convert all integer fields before validation
#         int_fields = [
#             "age", "husband_age", "menstruation_off_duration", "womb_count",
#             "living_children", "normal_delivery_count", "c_section_count",
#             "d_and_c_count", "tt_dose_count"
#         ]
#         for field in int_fields:
#             mutable_data[field] = to_int(mutable_data.get(field))

#         # 🔁 Convert date fields
#         mutable_data["last_period_date"] = to_date(mutable_data.get("last_period_date"))
#         mutable_data["expected_delivery_date"] = to_date(mutable_data.get("expected_delivery_date"))

#         # 👇 Remove phone number from pregnancy data
#         mutable_data.pop("phone_number", None)
#         mutable_data["patient"] = patient.id

#         # 🧬 Serialize and save
#         serializer = PregnancyRecordSerializer(data=mutable_data)
#         if serializer.is_valid():
#             serializer.save(patient=patient)
#             return Response({
#                 "success": True,
#                 "message": f"{patient_message} Pregnancy record added successfully."
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class CreatePatientAndPregnancy(APIView):
    permission_classes = [IsAuthenticated, IsFieldAssistant | IsMidwife]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()

        # Convert boolean fields
        family_planning_value = mutable_data.get("family_planning_after_delivery")
        mutable_data["family_planning_after_delivery"] = family_planning_value in ["1", 1, "true", "True"]

        # Convert integer fields
        int_fields = [
            "age", "husband_age", "menstruation_off_duration", "womb_count",
            "living_children", "normal_delivery_count", "c_section_count",
            "d_and_c_count", "tt_dose_count"
        ]
        for field in int_fields:
            mutable_data[field] = to_int(mutable_data.get(field))

        # Convert date fields
        mutable_data["last_period_date"] = to_date(mutable_data.get("last_period_date"))
        mutable_data["expected_delivery_date"] = to_date(mutable_data.get("expected_delivery_date"))
        mutable_data["date_of_birth"] = to_date(mutable_data.get("date_of_birth"))

        # Validate all foreign keys before saving
        try:
            village = Village.objects.get(id=mutable_data.get("village"))
            union = Union.objects.get(id=mutable_data.get("union"))
            upazila = Upazilla.objects.get(id=mutable_data.get("upazila"))
            district = District.objects.get(id=mutable_data.get("district"))
            division = Division.objects.get(id=mutable_data.get("division"))
        except (Village.DoesNotExist, Union.DoesNotExist, Upazilla.DoesNotExist, District.DoesNotExist, Division.DoesNotExist):
            return Response({"error": "Invalid location data provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare patient data dict
        patient_data = {
            "full_name": mutable_data.get("full_name"),
            "phone_number": phone_number,
            "date_of_birth": mutable_data.get("date_of_birth"),
            "husband_name": mutable_data.get("husband_name"),
            "husband_phone": mutable_data.get("husband_phone"),
            # "couple_no": mutable_data.get("couple_no"),
            "nid_number": mutable_data.get("nid_number"),
            "village": village,
            "union": union,
            "upazilla": upazila,
            "district": district,
            "division": division,
            "blood_group": mutable_data.get("blood_group"),
            "husband_blood_group": mutable_data.get("husband_blood_group"),
            "husband_earning": mutable_data.get("husband_earning"),
            "created_by": request.user,
        }

        # Prepare pregnancy record data
        pregnancy_data = {key: mutable_data.get(key) for key in mutable_data if key not in ["phone_number"]}
        
        with transaction.atomic():
            # Save patient temporarily in memory and only persist after successful pregnancy record validation
            patient = Patient(**patient_data)

            # Temporarily simulate save (not committed until transaction block ends)
            patient.save()

            # Attach patient to pregnancy data
            pregnancy_data["patient"] = patient.id

            # Validate pregnancy data
            serializer = PregnancyRecordSerializer(data=pregnancy_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Patient and pregnancy record created successfully."
                }, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                # Any error => transaction rollback
                raise serializers.ValidationError(serializer.errors) 
 

class CheckupReportCreateView(generics.CreateAPIView):
    queryset = CheckupReport.objects.all()
    serializer_class = CheckupReportSerializer
    permission_classes = [IsAuthenticated, IsMidwife]

    def create(self, request, *args, **kwargs):
        request.data["checked_by"] = request.user.id
        request.data["hospital"] = request.user.hospital.id
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            checkup_report = serializer.save()

            return Response({
                "success":True,
                "message": "Checkup report created successfully.",
                "checkup_report": serializer.data,
            }, status=status.HTTP_201_CREATED)

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckupReportDetailView(generics.RetrieveAPIView):
    serializer_class = CheckupReportSerializer
    permission_classes = [IsAuthenticated, IsMidwife]

    def post(self, request, *args, **kwargs):
        anc_id= request.data.get("id")  # Get ID from the request body
        if not anc_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            anc = AncSchedule.objects.get(id=anc_id)
            report = CheckupReport.objects.get(anc=anc)
        except CheckupReport.DoesNotExist:
            return Response({"error": "Checkup report not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
# class PregnancyDeliveryStatisticsAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         today = now().date()
#         first_day_of_current_month = today.replace(day=1)
#         first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
#         last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

#         # 1️⃣ New pregnant patients created every month
#         new_pregnant_patients = PregnancyRecord.objects.filter(created_at__month=today.month).count()

#         # 2️⃣ ANC Taken in the Previous Month (1st, 2nd, 3rd, and 4th ANC)
#         anc_breakdown = AncSchedule.objects.filter(
#             anc_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).values('status').annotate(count=Count('id'))

#         # 3️⃣ Patients who completed delivery in the previous month
#         deliveries_last_month = DeliveryRecord.objects.filter(
#             delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).count()

#         # 4️⃣ Normal vs. Cesarean Deliveries
#         delivery_type_breakdown = DeliveryRecord.objects.filter(
#             delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).values('delivery_type').annotate(count=Count('id'))

#         # 5️⃣ Stillbirth vs. Live Birth
#         birth_status_breakdown = Birth.objects.filter(
#             birth_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).values('birth_status').annotate(count=Count('id'))

#         # 6️⃣ Number of newborn children in the previous month
#         newborns_last_month = Birth.objects.filter(
#             birth_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).count()

#         # 7️⃣ Expected Deliveries in the Next Month
#         expected_deliveries_next_month = Pregnancy.objects.filter(
#             expected_delivery_date__month=today.month + 1
#         ).count()

#         # 8️⃣ Delivery Locations (Home vs. Hospital/Clinic)
#         delivery_locations = DeliveryRecord.objects.filter(
#             delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).values('delivery_location').annotate(count=Count('id'))

#         # 9️⃣ Pregnant Patients Before 18 Years
#         underage_pregnancies = Pregnancy.objects.filter(
#             patient__date_of_birth__gt=today - timedelta(days=18 * 365)
#         ).count()

#         # 🔟 Patients who completed D&C (Dilation & Curettage) last month
#         completed_dsc_last_month = DSCProcedure.objects.filter(
#             procedure_date__range=(first_day_of_previous_month, last_day_of_previous_month)
#         ).count()

#         response_data = {
#             "new_pregnant_patients_this_month": new_pregnant_patients,
#             "anc_schedule_breakdown_previous_month": list(anc_breakdown),
#             "deliveries_last_month": deliveries_last_month,
#             "delivery_type_breakdown": list(delivery_type_breakdown),
#             "birth_status_breakdown": list(birth_status_breakdown),
#             "newborns_last_month": newborns_last_month,
#             "expected_deliveries_next_month": expected_deliveries_next_month,
#             "delivery_locations": list(delivery_locations),
#             "underage_pregnancies": underage_pregnancies,
#             "completed_dsc_last_month": completed_dsc_last_month,
#         }

#         return Response(response_data)


class PregnancyDeliveryStatisticsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        today = now().date()
        first_day_of_current_month = today.replace(day=1)
        first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        next_month = (first_day_of_current_month + timedelta(days=32)).replace(day=1)

        # 1️⃣ New pregnant patients created this month
        new_pregnant_patients = PregnancyRecord.objects.filter(
            created_at__month=today.month,
            created_at__year=today.year
        ).count()

        # 2️⃣ ANC Breakdown for Previous Month
        anc_breakdown = AncSchedule.objects.filter(
            anc_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        ).values('status').annotate(count=Count('id'))

        # 3️⃣ Deliveries Last Month
        deliveries_last_month = DeliveryRecord.objects.filter(
            delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        ).count()

        # 4️⃣ Delivery Type Breakdown (Normal vs. C-Section)
        delivery_type_breakdown = PregnancyRecord.objects.filter(
            expected_delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        ).values('preferred_delivery_place').annotate(count=Count('id'))

        # 5️⃣ Baby Status Breakdown (Stillbirth vs. Live)
        birth_status_breakdown = DeliveryRecord.objects.filter(
            delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        ).values('baby_status').annotate(count=Count('id'))

        # 6️⃣ Total newborns (i.e., count of babies born alive/dead)
        newborns_last_month = DeliveryRecord.objects.filter(
            delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        ).count()

        # 7️⃣ Expected Deliveries Next Month
        expected_deliveries_next_month = PregnancyRecord.objects.filter(
            expected_delivery_date__month=next_month.month,
            expected_delivery_date__year=next_month.year
        ).count()

        # 8️⃣ Delivery Locations (Home, Hospital, Clinic) — based on `preferred_delivery_place`
        delivery_locations = PregnancyRecord.objects.filter(
            expected_delivery_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        ).values('preferred_delivery_place').annotate(count=Count('id'))

        # 9️⃣ Pregnant Patients Before 18 Years
        # ⚠️ Patient model does NOT include `date_of_birth`. You must add it for this to work.
        underage_pregnancies = 0
        # If you add date_of_birth to Patient, use the below query:
        # underage_pregnancies = PregnancyRecord.objects.filter(
        #     patient__date_of_birth__gt=today - timedelta(days=18*365)
        # ).count()

        # 🔟 D&C Procedures Last Month
        completed_dsc_last_month = 0
        # If DSCProcedure exists:
        # completed_dsc_last_month = DSCProcedure.objects.filter(
        #     procedure_date__range=(first_day_of_previous_month, last_day_of_previous_month)
        # ).count()

        response_data = {
            "new_pregnant_patients_this_month": new_pregnant_patients,
            "anc_schedule_breakdown_previous_month": list(anc_breakdown),
            "deliveries_last_month": deliveries_last_month,
            "delivery_type_breakdown": list(delivery_type_breakdown),
            "birth_status_breakdown": list(birth_status_breakdown),
            "newborns_last_month": newborns_last_month,
            "expected_deliveries_next_month": expected_deliveries_next_month,
            "delivery_locations": list(delivery_locations),
            "underage_pregnancies": underage_pregnancies,
            "completed_dsc_last_month": completed_dsc_last_month,
        }

        return Response(response_data)
    
    
    

class DashboardStatsAPIView(APIView):
    """
    Class-based API view to provide various dashboard statistics.
    """
    def get(self, request, *args, **kwargs):
        today = date.today()
        current_month = today.month
        current_year = today.year

        # Calculate dates for last month and next month
        first_day_of_current_month = date(current_year, current_month, 1)
        last_month_end_date = first_day_of_current_month - timedelta(days=1)
        
        # Calculate the first day of next month for expected deliveries
        if current_month == 12:
            first_day_of_next_month = date(current_year + 1, 1, 1)
        else:
            first_day_of_next_month = date(current_year, current_month + 1, 1)

        # --- 1. Pregnant Patients (This Month) ---
        pregnant_patients_this_month = PregnancyRecord.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year
        ).count()

        # --- 2. Total Deliveries (Last Month) ---
        total_deliveries_last_month = DeliveryRecord.objects.filter(
            delivery_date__month=last_month_end_date.month,
            delivery_date__year=last_month_end_date.year
        ).count()

        # --- 3. High-Risk Pregnancies ---
        high_risk_pregnancies_count = PregnancyRecord.objects.filter(
            Q(physical_problem__isnull=False) & ~Q(physical_problem='')
        ).count()

        # --- 4. Expected Births (Next Month) ---
        expected_births_next_month = PregnancyRecord.objects.filter(
            expected_delivery_date__month=first_day_of_next_month.month,
            expected_delivery_date__year=first_day_of_next_month.year
        ).count()

        # --- 5. Delivery Type (Last Month): Normal vs Cesarean ---
        normal_deliveries_last_month = 0
        cesarean_deliveries_last_month = 0
        if hasattr(DeliveryRecord, 'delivery_type'): # Check if the field exists
            deliveries_last_month_qs = DeliveryRecord.objects.filter(
                delivery_date__month=last_month_end_date.month,
                delivery_date__year=last_month_end_date.year
            )
            normal_deliveries_last_month = deliveries_last_month_qs.filter(delivery_type='Normal').count()
            cesarean_deliveries_last_month = deliveries_last_month_qs.filter(delivery_type='Cesarean').count()

        # --- 6. Birth Outcomes (Last Month): Stillbirth vs Live Birth ---
        deliveries_last_month_outcomes = DeliveryRecord.objects.filter(
            delivery_date__month=last_month_end_date.month,
            delivery_date__year=last_month_end_date.year
        )
        stillbirths_last_month = deliveries_last_month_outcomes.filter(baby_status='Stillborn').count()
        live_births_last_month = deliveries_last_month_outcomes.filter(baby_status='Alive').count()

        # --- 7. Delivery Location (Last Month): Hospital/Clinic vs Home ---
        hospital_clinic_deliveries_last_month = 0
        home_deliveries_last_month = 0
        if hasattr(DeliveryRecord, 'actual_delivery_place'): # Check if the field exists
            deliveries_by_place = DeliveryRecord.objects.filter(
                delivery_date__month=last_month_end_date.month,
                delivery_date__year=last_month_end_date.year
            )
            hospital_clinic_deliveries_last_month = deliveries_by_place.filter(
                actual_delivery_place__in=['Hospital', 'Clinic']
            ).count()
            home_deliveries_last_month = deliveries_by_place.filter(actual_delivery_place='Home').count()

        # --- 8. Monthly Pregnancies Trend (Last 6 Months) ---
        monthly_pregnancy_data = []
        months_labels = []
        for i in range(6): # Iterate for 6 months
            target_month = current_month - i
            target_year = current_year
            if target_month <= 0:
                target_month += 12
                target_year -= 1
            
            count = PregnancyRecord.objects.filter(
                created_at__month=target_month,
                created_at__year=target_year
            ).count()
            
            monthly_pregnancy_data.insert(0, count)
            months_labels.insert(0, calendar.month_abbr[target_month])

        # --- 9. High-Risk Pregnancies by Union ---
        high_risk_by_union = PregnancyRecord.objects.filter(
            Q(physical_problem__isnull=False) & ~Q(physical_problem='')
        ).values(
            'patient__union__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        union_labels = []
        union_counts = []
        other_count = 0
        top_n_unions = 4 
        for i, item in enumerate(high_risk_by_union):
            if i < top_n_unions:
                union_labels.append(item['patient__union__name'] or "Unknown Union")
                union_counts.append(item['count'])
            else:
                other_count += item['count']
        if other_count > 0:
            union_labels.append('Other')
            union_counts.append(other_count)
        
        # --- 10. ANC Schedule Breakdown (Last Month) ---
        anc_reports_last_month = CheckupReport.objects.filter(
            created_at__month=last_month_end_date.month,
            created_at__year=last_month_end_date.year
        )
        anc_1st = anc_reports_last_month.filter(anc_checkup_number=1).count()
        anc_2nd = anc_reports_last_month.filter(anc_checkup_number=2).count()
        anc_3rd = anc_reports_last_month.filter(anc_checkup_number=3).count()
        anc_4th = anc_reports_last_month.filter(anc_checkup_number=4).count()

        # Compile data into a dictionary
        data = {
            'pregnant_patients_this_month': pregnant_patients_this_month,
            'total_deliveries_last_month': total_deliveries_last_month,
            'high_risk_pregnancies_count': high_risk_pregnancies_count,
            'total_births_last_month': total_deliveries_last_month,
            'expected_births_next_month': expected_births_next_month,

            'delivery_type_last_month': {
                'normal': normal_deliveries_last_month,
                'cesarean': cesarean_deliveries_last_month,
            },
            'birth_outcomes_last_month': {
                'stillbirths': stillbirths_last_month,
                'live_births': live_births_last_month,
            },
            'delivery_location_last_month': {
                'hospital_clinic': hospital_clinic_deliveries_last_month,
                'home': home_deliveries_last_month,
            },
            'monthly_pregnancies_trend': {
                'labels': months_labels,
                'data': monthly_pregnancy_data,
            },
            'high_risk_pregnancies_by_union': {
                'labels': union_labels,
                'data': union_counts,
            },
            'anc_schedule_last_month': {
                '1st_anc': anc_1st,
                '2nd_anc': anc_2nd,
                '3rd_anc': anc_3rd,
                '4th_anc': anc_4th,
            },
        }

        # Use the serializer to validate and render the data
        serializer = DashboardStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True) # Ensure data matches serializer structure
        return Response(serializer.data, status=status.HTTP_200_OK)





class DjangoDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        current_month_start = today.replace(day=1)

        end_of_last_month = current_month_start - timedelta(days=1)
        start_of_last_month = end_of_last_month.replace(day=1)

        start_of_next_month = current_month_start + relativedelta(months=1)
        end_of_next_month = (start_of_next_month + relativedelta(months=1)) - timedelta(days=1)

        aware_start_last_month = timezone.make_aware(datetime.combine(start_of_last_month, datetime.min.time()))
        aware_end_last_month = timezone.make_aware(datetime.combine(end_of_last_month, datetime.max.time()))
        aware_start_current_month = timezone.make_aware(datetime.combine(current_month_start, datetime.min.time()))
        aware_today = timezone.make_aware(datetime.combine(today, datetime.max.time()))
        aware_start_next_month = timezone.make_aware(datetime.combine(start_of_next_month, datetime.min.time()))
        aware_end_next_month = timezone.make_aware(datetime.combine(end_of_next_month, datetime.max.time()))

        # Get user's upazila
        user_upazila = getattr(getattr(request.user, 'hospital', None), 'upazila', None)
        if not user_upazila:
            return Response({'detail': 'Upazila not associated with user.'}, status=status.HTTP_400_BAD_REQUEST)

        base_filter = Q(patient__union__upazilla=user_upazila)

        pregnant_patients_this_month = PregnancyRecord.objects.filter(
            base_filter,
            created_at__gte=aware_start_current_month,
            created_at__lte=aware_today
        ).count()

        total_deliveries_last_month = DeliveryRecord.objects.filter(
            base_filter,
            delivery_date__gte=start_of_last_month,
            delivery_date__lte=end_of_last_month
        ).count()

        high_risk_by_physical = PregnancyRecord.objects.filter(
            base_filter,
            Q(physical_problem__isnull=False) & ~Q(physical_problem__exact='')
        )

        high_risk_checkup = CheckupReport.objects.filter(
            Q(diabetes=True) |
            Q(thyroid_disease=True) |
            Q(heart_disease=True) |
            Q(bronchial_asthma=True) |
            Q(kidney_disease=True) |
            Q(epilepsy=True) |
            Q(history_iud=True) |
            Q(history_stillbirth=True) |
            Q(history_preclampsia=True) |
            Q(history_eclampsia=True),
            pregnancy_record__patient__union__upazilla=user_upazila
        ).select_related("pregnancy_record")

        high_risk_pregnancies_ids = set(high_risk_by_physical.values_list("id", flat=True)) | \
                                    set(high_risk_checkup.values_list("pregnancy_record_id", flat=True))
        high_risk_pregnancies = len(high_risk_pregnancies_ids)

        total_births_last_month = DeliveryRecord.objects.filter(
            base_filter,
            delivery_date__gte=start_of_last_month,
            delivery_date__lte=end_of_last_month,
            baby_status='Alive'
        ).count()

        expected_births_next_month = PregnancyRecord.objects.filter(
            base_filter,
            expected_delivery_date__gte=start_of_next_month,
            expected_delivery_date__lte=end_of_next_month
        ).count()

        delivery_type_data = DeliveryRecord.objects.filter(
            base_filter,
            delivery_date__gte=start_of_last_month,
            delivery_date__lte=end_of_last_month
        ).values('delivery_type').annotate(count=Count('delivery_type'))

        normal_deliveries = 0
        cesarean_deliveries = 0
        for item in delivery_type_data:
            if item['delivery_type'] == 'Normal':
                normal_deliveries = item['count']
            elif item['delivery_type'] == 'Cesarean':
                cesarean_deliveries = item['count']

        birth_outcomes_data = DeliveryRecord.objects.filter(
            base_filter,
            delivery_date__gte=start_of_last_month,
            delivery_date__lte=end_of_last_month
        ).values('baby_status').annotate(count=Count('baby_status'))

        stillbirths = 0
        live_births_count = 0
        for item in birth_outcomes_data:
            if item['baby_status'] == 'Stillborn':
                stillbirths = item['count']
            elif item['baby_status'] == 'Alive':
                live_births_count = item['count']

        location_data = DeliveryRecord.objects.filter(
            base_filter,
            delivery_date__gte=start_of_last_month,
            delivery_date__lte=end_of_last_month
        ).values('actual_delivery_place').annotate(count=Count('actual_delivery_place'))

        hospital_clinic = 0
        home = 0
        for item in location_data:
            if item['actual_delivery_place'] in ['Hospital', 'Clinic']:
                hospital_clinic += item['count']
            elif item['actual_delivery_place'] == 'Home':
                home = item['count']

        monthly_pregnancy_data = []
        for i in range(5, -1, -1):
            month_date = today - relativedelta(months=i)
            month_start = month_date.replace(day=1)
            month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)

            count = PregnancyRecord.objects.filter(
                base_filter,
                created_at__gte=timezone.make_aware(datetime.combine(month_start, datetime.min.time())),
                created_at__lte=timezone.make_aware(datetime.combine(month_end, datetime.max.time()))
            ).count()

            monthly_pregnancy_data.append({
                'month': calendar.month_abbr[month_date.month],
                'count': count
            })

        trend_labels = [item['month'] for item in monthly_pregnancy_data]
        trend_series = [item['count'] for item in monthly_pregnancy_data]

        high_risk_by_union = PregnancyRecord.objects.filter(
            id__in=high_risk_pregnancies_ids
        ).values('patient__union__name').annotate(count=Count('id')).order_by('-count')

        high_risk_union_names = []
        high_risk_union_counts = []
        for item in high_risk_by_union:
            union_name = item['patient__union__name'] or 'Unknown Union'
            high_risk_union_names.append(union_name)
            high_risk_union_counts.append(item['count'])

        anc_schedule = CheckupReport.objects.filter(
            pregnancy_record__patient__union__upazilla=user_upazila,
            created_at__gte=aware_start_last_month,
            created_at__lte=aware_end_last_month
        ).values('anc_checkup_number').annotate(count=Count('anc_checkup_number'))

        anc_counts = {'1st ANC': 0, '2nd ANC': 0, '3rd ANC': 0, '4th ANC': 0}
        for item in anc_schedule:
            number = item['anc_checkup_number']
            if number == 1:
                anc_counts['1st ANC'] = item['count']
            elif number == 2:
                anc_counts['2nd ANC'] = item['count']
            elif number == 3:
                anc_counts['3rd ANC'] = item['count']
            elif number == 4:
                anc_counts['4th ANC'] = item['count']

        response_data = {
            'pregnant_patients_this_month': pregnant_patients_this_month,
            'total_deliveries_last_month': total_deliveries_last_month,
            'high_risk_pregnancies': high_risk_pregnancies,
            'total_births_last_month': total_births_last_month,
            'expected_births_next_month': expected_births_next_month,
            'delivery_type_chart_data': {
                'series': [normal_deliveries, cesarean_deliveries],
                'labels': ['Normal', 'Cesarean'],
            },
            'birth_outcomes_chart_data': {
                'series': [stillbirths, live_births_count],
                'labels': ['Stillbirths', 'Live Births'],
            },
            'delivery_location_last_month': {
                'hospital_clinic': hospital_clinic,
                'home': home,
            },
            'monthly_pregnancies_trend_chart_data': {
                'labels': trend_labels,
                'series': trend_series,
            },
            'high_risk_pregnancies_by_union_chart_data': {
                'categories': high_risk_union_names,
                'series': [{
                    'name': 'High-Risk Pregnancies',
                    'data': high_risk_union_counts
                }]
            },
            'anc_schedule_last_month': anc_counts,
        }

        return Response(response_data, status=status.HTTP_200_OK)