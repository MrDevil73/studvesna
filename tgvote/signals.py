from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .config import send_message
from .models import TgUser


@receiver(pre_save, sender=TgUser)
def send_notification(sender, instance, **kwargs):

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    #print(old_instance.__dict__)
    #print(instance.__dict__)
    if not old_instance.is_judge and instance.is_judge:  # Проверяем, что is_judge теперь равно True
        user:TgUser = instance  # Получаем пользователя
        message = "Администратор назначил вас судьёй"  # Сообщение для отправки
        send_message(user.user_id,message)
