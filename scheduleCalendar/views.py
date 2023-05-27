import json
import time
from .models import Event
from django.db import models as django_models  
from .forms import CalendarForm, EventForm
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from .forms import ImageUploadForm

def index(request):
    """
    カレンダー画面
    """
    # CSRFのトークンを発行する
    get_token(request)

    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def get_event(request, parameter):

    try:
        event = Event.objects.get(pk=parameter)

    except Event.DoesNotExist:
        return JsonResponse(
            data={},
            status=404
        )

    event = {
        "id": event.id,
        "title": event.event_name,
        "start": event.start_date,
        "end": event.end_date,
    }

    template = loader.get_template("event.html")
    return HttpResponse(template.render(event))

def get_events(request):
    """
    イベントの取得
    """
    
    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # FullCalendarの表示範囲のみ表示
    events = Event.objects.filter(
        start_date__lt=formatted_end_date, end_date__gt=formatted_start_date
    )

    # fullcalendarのため配列で返却
    list = []
    for event in events:
        list.append(
            {
                "id": event.id,
                "title": event.event_name,
                "start": event.start_date,
                "end": event.end_date,
            }
        )

    return JsonResponse(list, safe=False)

def add_event(request):

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # 登録処理
    event = Event(
        event_name=str(event_name),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
    )
    event.save()

    # 空を返却
    return HttpResponse("")


def edit_event(request):
    """
    イベント編集
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    id = datas["id"]
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # 更新処理
    event = Event(
        id=id,
        event_name=str(event_name),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
    )
    event.save()

    return HttpResponse("")

def delete_event(request, _id):
    """
    イベント削除
    """
    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # 削除処理
    event = Event(
        id=_id,
    )
    event.delete()

    return HttpResponse("")

# 独自の変換関数    
def encode_myway(obj):
    if isinstance(obj, django_models.Model):
        return obj.encode()    # models.py のモデルに encode() メソッドを追加定義すること
        # encode という名前は適当に付けました
    # elif isinstance(obj, QuerySet):
    #     return list(obj)    # 空の QuerySet は list 化する
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")
    
class ImageUploadView(CreateView):
    template_name = "nippo/image-upload.html"
    form_class = ImageUploadForm
    success_url = "/"