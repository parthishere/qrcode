import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import cv2
import numpy as np

def generate_qrcode(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    
    
    
    background_image = cv2.imread('background_image.jpg')

    data_to_encode = "hehe"
    qr_code = qrcode.make(data_to_encode)

 
    qr_code_image = cv2.cvtColor(np.array(qr_code), cv2.COLOR_RGB2BGR)

    qr_code_x = 100
    qr_code_y = 200

    overlay_image(background_image, qr_code_image, qr_code_x, qr_code_y)

   
    name = "Parth thakkar"
    name_x = 100
    name_y = 250
    max_width = 10
    
    overlay_text(background_image, name, name_x, name_y, max_width)


    cv2.imwrite('result_image.jpg', background_image)
    
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    qr_code_image = InMemoryUploadedFile(
        buffer,
        None,
        filename,
        'image/png',
        buffer.tell(),
        None
    )

    return qr_code_image



def overlay_image(background, overlay, x, y):
    h, w, _ = overlay.shape
    background[y:y+h, x:x+w] = overlay
    
    
def overlay_text(image, text, x, y, max_width):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2

    # Calculate the width and height of the text
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)

    # Adjust the text position if it exceeds the maximum width
    if x + text_width > max_width:
        x = max_width - text_width - 10  # Adjust the margin for the text

    # Overlay the text on the image
    cv2.putText(image, text, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)