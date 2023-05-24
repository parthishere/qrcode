from events.models import Event
import cv2
from invitee.models import Invitee
from pyzbar.pyzbar import decode

import numpy as np 


import base64
from io import BytesIO

import numpy as np
from PIL import Image


def base64_decode(data):
    out=base64.decodestring(data.split(',')[1].encode())
    return out
     
def base64_encode(data):
    if data:
        return 'data:image/png;base64,' + data


def get_face_detect_data(data, event):
    nparr = np.fromstring(base64_decode(data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_data, message = detectImage(img, event)
    # print('image_data',image_data)

    return base64_encode(image_data), message


def detectImage(image, event_id):
            
    frame = image
    message = None
    # self.frame = cv2.flip(self.frame,1)
    for barcode in decode(frame):
        data = barcode.data.decode('utf-8')
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        print(data)
        try:
            name, email, phone_number, event, unique_id, other_info = data.split(',')[0], data.split(',')[1], data.split(',')[2], data.split(',')[3], data.split(',')[4], data.split(',')[5]
        except:
            pass
            print("will not recognize")
            data = "Not valid QR"
            message = {"message": "not valid QR", "code": 1004}
            cv2.polylines(frame, [pts], True, (0, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
        
        try:
            event = Event.objects.prefetch_related("invitees", "recognied_invitees").get(pk=event_id)
            q = Invitee.objects.filter(email=email, unique_id=unique_id, event=event)
            q_in_event_exists = q in event.invitees.all()
            q_already_scaned = q in event.recognied_invitees.all()
            if q_in_event_exists:
                                    
                pts2 = barcode.rect
                
                if q_already_scaned:
                    cv2.polylines(frame, [pts], True, (0, 0, 255), 5)
                    
                    cv2.putText(frame, "scanned again", (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    message = {"message": "Scanned Again", "code": "1000"}
                else:
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 5)

                    cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    
                    q.recognized = True
                    q.save()
                    event.recognied_invitees.add(q)
                    event.save()
                    message = {"message": [name, email, phone_number, event, unique_id, other_info], "code": "1001" }
            else:
                data = "User does not exists in the event"
                message = {"message": "User does not exists in the event", "code": "1002"}
                cv2.polylines(frame, [pts], True, (255, 0, 0), 5)
                pts2 = barcode.rect
                cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
        except:
            message = {"message": "Something Is Wrong either Event or Invitee doesn't exist", "code": "1003"}
                
        # cv2.imshow('frame', self.frame)
    # ret, jpeg = cv2.imencode('.jpg', frame)
                

    buffer = BytesIO()
    img = Image.fromarray(frame)
    img.save(buffer, format="png")
    encoded_string = base64.b64encode(buffer.getvalue()).decode('ascii')
    return encoded_string, message