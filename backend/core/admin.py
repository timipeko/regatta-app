
from django.contrib import admin
from .models import *
admin.site.register([SailingClub, BoatClass, Boat, Regatta, RegattaClass, Race, Entry, RaceResult])
