from django.shortcuts import render
from database_site.models import *
from django.contrib.gis.geos import Polygon, Point, GEOSGeometry
from rest_framework import viewsets




def display_map(request):
    # Get all occurrences from the database
    occurrences = Occurence.objects.all()
    #Events = Event.objects.all()

    #Create a list to store the coordinates of the occurrences
    coordinates = []

    # Iterate through the occurrences and get the latitude and longitude of each one
    for occurence in occurrences:
        lat = occurence.eventid.locationid.decimallatitude
        lng = occurence.eventid.locationid.decimallongtitude
        coordinates.append((lat, lng))

    # Pass the coordinates to the template
    context = {'coordinates': coordinates}
    return render(request, 'map.html', context)

