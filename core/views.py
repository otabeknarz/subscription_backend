from rest_framework.decorators import api_view

from core.models import Account
from rest_framework.response import Response

from .models import Bot, Channel, Pay

from accounts.serializers import AccountSerializer
from .serializers import BotSerializer, ChannelSerializer


@api_view(["GET"])
def get_accounts(request):
    accounts = AccountSerializer(Account.objects.filter(is_active=True), many=True)
    return Response(accounts.data, status=200)


@api_view(["POST"])
def add_account(request):
    """
    Create a new account if it doesn't exist.

    :param:
    request: POST
    request
    with 'id', 'name',
        'phone_number', and 'username'.
    :return: Response
    with account data or error.
    """
    if not request.data.get("id"):
        return Response({"detail": "Account id is required"}, status=400)
    elif Account.objects.filter(id=request.data.get("id")).exists():
        return Response({"detail": "Account already exists"}, status=400)

    account = AccountSerializer(
        Account.objects.create(
            id=request.data.get("id"),
            name=request.data.get("name"),
            phone_number=request.data.get("phone_number"),
            username=request.data.get("username"),
        )
    )
    return Response(account.data, status=201)


@api_view(["GET"])
def get_bots(request):
    if request.query_params.get("account_id"):
        bots = BotSerializer(
            Bot.objects.filter(
                owner__id=request.query_params.get("account_id"), is_active=True
            ),
            many=True,
        )
        return Response(bots.data, status=200)

    bots = BotSerializer(Bot.objects.filter(is_active=True), many=True)
    return Response(bots.data, status=200)


@api_view(["POST"])
def add_bot(request):
    try:
        account = Account.objects.get(id=request.data.get("owner"))
        channel = Channel.objects.get(id=request.data.get("channel_id"), owner=account)
        bot = Bot.objects.create(
            id=request.data.get("id"),
            name=request.data.get("name"),
            token=request.data.get("token"),
            username=request.data.get("username"),
            channel=channel,
            owner=account,
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=400)
    return Response(BotSerializer(bot).data, status=201)


@api_view(["PATCH"])
def update_bot(request, id):
    try:
        bot = Bot.objects.get(id=id)
        bot_serializer = BotSerializer(bot, data=request.data, partial=True)
        if bot_serializer.is_valid():
            bot_serializer.save()
        else:
            return Response(bot_serializer.errors, status=400)
    except Exception as e:
        return Response({"detail": str(e)}, status=400)
    return Response(BotSerializer(bot).data, status=200)


@api_view(["GET"])
def get_channels(request):
    if request.query_params.get("account_id"):
        if request.query_params.get("doesnt_have_bot"):
            channels = ChannelSerializer(
                Channel.objects.filter(
                    owner__id=request.query_params.get("account_id"),
                    is_active=True,
                    bot=None,
                ),
                many=True,
            )
            return Response(channels.data, status=200)
        channels = ChannelSerializer(
            Channel.objects.filter(
                owner__id=request.query_params.get("account_id"), is_active=True
            ),
            many=True,
        )
        return Response(channels.data, status=200)
    channels = ChannelSerializer(Channel.objects.filter(is_active=True), many=True)
    return Response(channels.data, status=200)


@api_view(["POST"])
def add_channel(request):
    try:
        channel = Channel.objects.create(
            id=request.data.get("id"),
            name=request.data.get("name"),
            owner=Account.objects.get(id=request.data.get("owner")),
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=400)

    return Response(ChannelSerializer(channel).data, status=201)
