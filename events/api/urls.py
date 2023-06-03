from django.urls import path
from .views import EventListCreateAPI, EventRetriveUpdateAPIView, send_email_to_all, send_email_to_remaining


app_name = "events-api"

urlpatterns = [
    path("list", EventListCreateAPI.as_view(), name="event-list"),
    path("<int:pk>", EventRetriveUpdateAPIView.as_view(), name="event-detail"),
     
    path("email/<int:event_pk>/all", send_email_to_all),
    path("email/<int:event_pk>/remaining", send_email_to_remaining),
]
