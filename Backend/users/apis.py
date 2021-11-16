from django.db import IntegrityError
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
    User chooses his systems: targets and anchors and related measurements to put an alert on.
    User chooses where to receive alert on: the email.
    Systems stores the input of the users and creates alert_configurations based on the input.

    """

    def post(self, request):

        if request.user.ripe_user.initial_setup_complete:
            return Response({"message": "user has already completed the initial setup!"},
                            status=status.HTTP_403_FORBIDDEN)

        initial_setup_serializer = InitialSetupSerializer(data=request.data)

        if not initial_setup_serializer.is_valid():
            return Response(initial_setup_serializer.errors, status=status.HTTP_409_CONFLICT)

        # try:
        user = initial_setup_serializer.save(user=request.user)
        # except Exception:
        #     return Response("OOPS", status=status.HTTP_400_BAD_REQUEST)
        return Response(user, status=status.HTTP_201_CREATED)


class SystemList(APIView):
    def get(self, request):
        """returns all systems that the user has an alert on, systems is categorized by """
        pass