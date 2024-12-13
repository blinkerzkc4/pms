import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_custom_mail(subject, template_name, context, user_email):
    try:
        email_content = render_to_string(f"../templates/{template_name}.html", context)
        text_content = None
        if os.path.exists(f"../templates/{template_name}.txt"):
            text_content = render_to_string(
                f"../templates/{template_name}.txt", context
            )

        msg = EmailMultiAlternatives(
            subject=subject,
            to=[user_email],
            from_email=None,
            body=text_content
            if text_content is not None
            else "Please enable html view",
        )
        msg.attach_alternative(email_content, "text/html")
        msg.send()

    except Exception as e:
        print(e)
