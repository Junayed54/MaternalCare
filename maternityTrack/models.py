from django.db import models
from hospital.models import Hospital
from django.contrib.auth import get_user_model
from datetime import timedelta
User = get_user_model()

class Division(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class District(models.Model):
    division = models.ForeignKey(Division, related_name='districts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Upazilla(models.Model):
    district = models.ForeignKey(District, related_name='upazillas', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Union(models.Model):
    upazilla = models.ForeignKey(Upazilla, related_name='unions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Village(models.Model):
    union = models.ForeignKey(Union, related_name='villages', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    word_no = models.PositiveIntegerField(choices=[(1, "Ward No: 1"), (2, "Ward No: 2"), (3, "Ward No: 3")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Ward No: {self.word_no})"


class PostOffice(models.Model):
    union = models.ForeignKey(Union, related_name='post_offices', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_patients", null=True, blank=True)

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    
    husband_name = models.CharField(max_length=255)
    husband_phone = models.CharField(max_length=20)
    
    couple_no = models.CharField(max_length=50, unique=True)
    nid_number = models.CharField(max_length=50, unique=True)
    
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    # ward_number = models.CharField(max_length=10)
    union = models.ForeignKey(Union, on_delete=models.CASCADE)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    husband_blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    
    husband_earning = models.DecimalField(max_digits=10, decimal_places=2, help_text="Husband's earning per month")

    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} (Patient Profile)"


class PregnancyRecord(models.Model):
    DELIVERY_CHOICES = [
        ('Hospital', 'Hospital'),
        ('Clinic', 'Clinic'),
        ('Home', 'Home')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="pregnancies")
    
    age = models.IntegerField()
    husband_age = models.IntegerField()
    
    pregnancy_count = models.PositiveIntegerField(help_text="Pregnancy Number", default=1)
    menstruation_off_duration = models.IntegerField(help_text="How long is menstruation off (in months)")
    
    womb_count = models.IntegerField(help_text="How many wombs")
    living_children = models.IntegerField(help_text="Number of living children")
    last_child_age = models.IntegerField(null=True, blank=True, help_text="Last child's age")
    
    normal_delivery_count = models.IntegerField(help_text="Previous normal deliveries")
    c_section_count = models.IntegerField(help_text="Previous C-sections")
    d_and_c_count = models.IntegerField(help_text="Previous D&C/MRI procedures")
    
    preferred_delivery_place = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    tt_dose_count = models.IntegerField(help_text="How many TT doses taken")
    
    family_planning_after_delivery = models.BooleanField(default=False, help_text="Willing to take family planning after delivery?")
    physical_problem = models.TextField(null=True, blank=True, help_text="Any physical problems?")
    
    last_period_date = models.DateField()
    expected_delivery_date = models.DateField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Automatically create 4 ANC schedules per pregnancy. """
        is_new = self._state.adding  # Check if this is a new entry
        super().save(*args, **kwargs)

        if is_new:  # Only create ANC schedules for new pregnancies
            self.create_anc_schedules()

    def create_anc_schedules(self):
        """ Generate 4 ANC schedules spread across 10 months. """
        schedule_intervals = [75, 150, 225, 300]  # ANC schedule in days
        for days in schedule_intervals:
            AncSchedule.objects.create(
                pregnancy_record=self,
                anc_date=self.last_period_date + timedelta(days=days),
                status="Scheduled"
            )

    def __str__(self):
        return f"{self.patient.full_name} (Pregnancy {self.pregnancy_count})"



class AncSchedule(models.Model):
    pregnancy_record = models.ForeignKey(PregnancyRecord, on_delete=models.CASCADE)  # Updated field name
    anc_date = models.DateField()  # Scheduled ANC date
    status = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'), 
        ('Completed', 'Completed'), 
        ('Missed', 'Missed')
    ])
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    def __str__(self):
        return f"ANC schedule for {self.pregnancy_record.patient.full_name} on {self.anc_date}"

class CheckupReport(models.Model):
    ANC_CHOICES = [
        (1, '1st ANC'),
        (2, '2nd ANC'),
        (3, '3rd ANC'),
        (4, '4th ANC'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="checkup_reports")
    anc = models.ForeignKey(AncSchedule, null=True, blank=True, on_delete=models.SET_NULL)  # Keep this if tracking schedules
    anc_checkup_number = models.PositiveSmallIntegerField(choices=ANC_CHOICES, null=True, blank=True)  # NEW FIELD
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    bp = models.CharField(max_length=20)  # Blood Pressure (e.g., 120/80)
    rbs = models.DecimalField(max_digits=5, decimal_places=2)  # Random Blood Sugar (e.g., 120.5)
    pulse = models.IntegerField()  # Pulse rate
    ifa = models.BooleanField()  # Iron-Folic Acid supplementation (Yes/No)
    diabetes = models.BooleanField()  # Diabetes (Yes/No)
    thyroid_disease = models.BooleanField()  # Thyroid disease (Yes/No)
    heart_disease = models.BooleanField()  # Heart disease (Yes/No)
    bronchial_asthma = models.BooleanField()  # Bronchial Asthma (Yes/No)
    kidney_disease = models.BooleanField()  # Kidney disease (Yes/No)
    epilepsy = models.BooleanField()  # Epilepsy (Yes/No)
    placenta_location = models.CharField(max_length=255)  # Placenta location (e.g., Anterior/Posterior)
    history_iud = models.BooleanField()  # History of Intrauterine Death (Yes/No)
    history_stillbirth = models.BooleanField()  # History of Stillbirth (Yes/No)
    history_preclampsia = models.BooleanField()  # History of Preeclampsia (Yes/No)
    history_eclampsia = models.BooleanField()  # History of Eclampsia (Yes/No)
    additional_notes = models.TextField(null=True, blank=True)  # Other medical records or notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checkup for {self.patient.full_name} ({dict(self.ANC_CHOICES).get(self.anc_checkup_number, 'Unknown')}) on {self.created_at}"



class DeliveryRecord(models.Model):
    STATUS_CHOICES = [
        ("Alive", "Alive"),
        ("Deceased", "Deceased"),
        ("Stillborn", "Stillborn"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    patient_phone = models.CharField(max_length=15, unique=True, help_text="Phone number of the mother")
    mother_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Alive", help_text="Mother's status")
    delivery_date = models.DateField(help_text="Date of delivery")
    
    # Baby details
    baby_name = models.CharField(max_length=100, null=True, blank=True, help_text="Full name of the baby")
    baby_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    baby_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Alive", help_text="Baby's status")
    
    # Death details (if applicable)
    mother_death_date = models.DateField(null=True, blank=True, help_text="Date of mother's death")
    cause_of_mother_death = models.TextField(null=True, blank=True, help_text="Cause of mother's death")

    def __str__(self):
        return f"Delivery Record - {self.patient_phone} (Mother: {self.mother_status}, Baby: {self.baby_status})"
