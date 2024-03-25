from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views
from .admin import admin_site



urlpatterns = [
    path('admin/', admin_site.urls),
    path('score/', views.category_list, name='score_page'),
    path('score/<int:page>/', views.score_page, name='score_page'),
    path("tg_hook/", csrf_exempt(views.TgParse))
]
