
from .models_helpTables import Location
from django.http import JsonResponse


def get_locations(request):
    locations = Location.objects.values('locationid')
    data = {
        'locationids' : list(locations)
    }
    return JsonResponse(data)
