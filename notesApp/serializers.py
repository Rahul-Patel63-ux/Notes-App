
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminUserModel
        fields = ["username", "email", "password", "c_password", "role"]
        extra_kwargs = {'password': {'write_only': True}, 'c_password': {'write_only': True},}

    def validate(self, data):

        # Check if user fave any special charactors
        if any([c in "~`!@#$%^&*()_+=-{[]}|\/?;:.," for c in data["username"]]):
            raise serializers.ValidationError("Special charactors not allowed")
        
        # check if same role have existing email
        if AdminUserModel.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Eamil already exist")

        # check is password did not match
        if data['password'] != data['c_password']:
            raise serializers.ValidationError("Password did not match!")
        
        return data
    
    def create(self, validated_data):

        validated_data["password"] =  make_password(validated_data["password"])
        validated_data["c_password"] =  make_password(validated_data["c_password"])

        user = AdminUserModel.objects.create(**validated_data)
        return user
    

class NoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NotesModel
        fields = ["id", "note", "created_at"]
        read_only_fields = ["created_at"]
        

class AdminUserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = AdminUserModel
        # fields = ["id", "username", "email", "created_at", "is_active", "notes", "role"]
        fields = "__all__"