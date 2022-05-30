from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import (GenericAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.response import Response

from accounts.exceptions import (AlreadyRegisteredEmailError,
                                 AlreadyRegisteredUsernameError,
                                 UserAlreadyExistsException)
from accounts.models import AccountModel
from accounts.permissions import (IsAdmin, IsAuthenticatedAccounts,
                                  RetrieveUpdateOneAuthenticatePermission,
                                  RetrieveUpdateOneAuthorizePermission)
from accounts.serializers import (AccountSerializer, AccountUpdateSerializer,
                                  LoginSerializer, RetrieveUpdateOneSerializer)


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
    
    def put(self, request, *args, **kwargs):
        """
            # Method \"PUT\" not allowed.
        """
        self.serializer_class = AccountUpdateSerializer
        raise MethodNotAllowed(method="PUT")
        

    def patch(self, request, *args, **kwargs):
        """
            This route is authenticated.
            All fields are optional.
            Seller User can change : 'password', 'first_name' and 'last_name'.
            Admin user can change : 'email','username','password','is_seller', 'first_name', 'last_name' and 'store_id'.
        """
        
        self.serializer_class = AccountUpdateSerializer
        self.kwargs.setdefault('pk', request.user.id)   
        return super().patch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        
        # these fields are unique
        restrict_unique_fields = ('username','email',)
        dict_fields = {}
        
        [ dict_fields.setdefault(key, request.data[key]) for key,value in request.data.items() if key in restrict_unique_fields ]

        self.is_valid_conflict(**dict_fields)
        return super().create(request, *args, **kwargs)



class LoginPostView(GenericAPIView):

    serializer_class = LoginSerializer
    queryset = AccountModel.objects
    
    
    def post(self, request):
        """
            This route is for user login.
            The username and password fields are mandatory.
            This route returns a token if the credentials are valid and otherwise returns an error message. 
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response({'detail': "Invalid credentials."}, status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key},status.HTTP_200_OK)
       


class RetrieveUpdateOneView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        RetrieveUpdateOneAuthenticatePermission,
        RetrieveUpdateOneAuthorizePermission,
    ]
    serializer_class = RetrieveUpdateOneSerializer
    queryset = AccountModel.objects.all()
    lookup_url_kwarg = "user_id"

    def get(self, request, *args, **kwargs):

        """
            This route is authenticated.

            This route receives as a parameter a `user_id` of type UUID.
            
            This route returns the user or a not found message.
        """

        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
            # Method \"PUT\" not allowed.
        """
        self.serializer_class = AccountUpdateSerializer
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        """
            This route is authenticated.
            
            Only the admin user has access.
            
            This route receives as a parameter a `user_id` of type UUID.
            
            This route returns the user or a not found message.
            
            This route updates the user.
        """

        user_exists = self.get_queryset().filter(pk=kwargs["user_id"]).exists()

        if user_exists:
            email = (
                self.get_queryset()
                .exclude(pk=kwargs["user_id"])
                .filter(email__iexact=request.data["email"])
                .exists()
                if request.data.get("email")
                else False
            )

            if email:
                raise AlreadyRegisteredEmailError()

            username = (
                self.get_queryset()
                .exclude(pk=kwargs["user_id"])
                .filter(username__iexact=request.data["username"])
                .exists()
                if request.data.get("username")
                else False
            )

            if username:
                raise AlreadyRegisteredUsernameError()

        return super().patch(request, *args, **kwargs)

    def handle_exception(self, exc):
        return super().handle_exception(exc)

