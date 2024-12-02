from rest_framework import serializers
from .models import Bot, Channel, Pay
from accounts.serializers import AccountSerializer


class ChannelSerializer(serializers.ModelSerializer):
    owner = AccountSerializer()

    class Meta:
        model = Channel
        fields = (
            "id",
            "name",
            "owner",
        )


class BotSerializer(serializers.ModelSerializer):
    owner = AccountSerializer()
    channel = ChannelSerializer()

    class Meta:
        model = Bot
        fields = (
            "id",
            "name",
            "token",
            "username",
            "owner",
            "is_running",
            "required_pay_amount",
            "channel",
        )
