from django.urls import path

from . import views

app_name = 'diary'   # name space

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:board_id>/', views.detail, name='detail'),
    path('answer/create/<int:board_id>/', views.answer_board, name='answer_board'),
    path('post/write/', views.post_write, name='post_write'),
]