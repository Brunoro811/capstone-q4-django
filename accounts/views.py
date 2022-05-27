from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.exceptions import UserAlreadyExistsException
from accounts.models import AccountModel
from accounts.permissions import IsAdmin, IsAuthenticatedAccounts
from accounts.serializers import AccountSerializer, LoginSerializer


class AccountsListCreateUpdateAPIView(ListCreateAPIView,UpdateAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAccounts, IsAdmin]

    serializer_class = AccountSerializer
    queryset = AccountModel.objects

    def is_valid_conflict(self,*args,**kwargs):
        restrict_fields = (kwargs)
        message_already_exists_error = []

        message_already_exists_error  = [ 
            {key:  ["user with this {} already exists.".format(key)] }
            for key,value in restrict_fields.items() 
                if self.queryset.filter(**{key:value}).first() 
        ]
        if message_already_exists_error:
            raise UserAlreadyExistsException(detail=message_already_exists_error[0])
        
        

    def patch(self, request, *args, **kwargs):
        
        self.kwargs.setdefault('pk', request.user.id)   
        return super().patch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        restrict_fields = ('username','email',)
        found_fields = [ {key: request.data[key]} for key,value in request.data.items() if key in restrict_fields ]

        self.is_valid_conflict(*found_fields)
        return super().create(request, *args, **kwargs)



class LoginPostView(APIView):
    
    def post(self, request, *args, **kwargs):
        """
            Usuario faz login
            
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response({'detail': "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key},status.HTTP_200_OK)
        