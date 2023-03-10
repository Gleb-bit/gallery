# Generated by Django 3.2.4 on 2023-02-05 16:54

import accounts.models
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Адрес')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=accounts.models.get_user_avatar_upload_path, verbose_name='Аватар')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'In registration'), (1, 'Registered'), (2, 'Blocked')], default=0, verbose_name='Статус')),
                ('code', models.CharField(blank=True, default='', max_length=128, verbose_name='code')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Подтверждён')),
                ('email_verified', models.BooleanField(default=False, verbose_name='Подтверждена почта')),
                ('is_active', models.BooleanField(default=True, help_text='Определяет, следует ли считать этого пользователя активным.Снимите этот флажок вместо удаления учетных записей.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Определяет, может ли пользователь войти как администратор.', verbose_name='staff status')),
                ('is_admin', models.BooleanField(default=False, help_text='Определяет, может ли пользователь войти как суперюзер.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TempData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_verify_code', models.CharField(blank=True, max_length=10, null=True)),
                ('email_verify_code_expires', models.DateTimeField(blank=True, null=True)),
                ('password_recover_key', models.UUIDField(blank=True, null=True)),
                ('password_recover_key_expires', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temp', to='accounts.user')),
            ],
        ),
    ]
