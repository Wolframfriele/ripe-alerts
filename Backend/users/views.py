from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegistrationSerializer
from ripe_atlas.exceptions import TokenNotValid

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


class RegistrationService(APIView):
    """Create new user account. """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_user = serializer.save()
                return Response(get_tokens_for_user(new_user), status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'user with that username already exists'},
                                status=status.HTTP_400_BAD_REQUEST)
            except TokenNotValid:
                return Response({"message": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class UserDetail(APIView):
    """Returns specific information of authenticated user"""

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


class SystemList(APIView):
    def get(self, request):
        """returns all systems that the user has an alert on, systems is categorized by """
