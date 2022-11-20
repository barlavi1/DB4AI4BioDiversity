from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from .Objects import *
from database_site.models import *



class TestLoc(viewsets.ViewSet):
    def list(self, request):
        queryset = Location.objects.all()
        return response({'queryset': queryset})
