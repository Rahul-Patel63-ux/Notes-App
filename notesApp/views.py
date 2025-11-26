from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


# To specify Admin user Accessable views
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"



class RegisterView(APIView):

    def get(self, request):
        return render(request, "html/register.html")
    
    def post(self, request):
        serializer = RegisterSerializer(data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "User created successfully.",
                'user': serializer.data,
            }, status=201)
        
        return Response({
            'error': serializer.errors,
        }, status=400)
    

class LoginView(APIView):

    def get(self, request):
        return render(request, "html/login.html")

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = AdminUserModel.objects.get(username= username, is_active=True)

        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            serializer = AdminUserSerializer(user)
            # refresh['role'] = user.role

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.role
            }, status=201)
        
        return Response({
            'error': "Invalid cridentials",
        }, status=400)
    


class UserNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = NotesModel.objects.filter(user_id= request.user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response({
            "data": serializer.data,
        }, status=201)


    def post(self, request):

        serializer = NoteSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Note created successfully.",
                "data": serializer.data
            }, status=201)

        return Response({
            'error': serializer.errors,
        }, status=400)

        
    
class AdminNoteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        users = AdminUserModel.objects.all()
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data, status=201)
    
def admin_dashboard(request):
    # users = AdminUserModel.objects.all()
    return render(request, "html/admin/admin_dashboard.html")

def user_dashboard(request):
    return render(request, "html/user/user_dashboard.html")


class AdminNoteModifiyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(sele, request, pk):
        
        user = AdminUserModel.objects.get(id = pk).prefetch_related('notes')
        user.delete()
        return Response("User deleted successfully")
    
    
    
