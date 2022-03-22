from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, InitialSetupSerializer, AsnSerializer
from ripe_atlas.exceptions import TokenNotValid
from .services import get_monitored_asns


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
        # user = request.user
        user = User.objects.first()
        if hasattr(user, 'ripe_user'):
            user_information = {"username": user.username,
                                "ripe_api_token": user.ripe_user.ripe_api_token,
                                "initial_setup_complete": user.ripe_user.initial_setup_complete}
        else:
            user_information = {"username": user.username,
                                "ripe_api_token": None,
                                "initial_setup_complete": False}
        return Response(user_information, status=status.HTTP_200_OK)


class InitialSetup(APIView):
    """
        INPUT: asns, email
        OUTPUT: user data
    """
    def post(self, request):
        # user = request.user
        user = User.objects.first()

        initial_setup_serializer = InitialSetupSerializer(data=request.data)

        if not initial_setup_serializer.is_valid():
            return Response(initial_setup_serializer.errors, status=status.HTTP_409_CONFLICT)

        # try:
        user = initial_setup_serializer.save(user=user)
        # except Exception:
        #     return Response("OOPS something went wrong :(", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(user, status=status.HTTP_201_CREATED)


class ASNList(APIView):
    def get(self, request):
        temporary_user = User.objects.first()
        monitored_asns = get_monitored_asns(temporary_user.id)
        monitored_asns = [monitored_asn.asn for monitored_asn in monitored_asns]
        # monitored_asns_serialized = AsnSerializer(monitored_asns, many=True)
        return Response(monitored_asns, status=status.HTTP_200_OK)
