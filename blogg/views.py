from django.shortcuts import render, get_object_or_404
from .forms import  usersignupfrm, userloginfrm, passwordfrm, userchangefrm, adminchangefrm, modelblogggfrm, commentform, profileform
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import blogg, comment, profile
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, date
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    f = blogg.objects.order_by('-id')
    return render(request, 'app/home.html', {'ff': f})

    
def showpage(request, id):
    a = get_object_or_404(blogg, id=id)
    b = blogg.objects.filter(id=a.id)
    c = comment.objects.filter(commentt=a).order_by('-id')
    total = a.total_likes()
    liked = False
    if a.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        d = commentform(request.POST or None)
        if d.is_valid():
            s = d.cleaned_data['content']
            cmnt = comment.objects.create(commentt=a, usr=request.user, content=s)
            cmnt.save()
            return HttpResponseRedirect(reverse('show', args=[str(id)]))
    else:
        d = commentform()
    return render(request, 'app/showpage.html',{'comform': d, 'comments': c, 'b': b, 'liked': liked, 'total_likes': total})


def like_blog(request, id):
    a = request.POST.get('blog_id')
    p = get_object_or_404(blogg, id=a)
    c = request.user.id
    liked = False
    if p.likes.filter(id=c).exists():
        p.likes.remove(request.user)
        liked = False
    else:
        p.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('show', args=[str(id)]))

def comdelete(request, id):
    s = get_object_or_404(comment, id=id)
    if request.user == s.usr:
        s.delete()
    else:
        messages.warning(request, "You can't delete this comment..!!")
    return HttpResponseRedirect('/home/')


def about(request):
    name = request.user.get_full_name()
    return render(request, 'app/about.html', {'name': name})


def dashboardd(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            fm = blogg.objects.all().order_by('-id')
        else:
            a = request.user.email
            fm = blogg.objects.filter(user__email=a).order_by('-id')
        return render(request, 'app/dashboard.html', {'fm': fm, 'name': request.user.get_full_name})
    else:
        return HttpResponseRedirect('/login/')


def addblog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = modelblogggfrm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'successfully post...!!!')
                return HttpResponseRedirect('/dashboard/')
        else:
            z = request.user.id
            x = request.user.username
            fm = modelblogggfrm(initial={'user': z, 'name': '~' + x})
        return render(request, 'app/addblog.html', {'fm': fm})
    else:
        return HttpResponseRedirect('/login/')


def updateblog(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            fd = get_object_or_404(blogg, id=id)
            fm = modelblogggfrm(request.POST, instance=fd)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            fd = get_object_or_404(blogg, id=id)
            fm = modelblogggfrm(instance=fd)
            a = fd.title
            b = fd.brief
            c = fd.link
            z = request.user.id
            x = request.user.username
            y = datetime.now()
            n = date.today()
            fm = modelblogggfrm(initial={'user': z, 'name': '~' + x,'title':a,'brief':b,'link':c,'date':n,'dtn':y})
        return render(request, 'app/update.html', {'fm': fm})
    else:
        return HttpResponseRedirect('/login/')


def deleteblog(request, id):
    if request.user.is_authenticated:
        fm = blogg.objects.get(id=id)
        fm.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


def userlogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        if request.method == 'POST':
            fm = userloginfrm(request.POST)
            if fm.is_valid():
                a = fm.cleaned_data['username']
                b = fm.cleaned_data['password']

                user = auth.authenticate(username=a, password=b)
                if user is not None:
                    auth.login(request, user)
                    messages.info(request, 'You are logged In Successfully..!!')
                    return HttpResponseRedirect('/home/')
                else:
                    messages.info(request, 'Invalid credential')
        else:
            fm = userloginfrm()
        return render(request, 'app/login.html', {'fm': fm})

def usersignup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        if request.method == 'POST':
            fm = usersignupfrm(request.POST)
            if fm.is_valid():
                a = fm.cleaned_data['username']
                b = fm.cleaned_data['first_name']
                c = fm.cleaned_data['last_name']
                d = fm.cleaned_data['email']
                e = fm.cleaned_data['password']
                g = fm.cleaned_data['password2']
                if e == g:
                    f = User.objects.create_user(username=a, first_name=b, last_name=c, email=d, password=e)
                    f.save()
                    profile.objects.create(profile_id=f)
                    messages.success(request, 'You are Successfully Registered..!!')
                    return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Password not matched')
        else:
            fm = usersignupfrm()
        return render(request, 'app/signup.html', {'fm': fm})

def userlogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def passwordchange(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = passwordfrm(data=request.POST, user=request.user)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password successfully changed..!!')
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = passwordfrm(user=request.user)
        return render(request, 'app/passchange.html', {'ff': fm})
    else:
        return HttpResponseRedirect('/')

def detail(request):
    fm = User.objects.all()
    return render(request, 'app/details.html', {'ff': fm})


def updatedetail(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fd = User.objects.get(id=id)
                fm = adminchangefrm(request.POST, instance=fd)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Details successfully updated..!!')
                    return HttpResponseRedirect('/details/')
            else:
                fd = User.objects.get(id=id)
                fm = userchangefrm(request.POST, instance=fd)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Post successfully updated..!!')
                    return HttpResponseRedirect('/details/')
        else:
            if request.user.is_superuser:
                fd = User.objects.get(id=id)
                fm = adminchangefrm(instance=fd)
            else:
                fd = User.objects.get(id=id)
                fm = userchangefrm(instance=fd)
        return render(request, 'app/updatedetail.html', {'ff': fm})
    else:
        return HttpResponseRedirect('/')


def deletedetail(request, id):
    if request.user.is_authenticated:
        fm = User.objects.get(id=id)
        fm.delete()
        return HttpResponseRedirect('/details/')
    else:
        return HttpResponseRedirect('/')

def search(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            name = request.POST['search']
            fm = User.objects.filter(username__icontains=name)
            return render(request, 'app/details.html', {'ff': fm, 'abc': name})
    else:
        return HttpResponseRedirect('/')

def profiles(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = adminchangefrm(request.POST, instance=request.user)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Your profile is successfully updated...!!')
                    return HttpResponseRedirect('/dashboard/')
            else:
                fm = userchangefrm(data=request.POST, instance=request.user)
                if fm.is_valid():
                    fm.save()
                    messages.success(request, 'Your profile is successfully updated...!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            if request.user.is_superuser == True:
                fm = adminchangefrm(instance=request.user)
            else:
                fm = userchangefrm(instance=request.user)
        return render(request, 'app/profile.html', {'ff': fm})
    else:
        return HttpResponseRedirect('/login/')

def dpfile(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            fp = profileform(request.POST, request.FILES, instance=request.user.profile)
            if fp.is_valid():
                fp.save()
                return HttpResponseRedirect('/profile/')
        else:
            fp = profileform(instance=request.user.profile)
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'app/dpp.html', {'dpf': fp})


def searchblogg(request):
    if request.method == 'POST':
        search = request.POST['searchuserblogg']
        fm = blogg.objects.filter(user__username__icontains=search)
        aa = get_object_or_404(User, username=search)
        aaa = aa.pk
        ff = profile.objects.get(profile_id=aaa)
    return render(request, 'app/searchblogg.html', {'fm': fm, 'fp': ff, 'aa': aa, 'name': search})
