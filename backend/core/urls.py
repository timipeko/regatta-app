
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register("regattas", RegattaViewSet, basename="regattas")
router.register("regatta-classes", RegattaClassViewSet, basename="regatta-classes")
router.register("races", RaceViewSet, basename="races")

urlpatterns = [ path("", include(router.urls)) ]
