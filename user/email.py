from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from utils.constants import APP_NAME
from utils.email_attachments import email_header_image, generate_mime_image


def send_digital_signature_verification_email(request: HttpRequest) -> int:
    context = {
        "user": request.user,
        "app_name": APP_NAME,
    }
    body_html = render_to_string(
        "emails/user/digital_signature_verification.html",
        context=context,
        request=request,
    )
    signature_image = request.user.digital_signature.open()
    signature_image_mime = generate_mime_image(signature_image.read(), "user_signature")

    message = EmailMultiAlternatives(
        subject=f"{APP_NAME} Digital Signature Verification",
        body=strip_tags(body_html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.user.email],
    )
    message.attach_alternative(body_html, "text/html")
    message.attach(email_header_image())
    message.attach(signature_image_mime)
    return message.send(fail_silently=False)


def send_user_credentials_email(user, password: str) -> int:
    context = {
        "user": user,
        "password": password,
        "app_name": APP_NAME,
    }
    body_html = render_to_string("emails/user/user_credentials.html", context)

    message = EmailMultiAlternatives(
        subject=f"{APP_NAME} Account Created",
        body=strip_tags(body_html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    message.attach_alternative(body_html, "text/html")
    message.attach(email_header_image())

    return message.send(fail_silently=False)


def send_email(email, password):
    message = f"""
    You have been added to the system. Your temporary password  is as follows:
    Password:{password}
    """

    send_mail(
        subject="Activate email",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
