import uuid
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generate_unique_code():
    return str(uuid.uuid4()).replace("-", "")[:10]

def generate_qr_code_image(code):
    qr = qrcode.make(code)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f"{code}.png")
