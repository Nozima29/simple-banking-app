from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from users.models import AuthUser

# Create your views here.


def login(request):
    template = 'index.html'
    if request.method == "POST":
        email = request.POST.get("email", None)
        passwd = request.POST.get("passwd", None)
        user = authenticate(username="john", password="secret")
        if user is None:
            return redirect(reverse('cards:register'))

    return render(request, template)


def create(request):
    template = 'users/create.html'
    if request.method == "POST":
        uname = request.POST.get("name", None)
        email = request.POST.get("email", None)
        passwd = request.POST.get("passwd", None)
        user = User.objects.filter(username=uname).first()
        if not user:
            user = User()
            user.username = uname
            user.email = email
        user.set_password(passwd)
        user.save()
        auth_user = AuthUser.objects.create(user=user)
        if auth_user:
            return redirect(reverse('cards:register'))

    return render(request, template)
