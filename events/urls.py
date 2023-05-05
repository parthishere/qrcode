from django.urls import path
from .views import (
    delete_participant,
    list_event,
    create_event,
    detail_event,
    update_event,
    delete_event,
    delete_event_pass,
    add_participant,
    bulk_create,
    remove_all_participant,
    see_all_recognized_participant,
    see_all_unrecognized_participant
)


app_name = "events"

urlpatterns = [
    path('list/', list_event, name='list'),
    path('create/', create_event, name='create'),
    path("<int:pk>/", detail_event, name="detail"),
    path('<int:pk>/update/', update_event, name='update'),
    path("<int:pk>/delete/", delete_event, name='delete'),
    path("<int:pk>/delete-pass/", delete_event_pass, name='delete-pass'),
    path('<int:pk>/create-participant/', add_participant, name='add-participant'),
    path('<int:pk>/bulk-create-invitee/', bulk_create, name="add-bulk-participant"),
    path("<int:pk>/remove-invitees", remove_all_participant, name="remove-all"),
    path('<int:pk>/delete/<str:unique_id>', delete_participant, name="delete-participant"),
    path('<int:pk>/see-recognized-invitees/', see_all_recognized_participant, name="see-all-reconized-participant"),
    path('<int:pk>/see-unrecognized-invitees/', see_all_unrecognized_participant, name="see-all-unreconized-participant"),
    
    # path("remove-participant/<int:unique_id>/", remove_participant, name="remove-participant"),
    # path("recognized-inviees/", recognized_invitees, name="recognized-event"),
    # path("remaining-inviees/", remaining_invitees, name="recognized-event"),
]