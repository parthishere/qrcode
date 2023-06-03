from invitee.models import Invitee
from events.models import Event
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

import json

@api_view(["POST"])  
@login_required 
def scan(request, event_pk=None):
    """
    
    Send Intrument found_string in the request.body as a json response 
    @param: "found_string"
    
    const data = {
        "found_string":"qr_name, qr_email, qr_phone_number, qr_event_primary_key, qr_unique_id"
    }
    
    fetch("URI", {
        method:"POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: JSON.stringyfy(data)
    })
    
    .then(response => response.json())
    
    
    """
    
    try:
        data = json.loads(request.body)
        string = data["found_string"]
        qr_name, qr_email, qr_phone_number, qr_event_primary_key, qr_unique_id = string.split(',')[0], string.split(',')[1], string.split(',')[2], string.split(',')[3], string.split(',')[4]
        
        
    except Exception as e:
        print(e)
        print("will not recognize")
        data = "Not valid QR"
        message = {"message": "not valid QR", "code": 1004}
        return Response(message)
    
    try:
        # user = request.user
        og_event = Event.objects.prefetch_related("recognized_invitees").get(pk=event_pk)
        
        q = Invitee.objects.get(email=qr_email, unique_id=qr_unique_id, event=og_event)

        q_in_event_exists = True if q.event == og_event else False 

        q_already_scaned = q.recognized
        
    except Exception as e:
        print(e)
        message = {"message": "not valid event or invitee", "code": 1004}
        return Response(message)
    
    
    try:
        if q_in_event_exists and int(event_pk) == int(qr_event_primary_key) and (og_event.created_by == request.user or request.user in og_event.moderators.all()):                
            
        
            if q_already_scaned:
                message = {"message": "Scanned Again", "code": 1000}
                return Response(message)
            else:
               
                q.recognized = True
                q.save()
                og_event.recognized_invitees.add(q)
                og_event.save()
                
                message = {"message": {"qrcode":qr_name, "qr_email":qr_email, "qr_phone_number":qr_phone_number, "event_pk":og_event.pk, "qr_unique_id":qr_unique_id}, "code": "1001" }
                return Response(message)
        else:
            data = "User does not exists in the event"
            message = {"message": "User does not exists in the event", "code": 1002}
            return Response(message)
            
    except Exception as e:
        message = {"message": f"Something Is Wrong either Event or Invitee doesn't exist {e}", "code": 1003}
    return Response(message)