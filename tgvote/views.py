from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import HttpResponse
from telebot import types
from .set_handlers import TgBot as TgBot
import json
from django.http import HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, Performance, Score, TgUser
from django.db.models import Sum, Q, Prefetch, Case, When, CharField, Value, IntegerField, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.db.models import Case, When, Exists, OuterRef, F, BooleanField

SECRET_TOKEN = os.getenv("SECRET_TOKEN")


@csrf_exempt
def TgParse(request):
    data = ""
    try:
        # token_telegram = request.headers.get("X-Telegram-Bot-Api-Secret-Token", None)
        # if token_telegram != SECRET_TOKEN:
        #     return HttpResponse("F u", status=418)
        data = request.body.decode('UTF-8', 'ignore')
        update = types.Update.de_json(data)
        TgBot.process_new_updates([update])
    except json.JSONDecodeError:
        pass
    except FileNotFoundError as ex:
        pass

    return HttpResponse("Ok", status=200)


@staff_member_required
def score_page(request, page: int = 0):
    # Ваша логика для страницы

    this_category = Category.objects.filter(id=page).first()

    # performances = Performance.objects.filter(category_id=page).prefetch_related('score_set').annotate(sum_score=Sum('score__value')).order_by('-sum_score')

    # performances = Performance.objects.filter(
    #     category_id=page
    # ).prefetch_related(
    #     Prefetch('score_set', queryset=Score.objects.filter(judge__is_judge=True), to_attr='filtered_scores')
    # ).annotate(
    #     sum_score=Coalesce(Sum('score__value', filter=Q(score__judge__is_judge=True)), 0)
    # ).order_by('-sum_score')
    class CustomPerf:
        def __init__(self):
            self.scores = []
            self.sum_score = 0
            self.judges = []
            self.sended = False
            self.title_name = ""
            self.executor = ""

    performance_id = 1

    judges = {el.name: el for el in TgUser.objects.filter(is_judge=True)}
    performances = Performance.objects.filter(category_id=page)
    perfs_to_value = {el.id: el for el in performances}
    perfs = {}
    for prf in performances:
        perfs[prf.id] = CustomPerf()
        perfs[prf.id].title_name = prf.title_name
        perfs[prf.id].executor = prf.executor
    # print(perfs)

    all_scores = Score.objects.all().prefetch_related('judge')
    for sc in all_scores:
        if sc.judge.name in judges and sc.performance in performances:
            perfs[sc.performance_id].scores.append(sc)
            perfs[sc.performance_id].sum_score += sc.value
            perfs[sc.performance_id].judges.append(sc.judge.name)
            perfs[sc.performance_id].sended = perfs_to_value[sc.performance_id].is_sended
    for kk in perfs:
        need = set(judges) - set(perfs[kk].judges)
        for el in need:
            perfs[kk].scores.append(Score(judge=judges[el], performance=perfs_to_value[kk], value=0))
        perfs[kk].scores.sort(key=lambda x: -x.value)

    keys_sort = sorted(list(perfs.keys()), key=lambda pf: -perfs[pf].sum_score)
    perf_sort = [perfs[kk] for kk in keys_sort]

    # performances=[]

    return render(request, "results.html", context={"performances": perf_sort, "keys_sort": keys_sort, "category": this_category})


@staff_member_required
def category_list(request):
    # Ваша логика для страницы

    categoryes = Category.objects.all()

    html = ""
    for cat in categoryes:
        html += f"<br><a href='{cat.id}'>{cat.name_category}</a>\n"

    return HttpResponse(html)
