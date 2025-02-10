from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'id_card_number', 'full_name', 'father_name', 'husband_name',
            'mother_name', 'role', 'date_of_birth', 'address', 'email', 'is_active', 'is_staff', 
            'is_superuser', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'password', 'id_card_number', 'role', 'date_of_birth', 'address', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'father_name', 'husband_name', 'mother_name', 'role', 'date_of_birth', 'address', 'email']

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        # Use authenticate method to verify credentials
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid phone number or password.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            "phone_number": user.phone_number,  # You might not need this, but if you want to return it, you can
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

