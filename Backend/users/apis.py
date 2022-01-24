from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, InitialSetupSerializer
from ripe_atlas.exceptions import TokenNotValid


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
        user_information = {"username": request.user.username,
                            "ripe_api_token": request.user.ripe_user.ripe_api_token,
                            "initial_setup_complete": request.user.ripe_user.initial_setup_complete}
        return Response(user_information)


class InitialSetup(APIView):
    """
        INPUT: asns, email
        OUTPUT: user data
    """

    def post(self, request):

        temporary_user = User.objects.get(pk=1)
        # if request.user.ripe_user.initial_setup_complete:
        if temporary_user.ripe_user.initial_setup_complete:
            return Response({"message": "user has already completed the initial setup!"},
                            status=status.HTTP_403_FORBIDDEN)

        initial_setup_serializer = InitialSetupSerializer(data=request.data)

        if not initial_setup_serializer.is_valid():
            return Response(initial_setup_serializer.errors, status=status.HTTP_409_CONFLICT)

        try:
            user = initial_setup_serializer.save(user=temporary_user)
        except Exception:
                    return Response("OOPS something went wrong :(", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(user, status=status.HTTP_201_CREATED)
