from django.urls import path
from .views import EventListCreateAPI, EventRetriveUpdateAPIView, InviteeBulkCreateAPI, InviteeRetriveUpdateAPIView, InviteeListCreateListAPI


app_name = "events-api"

urlpatterns = [
    path("events/list", EventListCreateAPI.as_view(), name="event-list"),
    path("events/<int:pk>", EventRetriveUpdateAPIView.as_view(), name="event-detail"),
    
    path("events/<int:event_pk>/invitees/list", InviteeListCreateListAPI.as_view(), name="invitee-list"),
    path("events/<int:event_pk>/invitees/<int:pk>", InviteeRetriveUpdateAPIView.as_view(), name="invitee-detail"),
    path("events/<int:event_pk>/invitees/bulk-create", InviteeBulkCreateAPI.as_view(), name="invitee-detail"),
    
    path("scan/"),
    path("email/<int:event_pk>/all", email_to_all),
    path("email/<int:event_pk>/remaining", email_to_all),
]
