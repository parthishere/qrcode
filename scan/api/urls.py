from django.urls import path
from .views import scan


app_name = "scan-api"

urlpatterns = [
    path("scan/<int:event_pk>", scan),
]
