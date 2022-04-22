from django.shortcuts import render
from django.http.response import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


from .recog import QrRecognize
from .models import PassModel

from django.conf import settings
from django.template.loader import render_to_string

from django.core.mail import EmailMessage

# Create your views here.
def qrscan(request):
    return render(request, 'app/qrscan.html', {})

def home(request):
    return render(request, 'app/index.html', {})

def send_email(request):
    participant = [e for e in PassModel.objects.all()]
    print(participant)
    for p in participant:
        template = render_to_string('app/email_template.html', {'name': p.name, 'email':p.email, 'phone_number':p.phone_number})
        print(p)
        subject = "Invitation for Farewell 2k22 !"
        message = template
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [p.email,]
        mail = EmailMessage(subject, message, email_from, recipient_list)
        mail.attach(p.qr.name, p.qr.read())
        mail.send()

    return render(request, 'app/sent.html', {})

def pati_gayela(request):
    context = {}
    context['objects_list'] = PassModel.objects.filter(recognized=True)
    print(context)
    return render(request, 'app/pati_gayela.html', context)

def bachya_khutya(request):
    context = {}
    context['objects_list'] = PassModel.objects.filter(recognized=False)
    return render(request, 'app/bachya_khutya.html', context)



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