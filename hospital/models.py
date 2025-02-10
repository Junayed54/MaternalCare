from django.db import models
# from maternityTrack.models import Upazilla

class Hospital(models.Model):
    upazila = models.OneToOneField("maternityTrack.Upazilla", on_delete=models.CASCADE, related_name="health_complex")
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    total_beds = models.PositiveIntegerField(default=0)
    available_beds = models.PositiveIntegerField(default=0)
    total_doctors = models.PositiveIntegerField(default=0)
    total_nurses = models.PositiveIntegerField(default=0)
    total_staff = models.PositiveIntegerField(default=0)
    emergency_services = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.upazila.name}, {self.upazila.district.name})"
    
    
    
    
class BloodBank(models.Model):
    health_complex = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name="blood_bank")
    blood_group = models.CharField(
        max_length=3,
        choices=[("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("O+", "O+"), 
                 ("O-", "O-"), ("AB+", "AB+"), ("AB-", "AB-")],
    )
    total_units = models.PositiveIntegerField(default=0)  # Total available units of this blood type
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} - {self.total_units} units ({self.health_complex.name})"


class AmbulanceService(models.Model):
    health_complex = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="ambulance_services")
    driver_name = models.CharField(max_length=255)
    driver_phone = models.CharField(max_length=15, unique=True)
    ambulance_number = models.CharField(max_length=50, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Ambulance {self.ambulance_number} - {self.health_complex.name}"
