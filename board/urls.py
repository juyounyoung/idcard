from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board_write', views.board_write, name='board_write'),
    path('board_insert', views.board_insert, name='board_insert'),
    path('board_view', views.board_view, name='board_view'),
    # path('post/<int:post_id>', views.detail, name='detail')
]