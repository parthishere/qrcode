from events.models import Event
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


from django.conf import settings
from django.template.loader import render_to_string

from django.core.mail import EmailMessage

from .tasks import send_email_to_all, send_email_to_remaining

# Create your views here.
def qrscan(request, pk=None):
    context = {}
    user= request.user
    event_instance = Event.objects.exclude(removed=True).get(pk=pk, created_by=user)
    context['event_id'] = event_instance.pk
    return render(request, 'app/qrscan.html', context)

def home(request):
    return render(request, 'app/home.html', {})

def send_email_to_event(request, pk):
   
    send_email_to_all(None, request, pk)
    return render(request, "app/will_send_email_in_background.html", {"pk":pk})

def send_email_to_remaining_event(request, pk):
    send_email_to_remaining(None, request, pk)
    return render(request, "app/will_send_email_in_background.html", {"pk":pk})
        
        
def send_email(request, pk=None):
    # user = request.user
    # event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=pk, created_by=user)
    
    # invitees = event_instance.invitees.all()
    # # print(participant)
    
    # for invitee in invitees :
    #     if invitee.qr_code:
    #         template = render_to_string('app/email_template.html', {'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "organization_or_college":event_instance.organization_or_college})
    #         invitee.sent_email = True
    #         invitee.save()
    #         subject = "Initation for: " + event_instance.event_name
    #         message = template
    #         email_from = settings.EMAIL_HOST_USER
    #         recipient_list = [invitee.email,]
    #         mail = EmailMessage(subject, message, email_from, recipient_list)
    #         mail.attach(invitee.qr_code.name, invitee.qr_code.read())
    #         mail.send()
    #     else:
    #         return redirect(reverse("app:make-qr", kwargs={"pk":pk}))

    return render(request, 'app/sent.html', {"pk":pk})


def make_qr_code_all_event(request, pk=None):
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=pk, created_by=user)
    
    invitees = [i for i in event_instance.invitees.all()]
    for invitee in invitees:
        invitee.save()
    return redirect(reverse("events:detail", kwargs={"pk":pk}))

# def pati_gayela(request):
#     context = {}
#     context['objects_list'] = PassModel.objects.filter(recognized=True)
#     print(context)
#     return render(request, 'app/pati_gayela.html', context)

# def bachya_khutya(request):
#     context = {}
#     context['objects_list'] = PassModel.objects.filter(recognized=False)
#     return render(request, 'app/bachya_khutya.html', context)



def gen(camera):
    run = True
    while run:
        data, frame = camera.get_frame()
        # name, email, phone_number = data.split(',')[0], data.split(',')[1], data.split(',')[2]
        
        if data:
            run = False
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

	
def cam_feed(request):
    return StreamingHttpResponse(gen(QrRecognize()),
                    content_type='multipart/x-mixed-replace; boundary=frame') 