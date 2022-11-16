from django.db import models
from apps.utils.base_model import BaseModel
from enum import IntEnum
from .managers import UserManager
from django.db.models import Manager


class UserGender(IntEnum):
    FEMALE = 0
    MALE = 1
    LADYBOY = 2

    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))


class Users(BaseModel):

    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.SmallIntegerField(choices=UserGender.choices())
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'users'
        verbose_name = 'users'
        verbose_name_plural = 'users'



class Article(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(Users, related_name='user_articles', on_delete=models.CASCADE)

    class Meta:
        db_table = 'articles'
