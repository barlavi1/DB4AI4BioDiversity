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
from . import views
#from . import views_camtraps 
#from . import views_polygon
#from .views_AddEvent import AddNewEvent

from .views_upload import views_AddEvent
#from . import view_test 
#from . import views_NewOccurence 
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
#from .views_test import render_my_view, handle_post_request 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.static import serve
#from .views_query.view_map import display_map
#from .views_polygon import map_view
from .views_query import views_polygon
from .views_query import views_QueryOccurence
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView,
    )

router = routers.DefaultRouter()
router.register(r'event', views.EventViewSet)
#router.register(r'Media', views_camtraps.Media_VIEW, basename='experiments')
#router.register(r'Zooniverse', views_camtraps.Zooniverse, basename='experiments1')
router.register(r'QueryByPolygon', views_polygon.QueryByPolygon, basename='QueryByPolygon')
#router.register(r'QueryByPolygonV2', views_polygon.QueryByPolygonV2, basename='QueryByPolygonV2')
router.register(r'add-new-image-with-exif', views_AddEvent.AddNewImageWithExif, basename = 'add-new-image-with-exif')
router.register(r'Zooniverse',views_QueryOccurence.Zooniverse, basename = "Zooniverse")

#router.register(r'AddOccurence', views.AddOccurenceViewSet, basename='home1234')
#router.register(r'AddOccurenceFromVideo' , views_NewOccurence.AddOccurenceFromVideoViewSet, basename = 'home12345')
#router.register(r'AddVideo', views_NewOccurence.AddVideoViewSet, basename = 'home123456')
#router.register(r'ViewPoly', views_polygon.QueryByPolygon, basename = 'home1234567')
#router.register(r'ViewMap', view_map.display_map, basename = 'home12345678')

#router.register(r'Upload-Image-With-Data', AddNewEvent.UploadImageWithData, basename='Upload-Image-With-Data')
#router.register(r'Upload-Image-With-Exif', AddNewEvent.UploadImageWithExif, basename='Upload-Image-With-Exif')
#router.register(r'Upload-Video-With-Data', AddNewEvent.UploadVideoWithData, basename='Upload-Video-With-Data')
#router.register(r'Upload-Video-With-Exif', AddNewEvent.UploadVideoWithExif, basename='Upload-Video-With-Exif')







#path('auth/', include('auth.urls')),


urlpatterns = [
        path('api/', include(router.urls)),
        path('admin/', admin.site.urls),
        path('auth/', include('auth.urls')),#  'auth.urls')),
        #path('api/'+'<int:question_id>', views.success, name = 'success'),
        re_path(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        #path('api/map/', display_map, name='map'),
        #path('api/Upload-Image-With-Data/', AddNewEvent.UploadImageWithData, name='Upload-Image-With-Data'),
        #path('api/Upload-Image-With-Exif/', AddNewEvent.UploadImageWithExif, name='Upload-Image-With-Exif'),
        #path('api/Upload-Video-With-Data/', AddNewEvent.UploadVideoWithData, name='Upload-Video-With-Data'),
        #path('api/Upload-Video-With-Exif/', AddNewEvent.UploadVideoWithExif, name='Upload-Video-With-Exif'),
        #path('api/map-display/', map_view, name='map-dispay'),
        #path('api/query-by-polygon/', query_by_polygon, name='query-by-polygon'),
        #path('api/render_my_view/', render_my_view, name='render_my_view'),
        #path('api/handle_post_request/', handle_post_request, name='handle_post_request'),
       # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
#+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpateerns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#tatic(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
