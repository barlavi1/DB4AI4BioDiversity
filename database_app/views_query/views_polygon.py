from django.http import HttpResponse
from rest_framework import viewsets
from ..Objects import *
from database_site.models import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import sys
from shapely.geometry import Polygon
import ast, numpy as np
import collections
from rest_framework.response import Response
import json
from itertools import chain

class QueryByPolygon(viewsets.ViewSet):
    def list(self, request):
        #data = request.body.decode()
        data = ast.literal_eval(request.body.decode())
        poly = Polygon(data["polygon"]).wkt
        queryset = Occurence.objects.filter(eventid__locationid__location_coords__within = poly)
        Animals = list(queryset.values_list('taxonid__genericname','individualcount'))
        AnimalsCount = collections.defaultdict(int)
        for k, v in Animals:
            AnimalsCount[k]+=v
        #AnimalsCount = json.loads(json.dumps(str(dict( AnimalsCount))))
        return  Response(dict(AnimalsCount))
#"""
#class QueryByPolygonV2(viewsets.ViewSet):
#    """
#    #create histogram for query by polygon 
#    #"""
#    def list(self, request):
#        data = request.body.decode()
#        data = ast.literal_eval(data)
#        poly = Polygon(data["polygon"]).wkt
#        queryset = Occurence.objects.filter(eventid__deploymentid__locationid__location_coords__within = poly)
#        Animals = [Taxon.objects.get(taxonid = query.taxonid.taxonid).genericname for query in queryset]
#        Counts =  list(queryset.values_list('individualcount', flat = True))
#        AnimalsCount = list(chain.from_iterable([x] * y for x, y in zip(Animals, Counts)))
#        AnimalsCount = json.loads(json.dumps(collections.Counter(AnimalsCount)))
#        return Response(AnimalsCount)
#        #ax.set_ylabel('Count')
#        
#        #response = HttpResponse(content_type='image/png')
#        
#        #canvas = FigureCanvasAgg(fig)
#        #canvas.print_png(response)
#        
#        #return Response({'Species' : species, "Count" : counts)


#class TestLoc(viewsets.ViewSet):
#    def list(self, request):
#
#        queryset = Location.objects.all()
#        print(queryset[0].point_field)
#        return Response({'queryset': queryset})
#"""
