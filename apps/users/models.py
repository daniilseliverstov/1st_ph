from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import BaseModel


class Department(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Название отдела")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"


class User(AbstractUser, BaseModel):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Отдел")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
