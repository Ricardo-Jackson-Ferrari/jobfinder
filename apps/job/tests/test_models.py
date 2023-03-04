from django.urls import reverse_lazy
from django.utils.text import slugify
from job.models import Category, Item, Job, Section
from model_bakery import baker


class TestCategory:
    def test_str_return(self):
        obj = baker.prepare(Category)
        assert obj.title == str(obj)


class TestJob:
    def test_str_return(self):
        obj = baker.prepare(Job)
        assert obj.title == str(obj)

    def test_get_absolute_url(self, db):
        profile = baker.make(Job)
        url = reverse_lazy(
            'job:detail',
            kwargs={'title': slugify(profile.title), 'pk': profile.pk},
        )

        assert profile.get_absolute_url() == url


class TestSection:
    def test_str_return(self):
        obj = baker.prepare(Section)
        assert obj.title == str(obj)


class TestItem:
    def test_str_return(self):
        obj = baker.prepare(Item)
        assert obj.item == str(obj)
