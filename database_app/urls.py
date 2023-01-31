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
#from . import views

from .views_upload import views_AddEvent
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.static import serve
from .views_query import views_polygon, views_QueryOccurence
#from rest_framework_simplejwt.views import (
#        TokenObtainPairView,
#        TokenRefreshView,
#        TokenVerifyView,
#    )

from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import views_all
router = DefaultRouter()

#router = SimpleRouter()
#router.register(r'event', views.EventViewSet)
router.register(r'QueryByPolygon', views_polygon.QueryByPolygon, basename='QueryByPolygon')
router.register(r'add-new-image-with-exif', views_AddEvent.AddNewImageWithExif, basename = 'add-new-image-with-exif')
router.register(r'add-new-video', views_AddEvent.UploadVideoWithExif, basename = 'add-new-video')
router.register(r'Zooniverse',views_QueryOccurence.Zooniverse, basename = "Zooniverse")





router.register(r'Sexes', views_all.SexViewSet , basename = "Sex")
router.register(r'Taxa', views_all.TaxonViewSet , basename = "Taxon")
router.register(r'Behaviors', views_all.BehaviorViewSet , basename = "Behavior")
router.register(r'Life-stages', views_all.LifestageViewSet , basename = "Life-stage")
router.register(r'Events', views_all.EventViewSet , basename = "Event")
router.register(r'Images', views_all.ImageViewSet , basename = "Image")
router.register(r'Occurrences', views_all.OccurrenceViewSet , basename = "Occurrence")
router.register(r'Sequences', views_all.SequenceViewSet , basename = "Sequence")
router.register(r'Videos', views_all.VideoViewSet , basename = "Video")
router.register(r'Deployment', views_all.DeploymentViewSet , basename = "Deployment")
router.register(r'Locations', views_all.LocationViewSet , basename = "Location")
router.register(r'Counties', views_all.CountyViewSet , basename = "County")
#router.register(r'Regions', views_all.RegionViewSet , basename = "Regions")
#path('<str:pk>', NoteDetail.as_view())


#path('<str:pk>', NoteDetail.as_view())
urlpatterns = [
        path('api/', include(router.urls)),
        path('admin/', admin.site.urls),
        path('auth/', include('auth.urls')),#  'auth.urls')),
        re_path(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
