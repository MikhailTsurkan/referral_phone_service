from django.contrib.auth.models import AbstractUser
from django.db import models


NULL = {"null": True, "blank": True}


class User(AbstractUser):
    """
    Модель пользователя, используется для аутентификации
    """
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    username = None

    phone = models.CharField(max_length=32,
                             unique=True,
                             verbose_name="telephone number",
                             help_text="a user telephone number"
                             )
    invite_code = models.CharField(max_length=6,
                                   verbose_name="invitation code",
                                   help_text="code for referencing on owner of this code"
                                   )
    invited_by = models.ForeignKey("self",
                                   on_delete=models.SET_NULL,
                                   verbose_name="invited by",
                                   help_text="reference on user, who invite this user",
                                   **NULL
                                   )

    def __str__(self):
        return getattr(self, self.USERNAME_FIELD)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
