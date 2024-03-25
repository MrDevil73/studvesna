from django.db import models
from telebot.types import User as TelegramUser


class TgUser(models.Model):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    is_judge = models.BooleanField(default=False)

    def __str__(self):
        nm = ""
        #nm += f"@{self.username} " if self.username else ""
        nm += f"{self.name} " if self.name else ""
        nm += f"id_{self.user_id} " if nm == "" else ""
        nm += f"(СУДЬЯ)" if self.is_judge else ""
        return nm

    def create_or_update_user(self, tg_json: TelegramUser) -> 'TgUser':
        user, created = TgUser.objects.get_or_create(user_id=tg_json.id)
        if created or user.username != tg_json.username:
            user.username = tg_json.username or user.username
            nm = tg_json.first_name if tg_json.first_name else ""
            nm += tg_json.last_name if tg_json.last_name else ""
            user.name = nm
            user.save()

        return user


class Category(models.Model):
    name_category = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name_category}"


class Performance(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=128)
    executor = models.CharField(max_length=128)
    is_sended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title_name} {self.executor}"


class Score(models.Model):
    judge = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.judge} for {self.performance} score {self.value}"
