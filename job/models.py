from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    qualification = models.CharField(max_length=200,null=True, blank=True)
    interest = models.CharField(max_length=200,null=True, blank=True)
    experience = models.CharField(max_length=50,null=True, blank=True)
    type = models.CharField(max_length=20,null=True)
    resume = models.FileField(null=True, blank=True, upload_to='resumes/')
    def _str_(self):
        return self.user.username

class Recuiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    company=models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=20,null=True)
    status=models.CharField(max_length=20,null=True)
    def _str_(self):
        return self.user.username

class Job(models.Model):
    recuiter = models.ForeignKey(Recuiter,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=100)
    salary = models.CharField(max_length=20)
    image = models.FileField()
    description = models.CharField(max_length=300)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=20)
    creationdate = models.DateField()
    def _str_(self):
        return self.title

class Applyjob(models.Model):
    fname = models.CharField(max_length=50,null=True)
    lname = models.CharField(max_length=50,null=True)
    mobile = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=255,null=True)
    experience = models.CharField(max_length=50,null=True)
    qualification = models.CharField(max_length=200,null=True)
    gender = models.CharField(max_length=10,null=True)
    image = models.FileField(null=True)
    num = models.IntegerField(null=True)
    status = models.CharField(max_length=20, null=True, default='Pending')
    status_changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='application_status_changes')
    status_changed_at = models.DateTimeField(null=True, blank=True)
    resume = models.FileField(null=True, blank=True, upload_to='resumes/')

    def get_student_user(self):
        try:
            user = User.objects.filter(email=(self.email or '')).first()
            if user:
                return StudentUser.objects.filter(user=user).first()
        except Exception:
            return None
        return None

    def get_student_resume(self):
        su = self.get_student_user()
        if su and su.resume:
            try:
                return su.resume
            except Exception:
                return None
        return None

    def get_resume(self):
        return self.resume or self.get_student_resume()



class ApplyjobHistory(models.Model):
    application = models.ForeignKey(Applyjob, on_delete=models.CASCADE, related_name='history')
    previous_status = models.CharField(max_length=50, null=True, blank=True)
    new_status = models.CharField(max_length=50, null=True, blank=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    changed_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application {self.application.id}: {self.previous_status} -> {self.new_status} at {self.changed_at}"

