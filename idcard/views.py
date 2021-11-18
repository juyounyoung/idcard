from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.views import View
from django.views import generic


def login(request):
    return render(request, 'login.html')

def board_list(request):
    return render(request, 'board_list.html')