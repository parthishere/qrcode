import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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

    # Create a BytesIO object to temporarily hold the image data
    buffer = BytesIO()
    image.save(buffer, format='PNG')

    # Create an InMemoryUploadedFile from the buffer
    qr_code_image = InMemoryUploadedFile(
        buffer,
        None,
        filename,
        'image/png',
        buffer.tell(),
        None
    )

    return qr_code_image