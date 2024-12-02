from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Accounts
    path("accounts/", views.get_accounts, name="accounts"),
    path("account/add/", views.add_account, name="add_account"),

    # Channels
    path("channels/", views.get_channels, name="channels"),
    path("channel/add/", views.add_channel, name="add_channel"),

    # Bots
    path("bots/", views.get_bots, name="bots"),
    path("bot/add/", views.add_bot, name="add_bot"),
    path("bot/update/<str:id>/", views.update_bot, name="update_bot"),
]
