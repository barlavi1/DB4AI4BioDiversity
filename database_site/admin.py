from django.contrib import admin


# Register your models here.



#from .models import Taxon,Ai,Lifestage,Sex,Tasks,Annotators,Deployments,Event,Media,Observation,Location,Occurence,Behavior,Grades
from .models import *
admin.site.register(Taxon)
admin.site.register(Ai)
admin.site.register(Lifestage)
admin.site.register(Sex)
admin.site.register(Tasks)
admin.site.register(Annotators)
admin.site.register(Deployments)
admin.site.register(Event)
#admin.site.register(Media)
admin.site.register(Location)
admin.site.register(Occurence)
#admin.site.register(Observation)
admin.site.register(Behavior)
admin.site.register(Grades)
#admin.site.register(Continent)
#admin.site.register(Country)
#admin.site.register(County)
#admin.site.register(Region)

