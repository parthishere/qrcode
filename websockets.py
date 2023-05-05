from email.errors import MessageParseError
import json
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qrwebsite.settings")

import django
django.setup()
from asgiref.sync import sync_to_async
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import base64
from events.models import Event
import cv2
from accounts.models import Invitee
from pyzbar.pyzbar import decode
# from channels.db import database_sync_to_async


import numpy as np 

from io import BytesIO
from PIL import Image




class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection with tornado')
      
    async def on_message(self, message):
        
        
        message = json.loads(message)
        # print("recived event message",message['event_id'])
        nparr = np.frombuffer(base64.b64decode(message['message'].split(',')[1].encode()), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image_data, msg = await detectImage(img, message['event_id'])
        # print("processed message",type(image_data), len(image_data), msg)
    
        
        # b = base64.b64decode(message['message'])
        # image_data, msg = get_face_detect_data(b, message['event_id'])
        
        
        if msg :
            print(msg)
            # not valid QR
            self.write_message(json.dumps({"image":image_data, "message": msg['message']}))
        else:
            if not image_data:
                image_data = message['message']
            else:
                self.write_message(json.dumps({"image":image_data, "message": None}))
        
 
    def on_close(self):
        print ('connection closed')
 
    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/websocket', WSHandler),
], cookie_secret="L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM=")


async def detectImage(image, event_id):
            
    frame = image
    message = None
    # frame = cv2.flip(frame,1)
    for barcode in decode(frame):
        data = barcode.data.decode('utf-8')
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        try:
            qr_name, qr_email, qr_phone_number, qr_event_primary_key, qr_unique_id = data.split(',')[0], data.split(',')[1], data.split(',')[2], data.split(',')[3], data.split(',')[4]
        except:
            print("will not recognize")
            data = "Not valid QR"
            message = {"message": "not valid QR", "code": 1004}
            cv2.polylines(frame, [pts], True, (0, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
        
        
        og_event =  await _get_event(pk=event_id)
        
        q = await _get_invites(email=qr_email, unique_id=qr_unique_id, event=og_event)
        
        q_in_event_exists = True if q.event == og_event else False 
        print("q exists")
        print(q_in_event_exists)
        print("event_id")
        print(event_id)
        print("event_primary_key")
        print(qr_event_primary_key)
        q_already_scaned = q in og_event.recognized_invitees.all()
        if q_in_event_exists and event_id == qr_event_primary_key:                
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
                og_event.recognied_invitees.add(q)
                og_event.save()
                message = {"message": [qr_name, qr_email, qr_phone_number, og_event, qr_unique_id], "code": "1001" }
        else:
            data = "User does not exists in the event"
            message = {"message": "User does not exists in the event", "code": "1002"}
            cv2.polylines(frame, [pts], True, (255, 0, 0), 5)
            pts2 = barcode.rect
            cv2.putText(frame, data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
        # except:
        #     message = {"message": "Something Is Wrong either Event or Invitee doesn't exist", "code": "1003"}
                
                

    buffer = BytesIO()
    img = Image.fromarray(frame)
    img.save(buffer, format="png")
    encoded_string = base64.b64encode(buffer.getvalue()).decode('ascii')
    return 'data:image/png;base64,'+encoded_string, message
 
@sync_to_async
def _get_event(pk):
    e = Event.objects.prefetch_related("recognized_invitees").get(pk=pk)
    return e



@sync_to_async
def _get_invites(email, unique_id, event):
    e = Invitee.objects.get(email=email, unique_id=unique_id, event=event)
    return e

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()