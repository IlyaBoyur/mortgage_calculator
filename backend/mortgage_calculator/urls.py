from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("offer", views.MortgageOfferViewSet, basename='offer')


urlpatterns = [
    path('', include(router.urls)),
]
