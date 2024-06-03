"""
Модуль моделей субд
"""
from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    """
    Модель для сервиса
    """
    id = models.AutoField(primary_key=True)
    clinic = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.clinic

class SearchHistory(models.Model):
    """
    Модель для истории поиска
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"

class FavoriteService(models.Model):
    """
    Модель для любимых сервисов
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.service.clinic}"