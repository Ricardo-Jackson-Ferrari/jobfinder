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


class TestSection:
    def test_str_return(self):
        obj = baker.prepare(Section)
        assert obj.title == str(obj)


class TestItem:
    def test_str_return(self):
        obj = baker.prepare(Item)
        assert obj.item == str(obj)
