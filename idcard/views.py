from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.views import View
from django.views import generic


def login(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']

        print(username2)
        print(password2)
        # if User.objects.filter(user_id=username2).exists():
        #     getUser = User.objects.get(user_id=username2)
        #     # 로그인 성공 -> board_list
        #     if getUser.password == password2:
        #         return redirect('board_list')
    return render(request, 'login.html')

def board_list(request):
    return render(request, 'board_list.html')

def board_register(request):
    return render(request, 'board_register.html')

def board_template(request):
    return render(request, 'board_template.html')