from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password  # For hashing and checking passwords
from .models import User, Admin
import json

# Create User
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if not (first_name and last_name and email and password):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Hash the password before saving it
        hashed_password = make_password(password)

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password  # Store the hashed password
        )

        return JsonResponse({'message': 'User created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# Login User
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if not (email and password):
            return JsonResponse({'error': 'Missing email or password'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

        # Check the password
        if check_password(password, user.password):
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# views.py

@csrf_exempt
def create_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')

        if not (email and password and full_name):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if Admin.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Admin email already exists'}, status=400)

        hashed_password = make_password(password)
        Admin.objects.create(
            email=email,
            password=hashed_password,
            full_name=full_name
        )
        return JsonResponse({'message': 'Admin created successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            admin = Admin.objects.get(email=email)
            if check_password(password, admin.password):
                return JsonResponse({'message': 'Admin login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer

class CreateUserView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)