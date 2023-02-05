# Generated by Django 3.2.4 on 2023-02-05 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gallery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=gallery.models.get_picture_upload_path, verbose_name='Файл')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Картина',
                'verbose_name_plural': 'Картины',
            },
        ),
    ]