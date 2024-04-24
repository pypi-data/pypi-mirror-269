
from django.contrib import admin
from django.urls import path

from src.chat_bot_sea.seatalk import views as seatalk_views

urlpatterns = [
    path('seatalk/bots/admin/', admin.site.urls),
    path('seatalk/bots/', seatalk_views.BotView.as_view(), name='bots'),
]
