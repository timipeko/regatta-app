
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date
from core.models import *

class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        u,_ = User.objects.get_or_create(username="admin", defaults={"email":"admin@example.com"})
        if not u.has_usable_password():
            u.set_password("Admin!234"); u.save()
        club,_ = SailingClub.objects.get_or_create(name="HSS", short_name="HSS")
        bc,_ = BoatClass.objects.get_or_create(code="HBOAT", defaults={"name":"H-Boat","default_handicaps":{"FinRating":950}})

        reg,_ = Regatta.objects.get_or_create(name="Demo Regatta", defaults={"venue":"Helsinki","start_date":date.today(),"end_date":date.today()})
        rc,_ = RegattaClass.objects.get_or_create(regatta=reg, name="Fleet A", defaults={"handicap_system":"FinRating","scoring_system":"WS_APP_A","allow_self_service":True})
        r1,_ = Race.objects.get_or_create(regatta_class=rc, date=date.today(), sequence=1)
        r2,_ = Race.objects.get_or_create(regatta_class=rc, date=date.today(), sequence=2)

        b1,_ = Boat.objects.get_or_create(sail_number="FIN-123", defaults={"name":"Merituuli","boat_class":bc,"club":club})
        b2,_ = Boat.objects.get_or_create(sail_number="FIN-456", defaults={"name":"Tuulikki","boat_class":bc,"club":club})

        e1,_ = Entry.objects.get_or_create(regatta_class=rc, boat=b1, defaults={"helm":u,"status":"approved"})
        e2,_ = Entry.objects.get_or_create(regatta_class=rc, boat=b2, defaults={"helm":u,"status":"approved"})

        RaceResult.objects.get_or_create(race=r1, entry=e1, defaults={"elapsed_seconds":4354,"corrected_seconds":4354,"points":1,"rank":1})
        RaceResult.objects.get_or_create(race=r1, entry=e2, defaults={"elapsed_seconds":4440,"corrected_seconds":4440,"points":2,"rank":2})
        RaceResult.objects.get_or_create(race=r2, entry=e1, defaults={"elapsed_seconds":4200,"corrected_seconds":4200,"points":1,"rank":1})

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
