from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse  # 헬로 월드 없애서 이제 필요 없음!
from .models import Write
from django.utils import timezone
from .forms import WriteForm
from django.core.paginator import Paginator
from django.http import JsonResponse
import boto3
import json

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
    context = {'board': board}
    return render(request, 'diary/board_detail.html', context)    # diary/board_detail.html에 context 파라미터로 넘겨줘라!

def answer_board(request, board_id):
    """
    diary 댓글 등록
    """
    board = get_object_or_404(Write, pk=board_id)
    board.answer_set.create(answer_content=request.POST.get('content'), answer_date=timezone.now())   
    return redirect('diary:detail', board_id=board.id)

def post_write(request):
    """
    diary 작성
    """
    if request.method == 'POST':
        form = WriteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.board_date = timezone.now()
            post.mem_name = "asd"
            post.save()
            return redirect('diary:index')
    else:
        form = WriteForm()
    context = {'form': form}
    return render(request, 'diary/board_write.html', {'form': form})


def analyze_emotion(request):
    """
    감정 분석
    """
    if request.method == 'POST':
        data = json.loads(request.body)   #board_write.html 에서 넘어온 일기 내용 저장
        comprehend = boto3.client(service_name='comprehend', region_name='ap-northeast-2')   #컴프리핸드 선언

        result = json.dumps(comprehend.detect_sentiment(Text=data.get('content'), LanguageCode="ko"), sort_keys=True)  #감정 분석 실시

        context = {
            'result': result,
        }
        return JsonResponse(context)   #json 형식으로 반환
