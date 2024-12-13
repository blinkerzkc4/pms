from email.mime.image import MIMEImage
from functools import lru_cache

from django.contrib.staticfiles import finders


def generate_mime_image(image_bytes, content_id):
    image = MIMEImage(image_bytes)
    image.add_header("Content-ID", f"<{content_id}>")
    return image


@lru_cache
def email_header_image():
    path = finders.find("assets/email/header.png")
    with open(path, "rb") as file:
        image_bytes = file.read()
    return generate_mime_image(image_bytes, "email_header")
