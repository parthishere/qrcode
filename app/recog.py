import cv2
from pyzbar.pyzbar import decode

from django.shortcuts import get_list_or_404
import numpy as np 

from .models import PassModel


class QrRecognize():

    def __init__(self, details=None, username=None, unique_id=None):
                
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.data = None
        
    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        

    def get_frame(self):
        name = None
        email = None
        phone_number = None
        slug = None
                
        ret, self.frame = self.video.read()
        self.frame = cv2.flip(self.frame,1)
        for barcode in decode(self.frame):
            self.data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            print(self.data)
            try:
                name, email, phone_number, slug = self.data.split(',')[0], self.data.split(',')[1], self.data.split(',')[2], self.data.split(',')[3]
            except:
                pass
                print("will not recognize")
            
            try:
                q = PassModel.objects.filter(name=name, email=email, phone_number=phone_number, slug=slug)

                if q is not None:
                                      
                    
                    pts2 = barcode.rect
                    query = q.first()   

                    if query.recognized:
                        cv2.polylines(self.frame, [pts], True, (0, 0, 255), 5)
                        
                        cv2.putText(self.frame, "Scanned Again", (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    else:
                        cv2.polylines(self.frame, [pts], True, (0, 255, 0), 5)

                        cv2.putText(self.frame, self.data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                        
                        query.recognized = True
                        query.save()
                else:
                    self.data = "Not Recognized"
                    cv2.polylines(self.frame, [pts], True, (255, 0, 0), 5)
                    pts2 = barcode.rect
                    cv2.putText(self.frame, self.data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
            except:
                pass
                    
            # cv2.imshow('frame', self.frame)
        ret, jpeg = cv2.imencode('.jpg', self.frame)
                
        
        return self.data, jpeg.tobytes()