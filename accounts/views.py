from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from accounts.exceptions import (
    AlreadyRegisteredEmailError,
    AlreadyRegisteredUsernameError,
)
from accounts.models import AccountModel
from accounts.permissions import (
    RetrieveUpdateOneAuthenticatePermission,
    RetrieveUpdateOneAuthorizePermission,
)
from accounts.serializers import LoginSerializer, RetrieveUpdateOneSerializer


@api_view(http_method_names=("POST",))
def login(request):

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )

    if not user:
        return Response({"detail": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status.HTTP_200_OK)


class RetrieveUpdateOneView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        RetrieveUpdateOneAuthenticatePermission,
        RetrieveUpdateOneAuthorizePermission,
    ]
    serializer_class = RetrieveUpdateOneSerializer
    queryset = AccountModel.objects.all()
    lookup_url_kwarg = "user_id"

    def patch(self, request, *args, **kwargs):

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
