#-*- coding:utf-8-*-

from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse  # 헬로 월드 없애서 이제 필요 없음!
from .models import Write
from django.utils import timezone   # 시간표시 모듈
from .forms import WriteForm
from django.core.paginator import Paginator # 페이지 기능 모듈
from django.http import JsonResponse
import boto3 # AWS 모듈
import json
import pandas as pd # pandas 모듈
from .models import S3upload # S3 업로드 모델
from django.conf import settings # AWS 세팅값을 사용하기 위해 settings 불러오기
from django.contrib.auth.models import User # 인증모듈

# def index(request):
#     return HttpResponse("안녕하세요 diary에 오신것을 환영합니다.")

def index(request):
    """
    diary 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # index 페이지 = 1페이지
    # 조회
    board_list = Write.objects.order_by('-board_date') # 최신 순으로 질문 출력
    # 페이징처리
    paginator = Paginator(board_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'board_list': page_obj}  # 위에 선언한 board_list를 board_list에다가 집어 넣음(context라는 배열에!) JSON 형식임

    return render(request, 'diary/board_list.html', context)  # 저장한 context 배열을 템플릿 안에 출력~ context는 파라미터!

def detail(request, board_id):   # board_id 객체를 가져옴
    """
    diary 내용 출력
    """
    board = Write.objects.get(id=board_id)
    context = {
        'board': board,
        'bucket' : settings.AWS_STORAGE_BUCKET_NAME,
        'region' : settings.AWS_REGION
        }
    return render(request, 'diary/board_detail.html', context)    # diary/board_detail.html에 context 파라미터로 넘겨줘라!

def answer_board(request, board_id):
    """
    diary 댓글 등록
    """
    board = get_object_or_404(Write, pk=board_id)   # 페이지 없으면 404 띄우기
    board.answer_set.create(answer_content=request.POST.get('content'), answer_date=timezone.now(), mem_name=request.user.username) # 내용, 시간, 이름
    return redirect('diary:detail', board_id=board.id)  # 리다이렉트 지정

def post_write(request):
    """
    diary 작성
    """
    if request.method == 'POST':
        form = WriteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # post에 담기
            post.board_date = timezone.now()    # 작성 시간
            post.mem_name = request.user.username   # 이름
            post.chkinfo = request.POST["chkinfo"] # 사진 공개 유무

            # 사진이 공개 설정이고 분석 결과가 있을 경우
            if post.chkinfo == "pictrue" and post.board_img != "None":
                post.imgread = settings.imgread # 전역변수에서 이미지 파일명을 가져오기, 사진이 비공개 설정이면 imgread = null
            
            post.save()
            return redirect('diary:index')
    else:
        form = WriteForm()
    context = {
        'form': form
        }
    return render(request, 'diary/board_write.html', {'form': form})


def analyze_emotion(request):
    """
    감정 분석 및 핵심 단어(태그) 추출
    """
    if request.method == 'POST':
        data = json.loads(request.body)   #board_write.html 에서 넘어온 일기 내용 저장
        comprehend = boto3.client(service_name='comprehend', region_name='ap-northeast-2')   #컴프리핸드 선언

        result_sentiment = json.dumps(comprehend.detect_sentiment(Text=data.get('content'), LanguageCode="ko"), sort_keys=True)  #감정 분석 실시

        result_keyword = json.dumps(comprehend.detect_key_phrases(Text=data.get('content'), LanguageCode="ko"), sort_keys=True, indent=4)
        sub = json.loads(result_keyword)
        KeyPhrases = sub["KeyPhrases"]
        # keyPhrases[0]["Score"] 와 같은 방법으로 참조
        keyword = []
        
        for i in KeyPhrases :
            if i["Score"] >= 0.75 :
                keyword.append(i)

        # print(type(KeyPhrases))
        context = {
            'result_sentiment': result_sentiment,
            'result_keyword' : keyword
        }
        return JsonResponse(context)   #json 형식으로 반환


def img_emotion(request):
    """
    이미지 업로드 및 이미지 감정 분석 (AWS S3 & Rekognition)
    """
    # POST 요청 시
    if request.method == 'POST':
        s3 = S3upload() # S3 이미지 업로드 모델
        s3.picture = request.FILES.get('picture') # 파일 저장
        filename = request.FILES['picture'].name # 파일명 변수 저장
        s3.save() # 업로드

        media = 'media/' # S3의 이미지 폴더 경로
        photo = media + filename # media/파일명.확장자
        settings.imgread = photo # 전역변수에 이미지 파일명 넣기
        bucket = settings.AWS_STORAGE_BUCKET_NAME # S3 버킷 이름
        region = settings.AWS_REGION # AWS 지역

        client=boto3.client('rekognition', region) # AWS 모듈, 사용할 서비스
        response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL']) # 이미지 분석 응답

        # 감정 값만 저장하는 반복문
        for faceDetail in response['FaceDetails']:
            emotions = faceDetail['Emotions']

        df = pd.DataFrame(emotions) # 감정 값 데이터 가공

        result = {} # 감정값을 저장할 사전
        for i in df.itertuples(): # 감정값을 사전에 저장할 반복문
            result[i.Type] = i.Confidence # 타입을 키로, 컨피던스를 벨류로

        # type = str(df.Type[0]) # 가장 커서 맨 위에 있는 감정
        # confidence = str(df.Confidence[0]) # 가장 커서 맨 위에 있는 감정 비율
        # result = type + ' ' + confidence # 감정과 비율 모두 출력 시 사용
        
        context = {
            'rekognition': result
        }

        return JsonResponse(context) # Json 형태로 응답