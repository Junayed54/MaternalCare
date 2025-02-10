from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from hospital.models import Hospital
class UserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone number field must be set")
        if not full_name:
            raise ValueError("The Full Name field must be set")

        extra_fields.setdefault("is_active", True)

        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('AdMIN', 'Admin'),
        ("UHFPO", "Upazila Health & Family Planning Officer"),
        ("FS", "Field Assistant"),
        ("MIDWIFE", "Midwife"),
    ]
    hospital = models.ForeignKey('hospital.Hospital', on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    id_card_number = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Optional field
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    husband_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)  # Email can also be optional
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]  # Removed `id_card_number` from required fields

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    @property
    def is_admin(self):
        return self.is_superuser
