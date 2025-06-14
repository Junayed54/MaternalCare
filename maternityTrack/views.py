from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from datetime import timedelta
from django.shortcuts import get_object_or_404

from accounts.permissions import * 
from django.utils.timezone import now
from django.db.models import Count


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
                "couple_no": request.data.get("couple_no"),
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


class CreatePatientAndPregnancy(APIView):
    permission_classes = [IsAuthenticated, IsFieldAssistant | IsMidwife]  # Requires authentication

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Make a mutable copy of request.data before modifying it
        mutable_data = request.data.copy()

        patient = Patient.objects.filter(phone_number=phone_number).first()

        # ✅ Convert "1" and "0" to boolean
        family_planning_value = mutable_data.get("family_planning_after_delivery")
        mutable_data["family_planning_after_delivery"] = family_planning_value in ["1", 1, "true", "True"]

        # ✅ Initialize variables to avoid UnboundLocalError
        village = union = upazilla = district = division = None

        if not patient:
            try:
                village = Village.objects.get(id=mutable_data.get("village"))
                union = Union.objects.get(id=mutable_data.get("union"))
                upazilla = Upazilla.objects.get(id=mutable_data.get("upazilla"))
                district = District.objects.get(id=mutable_data.get("district"))
                division = Division.objects.get(id=mutable_data.get("division"))
            except (Village.DoesNotExist, Union.DoesNotExist, Upazilla.DoesNotExist, District.DoesNotExist, Division.DoesNotExist):
                return Response({"error": "Invalid location data provided."}, status=status.HTTP_400_BAD_REQUEST)

            patient = Patient.objects.create(
                full_name=mutable_data.get("full_name"),
                phone_number=phone_number,
                husband_name=mutable_data.get("husband_name"),
                husband_phone=mutable_data.get("husband_phone"),
                couple_no=mutable_data.get("couple_no"),
                nid_number=mutable_data.get("nid_number"),
                village=village,
                # ward_number=mutable_data.get("ward_number"),
                union=union,
                upazilla=upazilla,
                district=district,
                division=division,
                blood_group=mutable_data.get("blood_group"),
                husband_blood_group=mutable_data.get("husband_blood_group"),
                husband_earning=mutable_data.get("husband_earning"),
                created_by=request.user  
            )
            patient_message = "Patient created successfully."
        else:
            # ✅ Fetch location objects if IDs are provided
            try:
                if mutable_data.get("village"):
                    village = Village.objects.get(id=mutable_data.get("village"))
                if mutable_data.get("union"):
                    union = Union.objects.get(id=mutable_data.get("union"))
                if mutable_data.get("upazilla"):
                    upazilla = Upazilla.objects.get(id=mutable_data.get("upazilla"))
                if mutable_data.get("district"):
                    district = District.objects.get(id=mutable_data.get("district"))
                if mutable_data.get("division"):
                    division = Division.objects.get(id=mutable_data.get("division"))
            except (Village.DoesNotExist, Union.DoesNotExist, Upazilla.DoesNotExist, District.DoesNotExist, Division.DoesNotExist):
                return Response({"error": "Invalid location data provided."}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Update existing patient safely
            patient.full_name = mutable_data.get("full_name", patient.full_name)
            patient.husband_name = mutable_data.get("husband_name", patient.husband_name)
            patient.husband_phone = mutable_data.get("husband_phone", patient.husband_phone)
            patient.couple_no = mutable_data.get("couple_no", patient.couple_no)
            patient.nid_number = mutable_data.get("nid_number", patient.nid_number)
            # patient.ward_number = mutable_data.get("ward_number", patient.ward_number)
            patient.blood_group = mutable_data.get("blood_group", patient.blood_group)
            patient.husband_blood_group = mutable_data.get("husband_blood_group", patient.husband_blood_group)
            patient.husband_earning = mutable_data.get("husband_earning", patient.husband_earning)

            # ✅ Assign fetched location objects only if they exist
            if village: patient.village = village
            if union: patient.union = union
            if upazilla: patient.upazilla = upazilla
            if district: patient.district = district
            if division: patient.division = division

            patient.save()
            patient_message = "Patient updated successfully."

        # ✅ Create Pregnancy Record
        mutable_data.pop("phone_number", None)
        mutable_data["patient"] = patient.id
        pregnancy_serializer = PregnancyRecordSerializer(data=mutable_data)
        if pregnancy_serializer.is_valid():
            pregnancy_serializer.save(patient=patient)
            return Response({
                "success": True,
                "message": f"{patient_message} Pregnancy record added successfully."
            }, status=status.HTTP_201_CREATED)
        
        else:
            
            return Response(pregnancy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
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