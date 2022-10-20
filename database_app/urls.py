"""database_app URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView,
    )


router = routers.DefaultRouter()
router.register(r'taxon', views.TaxonViewSet)
router.register(r'ai', views.AiViewSet)
router.register(r'behavior', views.BehaviorViewSet)
router.register(r'lifestage', views.LifestageViewSet)
router.register(r'sex', views.SexViewSet)
router.register(r'tasks', views.TasksViewSet)
router.register(r'annotators', views.AnnotatorsViewSet)
router.register(r'deployments', views.DeploymentsViewSet)
router.register(r'grades', views.GradesViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'media', views.MediaViewSet)
router.register(r'observation', views.ObservationViewSet)
router.register(r'occurence', views.OccurenceViewSet)
router.register(r'location', views.LocationViewSet)
#router.register(r'FilterByChoice', views.GetImg)

urlpatterns = [
        path('', include(router.urls)),
        path('admin/', admin.site.urls),
        #path('api-auth/', include('rest_framework.urls',namespace='rest_framework')
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
#        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

