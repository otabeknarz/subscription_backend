from django.db import models
from accounts.models import Account


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Channel(BaseModel):
    # Telegram channel id
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="images/profile_pictures/channels/", blank=True, null=True
    )
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(Account, related_name="channels", blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Bot(BaseModel):
    # Telegram bot id
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="images/profile_pictures/bots/", blank=True, null=True
    )
    username = models.CharField(max_length=100, unique=True, null=True)
    token = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    is_running = models.BooleanField(default=True)
    users = models.ManyToManyField(Account, related_name="bots", blank=True)
    is_active = models.BooleanField(default=True)
    required_pay_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    # This is the channel group id that the bot is a member of and users can request to join
    channel = models.OneToOneField(
        Channel, on_delete=models.SET_NULL, null=True, related_name="bot"
    )

    def __str__(self):
        return self.name


class Pay(BaseModel):
    class Currencies(models.TextChoices):
        UZS = "UZS"
        USD = "USD"
        EUR = "EUR"
        RUB = "RUB"
        TON = "TON"
        # Telegram stars
        T_STAR = "T_STAR"

    bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True)
    # The account that the payment is made to
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=6, choices=Currencies.choices, default=Currencies.UZS
    )
    description = models.TextField(null=True, blank=True)
    is_payed = models.BooleanField(default=False)
    payed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.bot.name} - {self.amount} {self.currency}"
