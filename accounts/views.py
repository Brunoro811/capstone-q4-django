from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import (GenericAPIView, ListCreateAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response

from accounts.models import AccountModel
from accounts.permissions import IsAuthenticatedAccounts
from accounts.serializers import AccountSerializer, LoginSerializer


class LoginPostView(GenericAPIView):
    
    serializer_class = LoginSerializer
    queryset = AccountModel.objects
    
    
    def post(self, request, *args, **kwargs):
        """
            Usuario faz login
            
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response({'detail': "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key},status.HTTP_200_OK)


class AccountsListCreateUpdateAPIView(ListCreateAPIView,UpdateAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAccounts]

    serializer_class = AccountSerializer
    queryset = AccountModel.objects

    def patch(self, request, *args, **kwargs):
        
        self.kwargs.setdefault('pk', request.user.id)   
        return super().patch(request, *args, **kwargs)


