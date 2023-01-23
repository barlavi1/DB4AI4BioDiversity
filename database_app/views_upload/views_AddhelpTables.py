from database_site.models import *
#from database_site.functions import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
import sys
import pytz
utc=pytz.UTC
from rest_framework.response import Response
import ast
from shapely.geometry import Polygon

class CountyViewSet(viewsets.ViewSet):
	permission_classes = [permissions.IsAuthenticated]

    def create(self,request):
        data = ast.literal_eval(request.body.decode())
        countyPolygon = Polygon(data["polygon"]).wkt
        countyname = data['name']
        newCounty = County(countyname = countyname, countyPolygon = countyPolygon)
        newCounty.save()

class RegionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self,request):
        data = ast.literal_eval(request.body.decode())
        regionPolygon = Polygon(data["polygon"]).wkt
        regionname = data['name']
        county = County.objects.get(countyPolygon__contain = regionPolygon)
        if not county:
            county = County.objects.get(countyname = "unknown")
        newRegion = Region(regionname = regionname, regionPolygon = regionPolygon, county = county)
        newRegion.save()


class LocationViewSet(viewsets.ViewSet):
    """
    table for location of deployments
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self,request):
        decimallongtitude = request.data['lon']
        decimallatitude  = request.data['lat']
        coordinateuncertaintyinmeters = request.data['coordinate_uncertainty'] if 'coordinate_uncertainty' in request.data else 0
        location_coords = Point(float(self.decimallongtitude) , float(self.decimallatitude))
        region = Region.objects.get( regionPolygon__contain = location_coords )
        if not region:
            region = Region.objects.get( regionname = "unknown" )
         county = County.objects.get(countyPolygon__contain = location_coords)
        if not county:
            county = County.objects.get(countyname = "unknown")
        locationname = request.data['name'] in 'name' in request.data else "unknown"
        newLocation = Location( decimallongtitude  = decimallongtitude, decimallatitude = decimallatitude, coordinateuncertaintyinmeters = coordinateuncertaintyinmeters, region = region, county = county, locationname = locationname )
        newLocation.save()
        

class TaxonViewSet(viewsets.ViewSet):
    """
    table for different taxons
    """
    permission_classes = [permissions.IsAuthenticated]
    def create(self,request):
        taxonid = request.data['taxonid']
        scientificname = request.data['scientific_name']
        genericname = request.data['generic_name']
        newTaxon = Taxon( taxonid = taxonid, scientificname = scientificname, genericname = genericname)
        newTaxon.save()

class BehaviorViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    """
    behavior of occurence
    """
    def create(self,request):
        behaviortype = request.data['behavior']
        newBehavior= Behavior( behaviortype = behaviortype)
        newBehavior.save()

class LifestageViewSet(viewsets.ViewSet):
    """
    life stage of occurence
    """
    def create(self,request):
        lifestagetype = request.data['life_stage']
        newLifestage = Lifestage( lifestagetype = lifestagetype )
        newLifestage =.save()










