from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView, Response, status ,Request

from users.models import User
from users.permissions import IsAdmin, IsUserOwner
from users.serializer import (DetailUserSerializer, LoginSerializer,UserSerializer,UpdateStatusSerializer)

class ListCreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListNewestUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = DetailUserSerializer

    def get_queryset(self):

        num = self.kwargs['num']

        return self.queryset.order_by('-date_joined')[0:num]

class UpdateUserDetailsView(generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUserStatusView(generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_update(self, serializer):
        for key, value in self.request.data.items():
            if key =='is_active':
                return serializer.save(is_active= value)

class LoginView(APIView):
    queryset = User
    serializer_class = UserSerializer
    
    def post(self, request:Request)->Response:
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({"detail": 'invalid username or password'}, status.HTTP_401_UNAUTHORIZED)


        token = Token.objects.get_or_create(user=user)[0]
        return Response({'token': token.key})