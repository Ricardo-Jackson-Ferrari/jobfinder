from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('email address'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    is_candidate = models.BooleanField('candidate status', default=False)
    is_company = models.BooleanField('company status', default=False)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class ProfileAbstract(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email

    class Meta:
        abstract = True


class ProfileCandidate(ProfileAbstract):
    cv = models.FileField(
        upload_to='cv',
        validators=[FileExtensionValidator(allowed_extensions=('pdf',))],
        blank=True,
        null=True,
    )


class ProfileCompany(ProfileAbstract):
    logo = models.ImageField(upload_to='logo_company', blank=True)
    contact_email = models.EmailField(max_length=255, blank=True)
    website = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
