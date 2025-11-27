from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .serializers import *


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, "role", None) == "admin")


# Register API
class RegisterView(APIView):

    def get(self, request):
        return render(request, "html/register.html")
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "User created successfully.",
                'user': serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)



# Login API
class LoginView(APIView):

    def get(self, request):
        return render(request, "html/login.html")

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username & Password required"}, status=400)

        try:
            user = AdminUserModel.objects.get(username=username, is_active=True)
        except AdminUserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        }, status=200)


# USER NOTES LIST + CREATE
class UserNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = NotesModel.objects.filter(user_id=request.user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response({"data": serializer.data}, status=200)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Note created successfully.",
                "data": serializer.data
            }, status=201)

        return Response({'error': serializer.errors}, status=400)



# ADMIN: VIEW ALL USERS + NOTES
class AdminNoteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = AdminUserModel.objects.all()
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data, status=200)



# HTML VIEWS
def admin_dashboard(request):
    return render(request, "html/admin/admin_dashboard.html")

def create_note(request):
    return render(request, "html/user/create_note.html")

def user_dashboard(request):
    return render(request, "html/user/user_dashboard.html")



# USER NOTE READ/UPDATE/DELETE
class UserNoteModifiyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        note = NotesModel.objects.filter(id=pk, user=user).first()
        return note

    def get(self, request, pk):
        note = self.get_object(pk, request.user)
        
        if not note:
            return Response({"error": "Note not found"}, status=404)

        serializer = NoteSerializer(note)
        return Response({"data": serializer.data}, status=200)

    def put(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({"error": "Note not found"}, status=404)

        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Note updated successfully"}, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({"error": "Note not found"}, status=404)

        note.delete()
        return Response({"message": "Note deleted successfully"}, status=200)
