
from rest_framework import serializers
from .models import *

class BoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boat
        fields = ["id","name","sail_number","handicap_values","boat_class","club"]

class EntrySerializer(serializers.ModelSerializer):
    boat = BoatSerializer(read_only=True)
    class Meta:
        model = Entry
        fields = ["id","boat","status"]

class RaceResultSerializer(serializers.ModelSerializer):
    entry = EntrySerializer(read_only=True)
    class Meta:
        model = RaceResult
        fields = ["id","race","entry","elapsed_seconds","corrected_seconds","points","rank","status"]

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ["id","date","sequence"]

class RegattaClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegattaClass
        fields = ["id","name","handicap_system","scoring_system","allow_self_service"]

class RegattaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regatta
        fields = ["id","name","venue","start_date","end_date","description"]
