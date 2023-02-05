from django.db import models

from accounts.models import User


def get_picture_upload_path(instance, filename):
    return f'pictures/{instance.user.username}/{filename}'


class Picture(models.Model):
    file = models.FileField('Файл', upload_to=get_picture_upload_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='pictures')

    class Meta:
        verbose_name = 'Картина'
        verbose_name_plural = 'Картины'

    def __str__(self):
        return f'{self.file.name} {self.user.username}'
