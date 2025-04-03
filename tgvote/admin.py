from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from .models import TgUser, Category, Score, Performance
from django.contrib.admin import AdminSite
import tgvote.keyboards as MyKeyb
from .callback_handler import Create_Score_Message
from .config import send_message

from django.contrib import messages as djangoMessage


class MyAppAdminSite(AdminSite):
    site_header = 'Студвесна'
    site_title = 'Студвесна'
    index_title = 'Приветики Юлечка Попова!'
    # list_filter = ['Lesson']


class ForTgUser(admin.ModelAdmin):
    readonly_fields = ('user_id',)
    list_display = ['user_name_', 'name_prof', 'judge_status']
    ordering = ['-is_judge']

    def judge_status(self, obj):
        return "Да" if obj.is_judge else ""

    def name_prof(self, obj):
        return obj.name

    def user_name_(self, obj):
        return f"@{obj.username}"

    user_name_.short_description = 'Личная ссылка'
    name_prof.short_description = 'Фамилия Имя'
    judge_status.short_description = 'Является судьёй'

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions


class ForPerformance(admin.ModelAdmin):



    def send_status(self, obj):
        return "Отправлено" if obj.is_sended else ""

    def counter_scores(self, obj):
        ln_judges = TgUser.objects.filter(is_judge=True).count()
        cnt = Score.objects.filter(performance_id=obj.id,judge__is_judge=True).count()
        return f"{cnt}/{ln_judges}"

    counter_scores.short_description = 'Количество оценок'


    def sum_scores(self, obj):
        cnt = [el.value for el in Score.objects.filter(performance_id=obj.id)]
        return f"{sum(cnt)}"
    def category_name(self, obj):
        return obj.category.name_category
    def olymp(self,obj):
        return "Олимпийский" if obj.is_olympic else ""
    category_name.short_description = 'Категория'  # Название столбца в админке
    category_name.admin_order_field = 'category__name_category'

    ordering = ['category__name_category', 'title_name']
    list_display = ['title_name', 'executor', 'category_name', 'send_status','olymp', 'counter_scores','sum_scores']
    counter_scores.short_description = 'Количество оценок'
    send_status.short_description = 'Статус отправки'
    sum_scores.short_description = 'Суммарно баллов'
    olymp.short_description = 'В Олиимпийской'



    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def send_to_all_judges(self, request, queryset: list[Performance]):

        if len(queryset) > 1:
            self.message_user(request, "Нужно выбрать только одно выступление", level=djangoMessage.WARNING)
            return

        if queryset[0].is_sended == True:
            self.message_user(request, f"Выступление \"{queryset[0].title_name}\" уже было отправлено всем судьям на оценку", level=djangoMessage.WARNING)
            return
        judges = TgUser.objects.filter(is_judge=True)



        for tgus in judges:
            mes, keyb_score = Create_Score_Message(queryset[0],tgus)
            send_message(tgus.user_id, mes, keyb_score)
        queryset[0].is_sended = True
        queryset[0].save()

        self.message_user(request, f"""Выступление "{queryset[0].title_name}" было отправлено всем судьям""")
        pass

    send_to_all_judges.short_description = 'Отправить всем судьям'

    actions = ['send_to_all_judges']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        judges = TgUser.objects.filter(is_judge=True)  # Список получателей
        # actions['-------']=(None,'-------',None)
        for judge in judges:
            action_name = f'Отправить {judge.name}'  # Имя действия, например, send_to_Judge1
            action_func = self.create_send_action(judge)  # Создание функции действия

            actions[action_name] = (action_func, action_name, action_name)  # Добавление действия
        return actions

    def create_send_action(self, judge):
        def send_action(modeladmin, request, queryset):
            if len(queryset) > 1:
                self.message_user(request, "Нужно выбрать только одно выступление", level=djangoMessage.WARNING)
                return
            # print(judge)
            mes, keyb_score = Create_Score_Message(queryset[0],judge)

            send_message(judge.user_id, mes, keyb_score)

            self.message_user(request, f"""Выступление "{queryset[0].title_name}" было отправлено {judge.name}""")

        send_action.short_description = f'Send to {judge}'  # Описание действия
        return send_action


class ForScores(admin.ModelAdmin):
    readonly_fields = ('judge', 'performance', 'value')

    def is_judge(self, obj):
        return f"Судья" if obj.judge.is_judge else ""


    def perf_name(self, obj):
        return obj.performance.title_name

    def perf_exec(self,obj):
        return obj.performance.executor

    is_judge.admin_order_field = 'judge__is_judge'
    perf_name.admin_order_field = 'performance__title_name'

    list_display = ['judge', 'is_judge','perf_name','perf_exec','value']
    ordering = ('judge__is_judge', 'performance__title_name')


admin_site = MyAppAdminSite(name='studvesna_vote')
admin_site.register(TgUser, ForTgUser)
admin_site.register(Category)
admin_site.register(Score, ForScores)
admin_site.register(Performance, ForPerformance)
# Register your models here.
