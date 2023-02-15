from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import states


class Address(models.Model):
    user = models.ForeignKey(to='account.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=8)
    uf = models.CharField(max_length=2, choices=states)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    number = models.CharField(max_length=50)
    complement = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.user.address_set.exclude(pk=self.pk).count() >= 5:
            raise ValidationError(
                _('maximum number of address already registered')
            )

    def unique_error_message(self, model_class, unique_check):
        error = super().unique_error_message(model_class, unique_check)

        error.message = _('An address with title %(title)s already exists.')
        error.params['title'] = self.title

        return error

    class Meta:
        unique_together = ['user', 'title']
