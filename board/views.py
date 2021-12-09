from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote
from django.db.models import Q
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

from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
# @login_message_required
def login(request):
    if request.method == 'POST':
        username2 = request.POST['school_id']
        password2 = request.POST['password']


        if Users_user.objects.filter(school_ID=username2).exists():
            getUser = Users_user.objects.get(school_ID=username2)
            # 로그인 성공 -> board_list
            if getUser.password == password2:
                getName = school_info.objects.get(school_ID=username2)
                request.session['school_name'] = getName.school_name
                request.session['school_ID'] = username2
                if password2 =='password1':
                    # return render(request, 'pw_edit.html')
                    return render(request, 'login.html')
                else:
                    return redirect('/board')
    return render(request, 'login.html')


#비밀번호 변경 팝업창(미완성)

def pw_edit(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('users:profile')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'pw_edit.html', {'password_change_form':password_change_form})





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
        paginator = Paginator(search_board_list, 5)
        page = int(request.GET.get('page', 1))
        search_board_list = paginator.get_page(page)
        return render(request, 'board_list.html', {'boards': search_board_list, 'search':search_keyword})

    return render(request, 'board_list.html', {'boards': boards})

def board_write(request):
    if Board.objects.all().exists():
        obj = Board.objects.latest('id')
        new_board_id = int(obj.id) + 1
    else:
        new_board_id = 1
    post_id = request.GET.get('board_id', new_board_id)
    school_id = request.session['school_ID']
    print("board_detail")
    print(post_id)

    if request.FILES.get('excelfile') is not None:
        print("excel not none")
        excel_file = request.FILES.get('excelfile')
        fs = FileSystemStorage(location='static/board/xlsx')
        name = fs.save(excel_file.name, excel_file)


        sheets = load_workbook(excel_file, read_only=True).sheetnames
        for sheet in sheets:
            table1 = pd.read_excel(excel_file, sheet_name=sheet, header=0)
            for r in range(0, table1.index.stop):
                student_group = sheet
                student_name = table1.iat[r, 1]
                student_id = table1.iat[r, 2]
                student_rn = table1.iat[r, 3]
                student_phone = table1.iat[r, 4]
                student_img = str(student_id) + '_' + student_name + '.jpg'
                if student.objects.filter(Q(school_ID=school_id) & Q(student_ID=student_id)).exists():
                    student_row = student.objects.filter(Q(school_ID=school_id) & Q(student_ID=student_id))
                    student_row.update(
                        student_group=student_group,
                        student_name=student_name,
                        student_rn=student_rn,
                        student_phone=student_phone,
                        student_img=student_img,
                    )
                else:
                    student_row = student.objects.create(
                        school_ID=school_id,
                        student_ID=student_id,
                        student_group=student_group,
                        student_name=student_name,
                        student_rn=student_rn,
                        student_phone=student_phone,
                        student_img=student_img,
                        # 'detail_address': detail_address,
                    )

    students = student.objects.filter(school_ID=school_id)
    context = {
        'students': students,
        'board_id': post_id
    }

    return render(request, 'board_register.html', context)

# 게시판 글쓰기
def board_insert(request):
    title = request.GET['title']
    school_name = request.session['school_name']
    filename = ''

    #학생이미지
    if request.FILES.get('ufile') is not None:
        uploaded_file = request.FILES.get('ufile')
        name_org = uploaded_file.name
        name_ext = os.path.splitext(name_org)[1]

        fs = FileSystemStorage(location='static/board/image')

        name = fs.save(name_org + name_ext, uploaded_file)
        filename = uploaded_file.name

    if title != "":
        rows = Board.objects.create(title=title, school_name=school_name, filename=filename)
        return redirect('/board')
    else:
        return redirect('/board_write')


# 게시판 상세조회
def board_view(request):
    post_id = request.GET.get('board_id')
    print("board_detail"+post_id)
    school_id = request.session['school_ID']
    school_name = request.session['school_name']
    boards = get_object_or_404(Board, id=post_id)
    students = student.objects.filter(school_ID=school_id)

    if school_id == boards.school_name:
        board_auth = True
    else:
        board_auth = False

    context = {
        'boards': boards,
        'board_auth': board_auth,
        'board_id': post_id,
        'students': students,
        'count': int(students.count()/3)
    }

    response = render(request, 'board_template.html', context)


    boards.hit_count += 1
    boards.save()

    return response

# 게시글 수정
def board_edit(request):
    post_id = request.GET['board_id']
    boards = get_object_or_404(Board, id=post_id)
    school_id = request.session['school_ID']
    school_name = request.session['school_name']
    students = student.objects.filter(school_ID=school_id)

    context = {
        'boards': boards,
        'board_id': post_id,
        'students': students,
        'count': int(students.count()/3)
    }

    return render(request, 'board_register.html', context)


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

# 엑셀 업로드
def excel_upload(request):
    post_id = request.GET.get('board_id')
    school_id = request.session['school_ID']
    print("board_detail")
    print(post_id)

    if request.FILES.get('excelfile') is not None:
        print("excel not none")
        excel_file = request.FILES.get('excelfile')
        fs = FileSystemStorage(location='static/board/xlsx')
        name = fs.save(excel_file.name, excel_file)

        table1 = pd.read_excel(excel_file, sheet_name='1반', header=0)

        df = pd.read_excel(excel_file)
        for sheet_name in df.sheet_names:
            print(sheet_name)

        for r in range(1, table1.nrows):
            student_group = '1반'
            student_name = table1.cell(r, 2).value
            student_id = table1.cell(r, 3).value
            student_rn = table1.cell(r, 4).value
            student_phone = table1.cell(r, 5).value
            student_img = student_id+'_'+student_name+'.jpg'
            if student.objects.filter(Q(school_ID=school_id) & Q(student_ID=student_id)).exists():
                student_row = student.objects.filter(Q(school_ID=school_id) & Q(student_ID=student_id))
                student_row.update(
                    student_group=student_group,
                    student_name=student_name,
                    student_rn=student_rn,
                    student_phone=student_phone,
                    student_img=student_img,
                )
            else:
                student_row = student.objects.create(
                    school_ID=school_id,
                    student_ID=student_id,
                    student_group=student_group,
                    student_name=student_name,
                    student_rn=student_rn,
                    student_phone=student_phone,
                    student_img=student_img,
                    # 'detail_address': detail_address,
                )

    students = student.objects.filter(school_ID=school_id)
    context = {
        'students': students,
        'board_id': post_id
    }

    return render(request, 'board_register.html', context)