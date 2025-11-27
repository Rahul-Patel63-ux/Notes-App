# Notes-App
A secure and scalable REST API built using Django REST Framework with JWT Authentication and Role-Based Access Control.
The system uses a single custom user model where each user has a role (admin or user) and based on this role, different API permissions are applied.

## Features:
- Authentication
- Register new users
- Login using JWT (access + refresh tokens)
- Password hashing & secure credentials storage

# User Roles:
- Admin
- Can view all users
- Can view all notes created by users
- User
- Can create, read, update, and delete only their own notes

# Notes Management:
- Create notes
- View your notes
- Update your notes
- Delete your notes

# Security:
- JWT Authentication
- Custom permission classes (IsAdmin)
- Route protection using IsAuthenticated

# Tech Stack:
- Backend: Django, Django REST Framework
- Authentication: JWT (SimpleJWT)
- Database:  MySQL
- Frontend: HTML + CSS + Vanilla JavaScript

# Scalability Approach
This Notes App is built with scalability in mind. Below are strategies used (or easy to add later) to ensure the system can grow without performance issues:

# 1. Microservices Architecture
- Authentication, Users, and Notes can be separated into independent services.
- Each service can be deployed, scaled, and updated independently.
- Helps avoid bottlenecks and keeps the app modular.

# 2. Caching
- Frequently accessed data (like notes list or user profile).
- Reduces repeated database hits.
- Improves response time significantly.