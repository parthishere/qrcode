from django.shortcuts import render
from django.http.response import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


from .recog import QrRecognize
from .models import PassModel

# Create your views here.
def qrscan(request):
    return render(request, 'app/qrscan.html', {})

def send_email(request):

    send_mail(
    subject = 'Test Mail',
    message = 'Kindly Ignore',
    from_email = 'noreply@gmail.com',
    recipient_list = ['parthishere1234@gmail.com',],
    fail_silently = False,
    )
    return redirect('app:complete')

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