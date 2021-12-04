from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote
import urllib
import mimetypes
from mimetypes import guess_type
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
import pandas as pd
import datetime
import random
import os

from .models import *
from openpyxl import load_workbook

# Create your views here.

def login(request):
    if request.method == 'POST':
        username2 = request.POST['school_id']
        password2 = request.POST['password']

        print(username2)
        print(password2)
        # if User.objects.filter(user_id=username2).exists():
        #     getUser = User.objects.get(user_id=username2)
        #     # 로그인 성공 -> board_list
        #     if getUser.password == password2:
        return redirect('/board')
    return render(request, 'login.html')


# 게시판 조회
def board(request):
    # 페이징 5개씩
    all_boards = Board.objects.all()  # 정렬 기준 추가 필요
    paginator = Paginator(all_boards, 5)
    page = int(request.GET.get('page', 1))
    boards = paginator.get_page(page)

    search_keyword = request.GET.get('search', '')
    if search_keyword:
        search_board_list = all_boards.filter(title__icontains=search_keyword)
        return render(request, 'board_list.html', {'boards': search_board_list})

    return render(request, 'board_list.html', {'boards': boards})

def board_write(request):
    return render(request, 'board_register.html')

# 게시판 글쓰기
def board_insert(request):
    title = request.GET['title']
    school_name = request.GET['school_name']

    #학생이미지
    if request.FILES.get('ufile') is not None:
        uploaded_file = request.FILES.get('imgfile')
        name_org = uploaded_file.name
        name_ext = os.path.splitext(name_org)[1]

        fs = FileSystemStorage(location='static/board/photos')

        name = fs.save(name_org + name_ext, uploaded_file)

    #엑셀업로드
    """
    name_date = str(datetime.datetime.today().year) + '_' + str(datetime.datetime.today().month) + '_' + str(datetime.datetime.today().day)

    excel_file = request.FILES['excel_file']
    name_old = uploaded_file.name
    name_ext = os.path.splitext(name_old)[1]
    name_new = 'A' + name_date + '_' + str(random.randint(1000000000, 9999999999))

    fs = FileSystemStorage(location='static/board/xlsx')

    name = fs.save(name_new + name_ext, uploaded_file)

    table = pd.read_excel(excel_file, sheet_name = '1반', header=0)
    engine = create_engine("mysql+pymysql://root:root!@localhost:3306/studentidcard", encoding='utf-8-sig')
    table.to_sql(name='student', con=engine, if_exists='append', index=False)
    excel_data = list()
    for row in worksheet.iter_rows():
        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
    """


    if title != "":
        rows = Board.objects.create(title=title, school_name=school_name)
        return redirect('/board')
    else:
        return redirect('/board_write')


# 게시판 상세조회
def board_view(request):
    post_id = request.GET['board_id']
    boards = get_object_or_404(Board, id=post_id)

    context = {
        'board': boards,
    }

    response = render(request, 'board_template.html', context)


    boards.hit_count += 1
    boards.save()

    return response

# 게시글 첨부파일 다운로드 한글명 인코딩
def board_download_view(request):
    post_id = request.GET['board_id']
    boards = get_object_or_404(Board, id=post_id)
    url = boards.upload_files.url[1:]
    print(type(url))
    print(url)
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            # quote_file_url = urllib.parse.quote(file_url.encode('utf-8'))
            quote_file_url = urllib.parse.quote(boards.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            # response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url[29:]
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404