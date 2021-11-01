from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import query
from rest_framework import generics, request, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.models import AlertConfiguration, RipeUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from.serializers import AlertConfigurationSerializer, UserSerializer, RegistrationSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class AlertConfigurationList(generics.ListCreateAPIView):
    # queryset = AlertConfiguration.objects.all()
    # print("test")
    serializer_class = AlertConfigurationSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            print(user.ripeuser.ripe_api_token)
        except ObjectDoesNotExist:
            print("has no ripe token")
        print('test')
        return AlertConfiguration.objects.all()


class AlertConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlertConfiguration.objects.all()
    serializer_class = AlertConfigurationSerializer

class RegistrationService(APIView):

    permission_classes =[permissions.AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try: 
                new_user = serializer.save()
                return Response(get_tokens_for_user(new_user), status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'user with that username already exists'}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class UserDetail(APIView):
    # def get_object(self, user):
    #     try:
    #         return Snippet.objects.get(pk=pk)
    #     except Snippet.DoesNotExist:
    #         raise Http404

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


