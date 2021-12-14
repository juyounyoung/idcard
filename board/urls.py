from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('board', views.board, name='board'),
    path('board_write', views.board_write, name='board_write'),
    path('board_insert', views.board_insert, name='board_insert'),
    path('board_view', views.board_view, name='board_view'),
    path('board_edit', views.board_edit, name='board_edit'),
    path('pw_edit', views.pw_edit, name='pw_edit'),
    path('board_final', views.board_final, name='board_final'),

    #path('post/<int:post_id>', views.detail, name='detail')
]