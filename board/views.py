from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import datetime
import random
import os

from .models import *
from openpyxl import load_workbook

# Create your views here.

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
        return render(request, 'board_list.html')
    return render(request, 'login.html')

# 게시판 조회
def board(request):
    # 페이징 5개씩
    all_boards = Board.objects.all()  # 정렬 기준 추가 필요
    paginator = Paginator(all_boards, 5)
    page = int(request.GET.get('page', 1))
    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards': boards})

def board_write(request):
    return render(request, 'board_register.html')

# 게시판 글쓰기
def board_insert(request):
    title = request.GET['title']
    school_name = request.GET['school_name']

    #학생이미지
    if request.FILES.get('ufile') is not None:
        uploaded_file = request.FILES.get('ufile')
        name_org = uploaded_file.name
        name_ext = os.path.splitext(name_org)[1]

        fs = FileSystemStorage(location='static/board/photos')

        name = fs.save(name_org + name_ext, uploaded_file)

    #엑셀업로드
    """
    name_date = str(datetime.datetime.today().year) + '_' + str(datetime.datetime.today().month) + '_' + str(datetime.datetime.today().day)

    uploaded_file = request.FILES['ufile']
    name_old = uploaded_file.name
    name_ext = os.path.splitext(name_old)[1]
    name_new = 'A' + name_date + '_' + str(random.randint(1000000000, 9999999999))

    fs = FileSystemStorage(location='static/board/xlsx')

    name = fs.save(name_new + name_ext, uploaded_file)

    load_wb = load_workbook(name, data_only=True)
    load_ws = load_wb['1반']
    for row in load_ws.rows:
        for cell in row:
            print(cell.value)
            
    student_list = [Student(**vals) for vals in row]
    Student.objects.bulk_create(student_list)
    """

    if title != "":
        rows = Board.objects.create(title=title, school_name=school_name)
        return redirect('/board')
    else:
        return redirect('/board_write')

# 게시판 상세조회
def board_view(request):
    post_id = request.GET['board_oid']
    board = Board.objects.filter(id=post_id)

    return render(request, 'board_template.html', {
        'board': board
    })