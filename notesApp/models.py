
from django.db import models

class AdminUserModel(models.Model):

    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('user', 'user'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    c_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}"

    @property
    def is_authenticated(self):
        return True
    

class NotesModel(models.Model):

    user = models.ForeignKey(AdminUserModel, on_delete= models.CASCADE, related_name='notes')
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.note}"
