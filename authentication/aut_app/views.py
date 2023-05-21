from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def registation(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request,"Your password and confirm password didn't match....!")

        if User.objects.filter(username=username):
            messages.error(request,'Your username already existed...!')
            return redirect('/registration')

        if User.objects.filter(email=email):
            messages.error(request,'Your email Id already existed...!')
            return redirect('/registration')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request,'Your account has been created successfully.')
        return redirect('/login')
    return render(request,'aut_app/registration.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(request,username=username, password=pass1)

        if user is not None:
            login(request,user)
            return render(request,'aut_app/home.html')
        else:
            messages.error(request,'Bad credential.')
            return redirect('/login')
    return render(request,'aut_app/login.html')


def home(request):
    return render(request,'aut_app/home.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'aut_app/change_password.html', {'form': form})
