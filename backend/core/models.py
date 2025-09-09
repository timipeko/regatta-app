
from django.db import models
from django.contrib.auth.models import User

class SailingClub(models.Model):
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=2, default="FI")
    def __str__(self): return self.name

class BoatClass(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    default_handicaps = models.JSONField(default=dict, blank=True)
    def __str__(self): return self.name

class Boat(models.Model):
    name = models.CharField(max_length=120)
    sail_number = models.CharField(max_length=50, unique=True)
    boat_class = models.ForeignKey(BoatClass, on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey(SailingClub, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    handicap_values = models.JSONField(default=dict, blank=True)
    def __str__(self): return f"{self.name} ({self.sail_number})"

class Regatta(models.Model):
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

class RegattaClass(models.Model):
    regatta = models.ForeignKey(Regatta, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=120)
    handicap_system = models.CharField(max_length=40, default="FinRating")
    scoring_system = models.CharField(max_length=40, default="WS_APP_A")
    allow_self_service = models.BooleanField(default=True)

class Race(models.Model):
    regatta_class = models.ForeignKey(RegattaClass, on_delete=models.CASCADE, related_name="races")
    date = models.DateField()
    sequence = models.PositiveIntegerField(default=1)

class Entry(models.Model):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    STATUS_CHOICES = [(APPROVED,"approved"),(PENDING,"pending"),(REJECTED,"rejected")]
    regatta_class = models.ForeignKey(RegattaClass, on_delete=models.CASCADE, related_name="entries")
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    helm = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=APPROVED)

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results")
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="results")
    elapsed_seconds = models.PositiveIntegerField(null=True, blank=True)
    corrected_seconds = models.PositiveIntegerField(null=True, blank=True)
    points = models.FloatField(null=True, blank=True)
    rank = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=16, default="OK")

    class Meta:
        unique_together = ("race", "entry")
