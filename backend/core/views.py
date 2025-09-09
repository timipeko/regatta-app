
from rest_framework import viewsets, decorators, response
from .models import *
from .serializers import *

class RegattaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Regatta.objects.all().order_by("-start_date")
    serializer_class = RegattaSerializer

    @decorators.action(detail=True, methods=["get"])
    def classes(self, request, pk=None):
        items = RegattaClass.objects.filter(regatta_id=pk).order_by("name")
        return response.Response(RegattaClassSerializer(items, many=True).data)

class RegattaClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegattaClass.objects.all()
    serializer_class = RegattaClassSerializer

    @decorators.action(detail=True, methods=["get"])
    def races(self, request, pk=None):
        items = Race.objects.filter(regatta_class_id=pk).order_by("sequence")
        return response.Response(RaceSerializer(items, many=True).data)

    @decorators.action(detail=True, methods=["get"])
    def standings(self, request, pk=None):
        entries = Entry.objects.filter(regatta_class_id=pk).select_related("boat")
        rows = []
        for e in entries:
            rr = RaceResult.objects.filter(entry=e)
            total = sum([r.points or 0 for r in rr])
            ranks = [r.rank for r in rr if r.rank]
            rows.append({
                "entry_id": e.id,
                "boat": {"name": e.boat.name, "sail_number": e.boat.sail_number},
                "total_points": total,
                "ranks": ranks,
            })
        rows.sort(key=lambda x: x["total_points"])
        return response.Response(rows)

class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

    @decorators.action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        items = RaceResult.objects.filter(race_id=pk).select_related("entry__boat").order_by("rank","id")
        return response.Response(RaceResultSerializer(items, many=True).data)
