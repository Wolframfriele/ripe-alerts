from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertConfiguration, RipeUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AlertConfigurationSerializer, UserSerializer, RegistrationSerializer, TokenNotValid
from .ripe_api import get_anchors_probes_with_token, search_probes


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


class AlertConfigurationList(generics.ListCreateAPIView):
    """List of alert configurations"""
    # queryset = AlertConfiguration.objects.all()
    # print("test")
    serializer_class = AlertConfigurationSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            print(user.ripe_api_token.ripe_api_token)
        except ObjectDoesNotExist:
            print("has no ripe token")
        print('test')
        return AlertConfiguration.objects.all()


class AlertConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    """A single instance of AlertConfiguration"""
    queryset = AlertConfiguration.objects.all()
    serializer_class = AlertConfigurationSerializer


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
                
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class UserDetail(APIView):
    """Returns user specific information of authenticated user"""

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


"""
Ripe ATLAS API interaction
"""


class MyAtlasProbes(APIView):
    """
    Get all probes and anchors owned by the user from Ripe Atlas
    """

    def get(self, request):
        if request.user.ripe_api_token.ripe_api_token:
            return Response(get_anchors_probes_with_token(request.user.ripe_api_token))
        else:
            return Response({"error": "No api token set"}, status.HTTP_400_BAD_REQUEST)


class AtlasSearchProbes(APIView):
    """
    Search for probes in ripe atlas, search can be done on the following fields: "ASN", "Probe_id", "host" "prefix"
    """
    valid_filters = ['asn', 'probe_id', 'host',     'prefix']

    def get(self, request):

        filter: str = request.query_params.get('filter')
        value: str = request.query_params.get('value', '')
        if filter not in AtlasSearchProbes.valid_filters:
            return Response({"error": "invalid filter, you can filter on asn, probe_id, prefix or host"},
                            status.HTTP_400_BAD_REQUEST)
        if filter == "probe_id" and value.isnumeric() is False:
            return Response({"error": "invalid probe_id"}, status.HTTP_400_BAD_REQUEST)
        try:
            probes = search_probes(filter, value)
        except ValueError:
            return Response({"error": f"invalid {filter}"}, status.HTTP_400_BAD_REQUEST)
        return Response(probes, status.HTTP_200_OK)

