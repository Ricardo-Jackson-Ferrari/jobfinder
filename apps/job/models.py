from decimal import Decimal

from account.models import ProfileCompany
from address.models import Address
from django.core.validators import MinValueValidator
from django.db import models

from .choices import EXPERIENCIES, HIERARCHIES, MODALITIES


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.ForeignKey(to=ProfileCompany, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    vacancies = models.PositiveSmallIntegerField()
    modality = models.CharField(max_length=1, choices=MODALITIES)
    address = models.ForeignKey(
        to=Address, on_delete=models.SET_NULL, blank=True, null=True
    )
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.0'))],
        default=Decimal('0.0'),
    )
    status = models.BooleanField(default=True)
    description = models.TextField(max_length=500)
    hierarchy = models.CharField(max_length=3, choices=HIERARCHIES)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    experience = models.SmallIntegerField(choices=EXPERIENCIES)

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=100)
    job = models.ForeignKey(
        to=Job, on_delete=models.CASCADE, related_name='sections'
    )

    def __str__(self):
        return self.title


class Item(models.Model):
    item = models.CharField(max_length=150)
    section = models.ForeignKey(
        to=Section, on_delete=models.CASCADE, related_name='itens'
    )

    def __str__(self):
        return self.item
