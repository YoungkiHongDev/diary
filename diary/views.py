from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse  # 헬로 월드 없애서 이제 필요 없음!
from .models import Write
from django.utils import timezone
from .forms import WriteForm

# def index(request):
#     return HttpResponse("안녕하세요 diary에 오신것을 환영합니다.")

def index(request):
    """
    diary 목록 출력
    """
    board_list = Write.objects.order_by('-board_date') # 최신 순으로 질문 출력
    context = {'board_list': board_list}  # 위에 선언한 board_list를 board_list에다가 집어 넣음(context라는 배열에!) JSON 형식임
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
    diary 답변 등록
    """
    board = get_object_or_404(Write, pk=board_id)
    board.answer_set.board(content=request.POST.get('content'), board_date=timezone.now())
    return redirect('diary:detail', board_id=board.id)


def post_write(request):
    """
    pybo 질문등록
    """
    form = WriteForm()
    return render(request, 'diary/board_write.html', {'form': form})