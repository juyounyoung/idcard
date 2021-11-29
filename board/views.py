from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.paginator import Paginator

from .models import *
from openpyxl import load_workbook

# Create your views here.

# 게시판 조회
def index(request):
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

#엑셀 업로드
def xlsxload():
    load_wb = load_workbook("abc.xlsx", data_only=True)
    load_ws = load_wb['1반']
    for row in load_ws.rows:
        for cell in row:
            print(cell.value)