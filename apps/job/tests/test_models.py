from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.text import slugify
from job.models import Category, Item, Job, Section
from model_bakery import baker
from pytest import raises


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

    def test_create_section(self, db):
        job = baker.make(Job)
        section = baker.make(Section, job=job, title='Test section')
        assert section.clean() is None
        assert section.title == 'Test section'
        assert section.job == job

    def test_create_max_sections(self, db):
        job = baker.make(Job)
        baker.make(Section, job=job, _quantity=5)
        with raises(ValidationError) as excinfo:
            section = Section(title='Test section 5', job=job)
            section.clean()
        assert (
            excinfo.value.message
            == 'maximum number of sections already registered'
        )


class TestItem:
    def test_str_return(self):
        obj = baker.prepare(Item)
        assert obj.item == str(obj)

    def test_create_item(self, db):
        job = baker.make(Job)
        section = baker.make(Section, job=job, title='Test section')
        item = Item.objects.create(item='Test item', section=section)
        assert item.clean() is None
        assert item.item == 'Test item'
        assert item.section == section

    def test_create_max_items(self, db):
        section = baker.make(Section)
        baker.make(Item, section=section, _quantity=5)
        with raises(ValidationError) as excinfo:
            item = Item(item='Test item 5', section=section)
            item.clean()
        assert (
            excinfo.value.message
            == 'maximum number of itens already registered'
        )
