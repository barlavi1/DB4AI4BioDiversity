from .serializers import UserSerializer, TokenObtainPairWithData, TokenRefreshWithData
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.utils import aware_utcnow


# created a generic view set excluding the option to delete from db
class NoDeleteViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    pass


class LoginUpdateOnly(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    pass


# user ViewSet to allow edit user data on db, but disallow delete user from db
class UserViewSet(LoginUpdateOnly):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # allow a user to query only his data
    def get_queryset(self):
        return User.objects.all().filter(id=self.request.user.id)

    def get_permission(self):
        if self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairWithData


class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshWithData


# logout is enabled by blacklisting the refresh token currently in use at the user end
# it will be whitelisted as it is expired
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # delete expired tokens cascading to blacklisted
        OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()
        mismatch_id_refresh_access = False
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # check if the request access user id matches the refresh token user id
            if token.payload["user_id"] != self.request.user.id:
                mismatch_id_refresh_access = True
                raise Exception
            else:
                token.blacklist()
                return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            if mismatch_id_refresh_access:
                message = "there is a mismatch between access token user id and refresh token user id"
            else:
                message = f"{e}"
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": message})
