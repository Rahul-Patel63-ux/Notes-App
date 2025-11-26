from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AdminUserModel

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        try:
            return AdminUserModel.objects.get(id=user_id)
        except AdminUserModel.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")
