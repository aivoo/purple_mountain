from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect

from .forms import PostForm

from .models import Article, Tutorial, TaskList

import random, datetime

UA_LIST = [
    'Trident',  # IE内核
    'Presto',  # opera内核
    'AppleWebKit',  # 苹果、谷歌内核
    'Gecko',  # 火狐内核
    'Android',  # android终端
    'Adr',  # android终端
    'iPhone',  # 是否为iPhone或者QQHD浏览器
    'iPad',  # 是否iPad
]

ENCODE_LIST = {
    '0': '&#xF369;',
    '1': '&#xF52C;',
    '2': '&#xe072;',
    '3': '&#xF2bd;',
    '4': '&#xF51D;',
    '5': '&#xF7D9;',
    '6': '&#xE52C;',
    '7': '&#xF783;',
    '8': '&#xE8B8;',
    '9': '&#xEB7F;',
}


def index(request):
    tasklist = TaskList.objects.all()
    return render(request, 'tasks/index.html', {'tasklist': tasklist})


def api_data(request):
    articles = Article.objects.filter(exist=True).order_by('create_time')
    data = [{
        'id':art.id,
        'title':art.title,
        'image': art.image,
        'readcount':art.readcount
    } for art in articles]

    return JsonResponse({'articles': data})


def article_list(request):
    articles = Article.objects.filter(exist=True).order_by('create_time')
    return render(request, 'tasks/article_list.html', {'items': articles})


def article_one(request, pk):
    art_one = get_object_or_404(Article, pk=pk, exist=True)
    return render(request, 'tasks/article_one.html', {'item': art_one})


def tutorial_list(request):
    tutorials = Tutorial.objects.filter(exist=True)

    return render(request, 'tasks/tutorial_list.html', {'items': tutorials})


def text_encode(num):
    return ''.join(ENCODE_LIST[i] for i in str(num))


def web_encode(num):
    today = datetime.date.today()
    day = today.day
    month = today.month

    num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # list('0123456789')
    random.shuffle(num_list)
    encode_num_list = (num_list.index(i) for i in str(num))

    join_str = str(random.random())
    num_encode = join_str.join(str(day * item + month) for item in encode_num_list)

    return num_encode, join_str, num_list


def tutorial_one(request, pk):
    meta = request.META
    user_agent = meta.get('HTTP_USER_AGENT')
    host = meta.get('HTTP_HOST')
    # print(request.META, request.path)

    if not user_agent or not host: # 如果没有 ua 或者 host
        return HttpResponse(status=403)

    for ua in UA_LIST: # 如果 ua 不符合要求
        if ua in user_agent:
            break
    else:
        return HttpResponse(status=403)

    if not request.user.is_authenticated and pk > 11: # 未登录状态只能查看前几课内容
        return render(request, 'registration/login.html', {})

    tut_one = get_object_or_404(Tutorial, id=pk, exist=True)

    all_tut = Tutorial.objects.filter(exist=True)

    tut_last = all_tut.filter(index__lt=tut_one.index).last()
    tut_next = all_tut.filter(index__gt=tut_one.index).first()

    readcount_encode, join_str, num_list = web_encode(tut_one.readcount)

    # print(readcount_encode, join_str)

    return render(request, 'tasks/article_one.html', {
        'item': tut_one,
        'last': tut_last,
        'next': tut_next,
        'readcount': "%s" % readcount_encode,
        'join_str': join_str,
        'num_list': ''.join(num_list),
        # 'readcount': text_encode(tut_one.readcount),
        'likecount': text_encode(tut_one.likecount),
        'commentcount': text_encode(tut_one.commentcount),
    })


def tutorial_new(request):
    meta = request.META
    user_agent = meta.get('HTTP_USER_AGENT')
    host = meta.get('HTTP_HOST')

    if not user_agent or not host: # 如果没有 ua 或者 host
        return HttpResponse(status=403)

    for ua in UA_LIST: # 如果 ua 不符合要求
        if ua in user_agent:
            break
    else:
        return HttpResponse(status=403)

    if not request.user.is_authenticated:  # 未登录状态需要先登录
        return render(request, 'registration/login.html', {})

    if request.method == "POST":
        print('start post')
        form = PostForm(request.POST)
        print('form:', form, form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('tasks:tutorial_one', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'tasks/tutorial_new.html', {'form': form})
