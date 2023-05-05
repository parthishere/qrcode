from django.urls import path
from .views import qrscan, send_email, cam_feed, pati_gayela, bachya_khutya, home


app_name = "passtemplates"

urlpatterns = [
    path("<int:pk>/update-pass-template-for-all-invitee/", update_pass_template_for_all_invitee, name="update-pass"),
    path('<int:pk>/send-pass-on-email/', send_pass_on_email_event, name='send-pass'),
    path("<int:pk>/set-predefined-pass-template/", set_predefined_pass_template, name="predefined-pass")
]