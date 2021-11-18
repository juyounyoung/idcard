from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.paginator import Paginator

from .models import *


# Create your views here.

# 게시판 조회
def index(request):
    # 페이징 5개씩
    all_boards = Board.objects.all()  # 정렬 기준 추가 필요
    paginator = Paginator(all_boards, 5)
    page = int(request.GET.get('page', 1))
    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards': boards})

# 게시판 글쓰기
def post(request):
    if request.method == "POST":
        # TODO ::: 학생 리스트, 사진 DB 저장 기능 필요
        author = request.POST['author']
        title = request.POST['title']
        content = request.POST['content']
        board = Board(author=author, title=title, content=content)
        board.save()
        return HttpResponseRedirect(reverse('board_list'))
    else:
        return render(request, 'board_register.html')

# 게시판 상세조회
def detail(request, post_id):
    try:
        board = Board.objects.get(pk=post_id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'detail.html', {'board': board})