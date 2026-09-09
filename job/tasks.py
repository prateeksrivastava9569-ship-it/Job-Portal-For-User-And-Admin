from .models import Applyjob, Job
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from io import BytesIO

try:
    import django_rq
except Exception:
    django_rq = None

from .views import _generate_interview_letter_pdf


def send_interview_email(application_id):
    """Generate interview invitation PDF and email it to the applicant.
    This function is safe to call synchronously (in-process) or can be used as an RQ job.
    """
    try:
        application = Applyjob.objects.get(id=application_id)
    except Applyjob.DoesNotExist:
        return False

    try:
        pdf_buffer = _generate_interview_letter_pdf(application)
        filename = f'InterviewLetter_{application.fname}_{application.lname}_{application.id}.pdf'

        job = None
        try:
            job = Job.objects.get(id=application.num)
        except Job.DoesNotExist:
            job = None

        subject = f'Interview Invitation for {job.title if job else "your application"}'
        body_text = f'Dear {application.fname},\n\nWe are pleased to invite you for an interview for the position of {job.title if job else "the role"}. Please find the attached interview invitation with details including the interview location.\n\nBest regards,\nHR Team'
        body_html = f"<p>Dear {application.fname},</p><p>We are pleased to invite you for an <strong>interview</strong> for the position of {job.title if job else 'the role'}. Please find the attached interview invitation with details including the interview location.</p><p>Best regards,<br/>HR Team</p>"

        from_email = settings.DEFAULT_FROM_EMAIL or 'no-reply@example.com'
        to_email = [application.email] if application.email else []

        if to_email:
            msg = EmailMultiAlternatives(subject, body_text, from_email, to_email)
            msg.attach_alternative(body_html, 'text/html')
            msg.attach(filename, pdf_buffer.getvalue(), 'application/pdf')
            msg.send(fail_silently=False)
            return True
    except Exception:
        return False

    return False


def enqueue_send_interview_email(application_id):
    """Try to enqueue the email job to RQ if available; otherwise run synchronously."""
    if django_rq is not None:
        try:
            q = django_rq.get_queue('default')
            q.enqueue(send_interview_email, application_id)
            return True
        except Exception:
            # fall back to synchronous
            return send_interview_email(application_id)
    else:
        return send_interview_email(application_id)
