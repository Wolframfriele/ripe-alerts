from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer
from ripe_atlas.exceptions import TokenNotValid
from ripe_atlas.serializers import MeasurementSerializer, ProbeSerializer
from .models import RipeUser
from ripe_atlas.models import Measurement, Target
from alert_configuration.models import AlertConfiguration


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
        # user_serializer = UserSerializer(request.user)
        user_information = {"username": request.user.username,
                            "ripe_api_token": request.user.ripe_user.ripe_api_token,
                            "initial_setup_complete": request.user.ripe_user.initial_setup_complete}
        return Response(user_information)


class InitialSetup(APIView):
    """De probes en anchors van gebruiker met de bijbehorende measurements die geschikt zijn om te alerten worden
    automatisch uit ripe atlas opgehaald met behulp van de ripe-api-token .
    Dus volgens het AI plan zijn dat voor nu alleen de Ping measurements.
    De gebruiker kan zelf nog probes en anchors zoeken om toe te voegen, de relevante measurements worden ook door de
    backend  opgehaald.  gebruiker kiest de measurements uit waar alert op moet komen.
    Daarna invullen van email
    Akkoord met legal
    """

    def post(self, request):
        # key probe_measurement: lijst van json objecten binnen met daarin probe informatie, de measurement informatie van de probe
        # key email: is email waar alerts naar gestuurd moet worden
        # als alles correct opgeslagen is dan begint AI proces.

        if request.user.ripe_user.initial_setup_complete:
            return Response({"message": "user has already completed the initial setup!"}, status=status.HTTP_403_FORBIDDEN)

        #validate data:

        data: dict = request.data

        if 'email' not in data.keys():
            return Response({"error": "email is required"}, status=status.HTTP_409_CONFLICT)
        if 'probe_measurements' not in data.keys():
            return Response({"error": "probe_measurements field is missing"}, status=status.HTTP_409_CONFLICT)

        probe_measurements = data.get("probe_measurements")
        email = data.get("email")

        if not isinstance(probe_measurements, list):
            return Response({"error": "probe_measurements needs to be a list"}, status=status.HTTP_409_CONFLICT)
        if not isinstance(email, str):
            return Response({"error": "email needs to be a string"}, status=status.HTTP_409_CONFLICT)
        if len(probe_measurements) == 0:
            return Response({"error": "no probe measurements objects provided"}, status=status.HTTP_409_CONFLICT)

        for probe_measurement in probe_measurements:
            # check if probe_measurement object is a dict
            if not isinstance(probe_measurement, dict):
                return Response({"error": "probe_measurement needs to be a dict"}, status=status.HTTP_409_CONFLICT)

            # check if probe and measurement keys are provided
            if 'probe' not in probe_measurement.keys():
                return Response({"error": "probe field is required"}, status=status.HTTP_409_CONFLICT)
            if 'measurements' not in probe_measurement.keys():
                return Response({"error": "measurements field is required"}, status=status.HTTP_409_CONFLICT)

            # check if probe is valid
            probe_serializer = ProbeSerializer(data=probe_measurement['probe'])
            if not probe_serializer.is_valid():
                return Response(probe_serializer.errors, status=status.HTTP_409_CONFLICT)

            # check if measurements is valid
            if not isinstance(probe_measurement['measurements'], list):
                Response({"error": "measurements needs to be a list"}, status=status.HTTP_409_CONFLICT)

            if len(probe_measurement['measurements']) == 0:
                return Response({"error": "no measurements objects provided"}, status=status.HTTP_409_CONFLICT)

            measurements_serializer = MeasurementSerializer(data=probe_measurement['measurements'], many=True)
            if not measurements_serializer.is_valid():
                return Response(measurements_serializer.errors, status=status.HTTP_409_CONFLICT)

            # store measurements and probe if they do not exist in the database
            target = Target.objects.get_or_create(**probe_serializer.validated_data)[0]
            for measurement in measurements_serializer.validated_data:
                try:
                    measurement = Measurement.objects.get_or_create(**measurement, target=target)[0]
                except IntegrityError:
                    return Response({"error": "measurement already exists"}, status=status.HTTP_409_CONFLICT)

                # create a new alert configuration record voor nu nep alert configuratie
                print(f"storing alert configuration for measurment: {measurement.measurement_id} ")
                alert_config = {"max_packet_loss": 75}
                AlertConfiguration.objects.get_or_create(user=request.user,
                                                                  measurement=measurement,
                                                                  alert_configuration_type=measurement.type,
                                                                  alert_configuration=alert_config)
            # store the email
            print("storing the email")

            # set initial_setup_complete to true.
            ripe_user = RipeUser.objects.filter(user=request.user)
            ripe_user.update(initial_setup_complete=True)
            user_information = {"username": request.user.username,
                                "ripe_api_token": request.user.ripe_user.ripe_api_token,
                                "initial_setup_complete": request.user.ripe_user.initial_setup_complete}

        return Response(user_information, status=status.HTTP_201_CREATED)


class SystemList(APIView):
    def get(self, request):
        """returns all systems that the user has an alert on, systems is categorized by """
        pass