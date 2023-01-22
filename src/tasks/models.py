from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from tasks.validators import PhoneNumberValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone, password, **extra_fields):
        """
        Create and save a user with the given phone, email, and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    validate_phone = PhoneNumberValidator()

    email = models.EmailField(_('email address'), unique=True, error_messages={
                              'unique': _('Email should be unique')})
    phone = models.CharField(_('phone'), max_length=12, validators=[
                             validate_phone, ], unique=True, error_messages={'unique': _('Phone should be unique')})
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Task(models.Model):
    user = models.ForeignKey('tasks.User', on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=100)
    description = models.TextField()
    execution_at = models.DateTimeField()
    is_done = models.BooleanField(default=False)
