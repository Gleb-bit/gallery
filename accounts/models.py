from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def get_user_avatar_upload_path(instance, filename):
    return f'user_avatars/{instance.first_name} {instance.last_name}/{filename}'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, username=None):
        if username:
            try:
                validate_email(username)
            except ValidationError:
                raise ValidationError('Ошибка username')

            email = self.normalize_email(username)

        if not email:
            raise ValueError('У пользователя должен быть адрес электронной почты.')
        else:
            email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=email,
            is_staff=is_staff,
            is_admin=is_admin,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, password=None, **kwargs):
        email = kwargs['username']
        return self.create_user(email, password, True, False)

    def create_superuser(self, password=None, **kwargs):
        email = kwargs['username']
        return self.create_user(email, password, True, True)


class User(AbstractBaseUser):
    class Status(models.IntegerChoices):
        IN_REGISTRATION = 0, 'In registration'
        REGISTERED = 1, 'Registered'
        BLOCKED = 2, 'Blocked'

    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150, blank=True, null=True)

    email = models.EmailField('Адрес', blank=True, null=True, unique=True)

    avatar = models.ImageField(_("Аватар"), blank=True, null=True, upload_to=get_user_avatar_upload_path)

    status = models.PositiveSmallIntegerField(
        _("Статус"), choices=Status.choices, default=Status.IN_REGISTRATION)

    code = models.CharField(_("code"), max_length=128, default='', blank=True)
    is_verified = models.BooleanField('Подтверждён', default=False)
    email_verified = models.BooleanField('Подтверждена почта', default=False)

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Определяет, следует ли считать этого пользователя активным.'
            'Снимите этот флажок вместо удаления учетных записей.')
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Определяет, может ли пользователь войти как администратор.'
    )
    is_admin = models.BooleanField(
        'superuser status',
        default=False,
        help_text='Определяет, может ли пользователь войти как суперюзер.'
    )

    objects = UserManager()

    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class TempData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='temp')

    email_verify_code = models.CharField(max_length=10, blank=True, null=True)
    email_verify_code_expires = models.DateTimeField(blank=True, null=True)

    password_recover_key = models.UUIDField(blank=True, null=True)
    password_recover_key_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"
