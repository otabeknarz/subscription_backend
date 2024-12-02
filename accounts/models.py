from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(BaseModel):
    # Telegram user id
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="images/profile_pictures/accounts/", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
