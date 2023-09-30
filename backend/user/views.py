###############################################
# IMPORTS
###############################################
# Django imports
from django.shortcuts import render

# Model imports
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

# Rest Framework Imports
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


# JWT token import
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

###############################################
# VIEWS
###############################################
class RegisterUserView(APIView):
    def get(self, request):
        """
        To check whether the email given at registration already exists or not
        """
        email = request.query_params.get('email')

        # Check if a user with the given email already exists
        user = User.objects.filter(email=email).first()

        if user:
            return Response({'result': False, 'message': 'Email already exists.'}, status=status.HTTP_200_OK)
        else:
            return Response({'result': True}, status=status.HTTP_200_OK)
    def post(self, request):
        """
        Creates a user account
        """
        # Extract user registration data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)

            # Generate JWT tokens for the registered user
            tokens = get_tokens_for_user(user)

            response_obj = Response({'result': 'success', 'tokens': tokens}, status=status.HTTP_200_OK)
            response_obj.set_cookie('jwt-access',tokens["access"],httponly=True)
            response_obj.set_cookie('jwt-refresh',tokens['refresh'],httponly=True)
            return response_obj

        except Exception as e:
            return Response({'error': 'User registration failed.'}, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        """
        User Login End point
        """
        # Extract login data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check whether user exists or not.
        user = User.objects.filter(username = username).first()

        if user is not None and check_password(password, user.password):
            # Generate JWT tokens for the authenticated user
            tokens = get_tokens_for_user(user)
            response_obj = Response({'result': 'success', 'tokens': tokens}, status=status.HTTP_200_OK)
            response_obj.set_cookie('jwt-access',tokens["access"],httponly=True)
            response_obj.set_cookie('jwt-refresh',tokens['refresh'],httponly=True)
            return response_obj
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class GetUserDetailsView(APIView):
    """
    Returns the user details only if the jwt tokens exist
    """
    def get(self, request):
        try:
            # Extract the access token from the request
            access_token = AccessToken(request.COOKIES.get('jwt-access'))

            # Access the user identifier claim
            user_id = access_token['user_id']

            # Use the user identifier to fetch the associated user
            user = User.objects.get(id=user_id)


            # Customize this part to return the user's details as needed
            user_details = {
                'username': user.username,
                'email': user.email,
                # Add other user details here
            }

            return Response({'result': 'success', 'details': user_details}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(APIView):
    def post(self, request):
        """
        Logout function for user
        """
        response = Response({'result': 'success', 'message': 'Logged out successfully.'})

        # Clear HTTP-only cookies containing JWT tokens
        response.delete_cookie('jwt-access')
        response.delete_cookie('jwt-refresh')

        return response
    
class DeleteUserView(APIView):
    def post(self, request):
        """
        To delete the user account
        """
        try:
            # Extract the access token from the request
            access_token = AccessToken(request.COOKIES.get('jwt-access'))

            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            provided_password = request.data.get('password')  
            if user.check_password(provided_password):
                # Delete the user account
                user.delete()
                return Response({'result': 'Account deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
