from address.models import Address
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from tools.validators import validate_file_size

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
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    cv = models.FileField(
        upload_to='cv',
        validators=(
            FileExtensionValidator(allowed_extensions=('pdf',)),
            validate_file_size,
        ),
        blank=True,
        null=True,
    )


class ProfileCompany(ProfileAbstract):
    logo = ResizedImageField(
        upload_to='logo_company',
        size=(85, 85),
        blank=True,
        validators=(validate_file_size,),
    )
    name = models.CharField(_('name'), max_length=100)
    address = models.ForeignKey(
        to=Address, on_delete=models.SET_NULL, blank=True, null=True
    )
    contact_email = models.EmailField(
        _('contact email'), max_length=255, blank=True
    )
    website = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(
        _('short description'), max_length=50, blank=True
    )
    description = models.TextField(
        _('description'), max_length=500, blank=True
    )

    def get_absolute_url(self):
        return reverse_lazy(
            'account:profile_company',
            kwargs={'title': slugify(self.name), 'pk': self.pk},
        )
