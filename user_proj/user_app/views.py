from django.shortcuts import render
from user_app.models import UserProfileInfo
from user_app.forms import UserForm,UserInfo
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'user_app/index.html')

@login_required
def special(request):
    return HttpResponse('You are logged in !!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    # user_form = UserForm()
    # user_info = UserInfo()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        user_info = UserInfo(data = request.POST)

        if user_form.is_valid() and user_info.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            info = user_info.save(commit = False)
            info.user = user

            if 'profile_pic' in request.FILES:
                info.profile_pic = request.FILES['profile_pic']

            info.save()
            registered = True
        else:
            print('Failed')
    else:
        user_form = UserForm()
        user_info = UserInfo()


    return render(request,'user_app/registration.html',{'user_form':user_form,'user_info':user_info,'registered':registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('User is not active')
        else:
            print('username{} tried to login'.format(username))
            return HttpResponse('Invalid username/password')

    else:
        return render(request,'user_app/user_login.html',{})
