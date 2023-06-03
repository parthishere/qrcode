from django.urls import path
from .views import  InviteeBulkCreateAPI, InviteeRetriveUpdateAPIView, InviteeListCreateListAPI


app_name = "invitee-api"

urlpatterns = [
    path("events/<int:event_pk>/invitees/list", InviteeListCreateListAPI.as_view(), name="invitee-list-create"),
    path("events/<int:event_pk>/invitees/<int:pk>", InviteeRetriveUpdateAPIView.as_view(), name="invitee-rud"),
    path("events/<int:event_pk>/invitees/bulk-create", InviteeBulkCreateAPI.as_view(), name="invitee-bulk-create"),
]