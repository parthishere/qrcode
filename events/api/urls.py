from django.urls import path
from .views import EventListCreateAPI, EventRetriveUpdateAPIView, InviteeBulkCreateAPI, InviteeRetriveUpdateAPIView, InviteeListCreateListAPI, send_email_to_all, send_email_to_remaining, scan


app_name = "events-api"

urlpatterns = [
    path("events/list", EventListCreateAPI.as_view(), name="event-list"),
    path("events/<int:pk>", EventRetriveUpdateAPIView.as_view(), name="event-detail"),
    
    path("events/<int:event_pk>/invitees/list", InviteeListCreateListAPI.as_view(), name="invitee-list"),
    path("events/<int:event_pk>/invitees/<int:pk>", InviteeRetriveUpdateAPIView.as_view(), name="invitee-detail"),
    path("events/<int:event_pk>/invitees/bulk-create", InviteeBulkCreateAPI.as_view(), name="invitee-detail"),
    
    path("scan/<int:event_pk>", scan),
    path("email/<int:event_pk>/all", send_email_to_all),
    path("email/<int:event_pk>/remaining", send_email_to_remaining),
]
