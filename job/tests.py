from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from .models import Recuiter, StudentUser, Job, Applyjob, ApplyjobHistory
from django.urls import reverse
from django.core import mail
from datetime import date

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ApplicationWorkflowTests(TestCase):
    def setUp(self):
        # create recruiter user
        self.rec_user = User.objects.create_user(username='rec@example.com', email='rec@example.com', password='pass')
        self.rec = Recuiter.objects.create(user=self.rec_user, mobile='+911234567890', company='Acme', type='recuiter', status='active')

        # create student/applicant
        self.st_user = User.objects.create_user(username='applicant@example.com', email='applicant@example.com', password='pass')
        self.st = StudentUser.objects.create(user=self.st_user, mobile='+919876543210', qualification='B.Tech', interest='python', experience='2')

        # create job
        self.job = Job.objects.create(recuiter=self.rec, start_date=date.today(), end_date=date.today(), title='Python Developer', salary='50000', image='', description='Work on Python', experience='1', location='Remote', skills='python', creationdate=date.today())

        # create application
        self.app = Applyjob.objects.create(fname='Test', lname='User', mobile=self.st.mobile, email=self.st_user.email, experience=self.st.experience, qualification=self.st.qualification, gender='M', num=self.job.id)

        self.client = Client()

    def test_recruiter_can_accept_and_triggers_email_and_history(self):
        # login as recruiter
        logged = self.client.login(username='rec@example.com', password='pass')
        self.assertTrue(logged)
        url = reverse('change_application_status', args=[self.app.id])
        resp = self.client.post(url, {'action': 'accept'}, follow=True)
        self.app.refresh_from_db()
        self.assertEqual(self.app.status, 'Accepted')
        # history entry created
        histories = ApplyjobHistory.objects.filter(application=self.app)
        self.assertTrue(histories.exists())
        # email sent
        self.assertTrue(len(mail.outbox) >= 1)

    def test_applicant_can_download_joining_letter_after_accept(self):
        # accept the application first
        self.client.login(username='rec@example.com', password='pass')
        url = reverse('change_application_status', args=[self.app.id])
        self.client.post(url, {'action': 'accept'}, follow=True)

        # login as applicant and download
        self.client.logout()
        self.client.login(username='applicant@example.com', password='pass')
        dl_url = reverse('download_joining_letter', args=[self.app.id])
        resp = self.client.get(dl_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/pdf')
