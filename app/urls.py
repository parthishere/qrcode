from django.urls import path
from .views import qrscan, send_email, cam_feed, home, make_qr_code_all_event, send_email_to_event, send_email_to_remaining_event
from events.views import list_event

app_name = "app"

urlpatterns = [
    path('', list_event, name='event-home'),
    path('scan/<int:pk>', qrscan, name='scan'),
    path('email/<int:pk>', send_email, name='send-email'),
    path("email/<int:pk>/send", send_email_to_event, name="send_email_to"),
    path("email/<int:pk>/send-to-remaining", send_email_to_remaining_event, name="send_email_to_remaining"),
    path("make/qr/<int:pk>", make_qr_code_all_event, name="make-qr"),
    # path('stream', cam_feed, name='stream'),
    # path('completed', pati_gayela, name='complete'),
    # path('send-email', send_email, name='email'), 
    # path('remaining', bachya_khutya, name='remaining'),
]