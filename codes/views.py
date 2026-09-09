from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from datetime import date


def is_valid_gmail_email(email):
    if not email:
        return False
    value = email.strip()
    if value.count("@") != 1:
        return False
    local_part, domain = value.split("@", 1)
    return bool(local_part) and domain.lower() == "gmail.com"

# Create your views here.
def index(request):
    return render(request, 'index.html')


def admin_login(request):
    error = ""
    if request.method == "POST":
        ur = request.POST.get('uname')
        pd = request.POST.get('pwd')
        user = auth.authenticate(username=ur, password=pd)
        if user is not None:
            try:
                if user.is_staff:
                    auth.login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html', d)


def user_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_login.html', d)


def recuiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recuiter.objects.get(user=user)
                if user1.type == "recuiter" and user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'recuiter_login.html', d)


def recuiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        if not is_valid_gmail_email(e):
            error = "yes"
        else:
            try:
                user = User.objects.create_user(first_name=f, last_name=l, username=e, email=e, password=p)
                Recuiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=company, type="recuiter", status="pending")
                error = "no"
            except:
                error = "yes"
    d = {'error': error}
    return render(request, 'recuiter_signup.html', d)


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'user_home.html')


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


def recuiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recuiter_login')
    user = request.user
    recuiter = Recuiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']

        recuiter.user.first_name = f
        recuiter.user.last_name = l
        recuiter.mobile = con
        recuiter.gender = gen

        try:
            recuiter.save()
            recuiter.user.save()
            error = "no"
        except:
            error = "yes"
        try:
            i = request.FILES['image']
            recuiter.image = i
            recuiter.save()
            error = "no"
        except:
            pass
    d = {'recuiter': recuiter, 'error': error}
    return render(request, 'recuiter_home.html', d)


def logout(request):
    auth.logout(request)
    return redirect('/')


def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        if not is_valid_gmail_email(e):
            error = "yes"
        else:
            try:
                user = User.objects.create_user(first_name=f, last_name=l, username=e, email=e, password=p)
                StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
                error = "no"
            except:
                error = "yes"
    d = {'error': error}
    return render(request, 'user_signup.html', d)


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data': data}
    return render(request, 'view_users.html', d)


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')


def delete_recuiter(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recuiter = User.objects.get(id=pid)
    recuiter.delete()
    return redirect('recuiter_all')


def recuiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recuiter.objects.filter(status='pending')
    d = {'data': data}
    return render(request, 'recuiter_pending.html', d)


def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    recuiter = Recuiter.objects.get(id=pid)
    if request.method == "POST":
        s = request.POST['status']
        recuiter.status = s
        try:
            recuiter.save()
            error = "no"
        except:
            error = "yes"
    d = {'recuiter': recuiter, 'error': error}
    return render(request, 'change_status.html', d)


def recuiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recuiter.objects.filter(status='Accept')
    d = {'data': data}
    return render(request, 'recuiter_accepted.html', d)


def recuiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recuiter.objects.filter(status='Reject')
    d = {'data': data}
    return render(request, 'recuiter_accepted.html', d)


def recuiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recuiter.objects.all()
    d = {'data': data}
    return render(request, 'recuiter_accepted.html', d)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passwordadmin.html', d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passworduser.html', d)


def change_passwordrecuiter(request):
    if not request.user.is_authenticated:
        return redirect('recuiter_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'change_passwordrecuiter.html', d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recuiter_login')
    error = ""
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        st = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exc = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user = request.user
        recuiter = Recuiter.objects.get(user=user)
        try:
            Job.objects.create(recuiter=recuiter, end_date=ed, start_date=st, title=jt, salary=sal, image=l, description=des, experience=exc, location=loc, skills=skills, creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_job.html', d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recuiter_login')
    user = request.user
    recuiter = Recuiter.objects.get(user=user)
    job = Job.objects.filter(recuiter=recuiter)
    d = {'job': job}
    return render(request, 'job_list.html', d)


def edit_jobdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('recuiter_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        st = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        exc = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        job.title = jt
        job.salary = sal
        job.experience = exc
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if st:
            try:
                job.start_date = st
                job.save()
            except:
                pass
        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
    d = {'error': error, 'job': job}
    return render(request, 'edit_jobdetail.html', d)


def change_companylogo(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        l = request.FILES['logo']
        job.image = l
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error, 'job': job}
    return render(request, 'change_companylogo.html', d)


def view_job_user(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    data = Job.objects.all()
    d = {'data': data}
    return render(request, 'view_job_user.html', d)


def full_job_detail(request, id):
    data = Job.objects.get(id=id)
    d = {'data': data}
    return render(request, 'full_job_detail.html', d)


def apply_now(request, id):
    user = request.user
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        email = request.POST['email']
        ex = request.POST['exp']
        q = request.POST['que']
        g = request.POST['gender']
        i = request.FILES['image']
        try:
            Applyjob.objects.create(fname=f, lname=l, mobile=con, email=email, experience=ex,
                                    qualification=q, gender=g, image=i, num=id)
            error = "no"
        except:
            error = "yes"
    d = {'user': user, 'error': error}
    return render(request, 'apply_now.html', d)


def applyed_condidate(request):
    data = Job.objects.all()
    d = {'data': data}
    return render(request, 'applyed_condidate.html', d)


def applied_condidate_list(request):
    data = Applyjob.objects.all()
    d = {'data': data}
    return render(request, 'applied_condidate_list.html', d)


def latest_job(request):
    job = Job.objects.all()
    d = {'job': job}
    return render(request, 'latest_job.html', d)


def delete_job(request, id):
    data = Job.objects.get(id=id)
    data.delete()
    return redirect('job_list')


def delete_condidate(request, id):
    data = Applyjob.objects.get(id=id)
    data.delete()
    return redirect('applied_condidate_list')
