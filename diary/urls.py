from django.urls import path

from . import views

app_name = 'diary'   # name space

urlpatterns = [
    path('', views.index, name='index'),    # 메인
    path('<int:board_id>/', views.detail, name='detail'),   # 글 자세히 보기
    path('answer/create/<int:board_id>/', views.answer_board, name='answer_board'), # 댓글 작성
    path('post/write/', views.post_write, name='post_write'),   # 글 쓰기
    path('analyze/', views.analyze_emotion, name='analyze_emotion'),
]