from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .models import QuestionEntity

def send_buy_question_mail(email: str, question_file_path: str, question_title: str):

    email_subject = 'UT DM Contest Question'
    email_body = render_to_string(
        'buy_question_mail.txt', 
        {
            "question_title" : question_title
        },
    )

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.attach_file(question_file_path, 'application/pdf')

    return email.send(fail_silently=False)