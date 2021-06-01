from botocore import model
from djongo import models   # MongoDB
from django.contrib.auth.models import User

class Write(models.Model):
    board_subject = models.CharField(max_length=200)  # 제목
    board_content = models.TextField()    # 내용
    board_date = models.DateTimeField(auto_now_add=True)    # 생성날짜
    mem_name = models.CharField(max_length=20)  # 글쓴이
    board_emo = models.TextField(max_length=100) # 감정
    board_img = models.TextField(max_length=100) # 이미지 분석 결과
    board_tag = models.TextField(max_length=20) # 태그

    class Meta:
        abstract = False

# 답변모델, 보통 PK는 ID로 자동생성 함
class Answer(models.Model):
    board = models.ForeignKey(Write, on_delete=models.CASCADE)    # Write에서 가져온 외래키, 질문이 지워지면 답변도 지워지게! (on_delete=models.CASCADE)
    answer_content = models.TextField()    # 내용
    answer_date = models.DateTimeField()    # 생성날짜

# S3 업로드 모델
class S3upload(models.Model):
    picture = models.FileField(upload_to='media/') # 파일 필드, 업로드 경로 media/