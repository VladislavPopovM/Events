from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Account(models.Model):
    TYPE_ACC = (
        ('staff','Staff'),
        ('client','Client'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=TYPE_ACC, default='client')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

class Event_base(models.Model):
    # Содержимое
    title = models.CharField(max_length=256)
    body = models.TextField()

    date_posting = models.DateTimeField(default=timezone.now)
    date_event = models.DateTimeField()

    class Meta:
        abstract = True

class Event_simple(Event_base):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='events_simple')
    participants = models.ManyToManyField(Account)

    def __str__(self):
        return f'{self.title} {author.user.email}'

    class Meta:
        verbose_name = 'Простая заявка'
        verbose_name_plural = 'Простые заявки'

class Event_detailed(Event_base):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='events_detailed')
    participants = models.ManyToManyField(Account)
    #Данные
    client_title = models.CharField(max_length=256)
    client_body = models.TextField()
    client_file = models.FileField(upload_to='files')
    
    def __str__(self):
        return f'{self.title} {author.user.email}'

    class Meta:
        verbose_name = 'Расширенная заявка'
        verbose_name_plural = 'Расширенные заявки'