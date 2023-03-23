import os

from django.db import models
from django.db.models import CASCADE

from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
        null=True,
        blank=True,
        default=None,
    )
    verification_code = models.CharField(max_length=50, null=True, blank=True, default=None)

    objects = models.Manager()

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def set_verification_code(self) -> str:
        code = self._generate_verification_code()
        self.verification_code = code
        self.save(update_fields=('verification_code',))
        return code
