from django.urls import path, include
from auth.views import *
from rest_framework.routers import SimpleRouter
from auth.views import TokenRefreshView, TokenObtainPairView, LogoutView

router = SimpleRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
]
