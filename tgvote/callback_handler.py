from .models import TgUser, Performance, Score, Category
from telebot.types import CallbackQuery
from .config import send_message, edit_message
import tgvote.keyboards as MyKeyb


def Create_Score_Message(perfom: Performance, user: TgUser):
    mes = (f"Категория: {perfom.category.name_category}\n"
           f"Название выступления: {perfom.title_name}\n"
           f"Исполнитель: {perfom.executor}\n\n"
           f"Как вы его оцените?")
    if perfom.is_olympic:
        all_perf_by_category = Performance.objects.filter(category_id=perfom.category_id).all()
        perf_ids=[el.id for el in all_perf_by_category]
        all_scores=Score.objects.filter(performance_id__in=perf_ids,judge=user).all()
        excl=[ind for ind in range(1,11-len(perf_ids))]
        for score in all_scores:
            excl.append(score.value)
        keyb_score = MyKeyb.score_keyboard(perfom.id,excl)
    else:
        keyb_score = MyKeyb.score_keyboard(perfom.id)

    return mes,keyb_score


def perfomances_by_id_category(call: CallbackQuery):
    categ_id = int(call.data.split('_')[-1])
    user = TgUser().create_or_update_user(call.from_user)
    now_category = Category.objects.filter(id=categ_id).first()
    if not now_category:
        send_message(call.message.chat.id, "Ошибка категории, обратитесь к администратору")
        return None
    perfomances = Performance.objects.filter(category_id=categ_id).prefetch_related('category')
    #print(Score.objects.filter(judge__user_id=user.user_id),'Scores')
    perf_by_id = {el.performance_id: el.value for el in Score.objects.filter(judge__user_id=user.user_id)}
    #print(perfomances)
    #print(perf_by_id,'scores')
    edit_message(call.message.chat.id, call.message.message_id, f"Выберите выступление для категории \n<b><u>{now_category.name_category}</u></b>",
                 reply_markup=MyKeyb.perfomances_by_category(perfomances, perf_by_id), )


def list_categories_to_edit(call: CallbackQuery):
    edit_message(call.message.chat.id, call.message.id, "Выберите нужную категорию:", reply_markup=MyKeyb.categoryes())


def give_choice_score(call: CallbackQuery):
    user = TgUser().create_or_update_user(call.from_user)

    id_perf = int(call.data.split('_')[-1])
    perfom: Performance = Performance.objects.filter(id=id_perf).prefetch_related('category').first()
    if not perfom:
        send_message(call.message.chat.id, "Ошибка выступления, обратитесь к администратору")
        return None
    mes,keyb_score=Create_Score_Message(perfom,user)
    edit_message(call.message.chat.id, call.message.message_id, mes, reply_markup=keyb_score)


def set_assesment(call: CallbackQuery):
    user = TgUser().create_or_update_user(call.from_user)

    id_perf, score_value = map(int, call.data.split('_')[1:])
    perfom: Performance = Performance.objects.filter(id=id_perf).prefetch_related('category').first()
    if not perfom:
        send_message(call.message.chat.id, "Ошибка выступления, обратитесь к администратору")
        return
    if perfom.is_olympic:
        perf_ids_els=Performance.objects.filter(category_id=perfom.category_id).all()
        perf_ids=[el.id for el in perf_ids_els]
        score_with_this_value=Score.objects.filter(value=score_value, judge=user, performance_id__in=perf_ids).first()
        if score_with_this_value is None:
            pass
        else:
            perfo=Performance.objects.filter(id=score_with_this_value.performance_id).first()
            messge=f"У вас уже установлена оценка {score_value} для {perfo.title_name}\nВыберите другую оценку или смените для {perfo.title_name}"
            keyb=MyKeyb.change_score_perfomance(perfo.id,f"Сменить оценку для {perfo.title_name}")
            send_message(call.message.chat.id, messge,rep_id=call.message.id,reply_markup=keyb)
            return
    score_mdl, crt = Score.objects.get_or_create(judge_id=user.user_id, performance_id=id_perf)
    score_mdl.value = score_value
    score_mdl.save()


    mes = (f"Категория: {perfom.category.name_category}\n"
           f"Название выступления: {perfom.title_name}\n"
           f"Исполнитель: {perfom.executor}\n\n"
           f"Ваша оценка: {score_mdl.value}")

    edit_message(call.message.chat.id, call.message.message_id, mes)
