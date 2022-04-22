from django.urls import path
from .views import qrscan, send_email, cam_feed, pati_gayela, bachya_khutya


app_name = "app"

urlpatterns = [
    path('scan', qrscan, name='scan'),
    path('email', send_email, name='send-email'),
    path('stream', cam_feed, name='stream'),
    path('completed', pati_gayela, name='complete'),
    path('send-email', send_email, name='email'), 
    path('remaining', bachya_khutya, name='remaining'),
]