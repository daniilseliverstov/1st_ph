from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User


class Customer(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    city = models.CharField(max_length=50, verbose_name="Город")
    code = models.CharField(max_length=10, verbose_name="Код заказчика")
    manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Менеджер")

    def __str__(self):
        return f'{self.name} - {self.code}'

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"
