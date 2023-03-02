from django import template
from django.test import RequestFactory
from job.templatetags.pagination_tags import url_replace

factory = RequestFactory()


class TestUrlReplace:
    def test_url_replace_tag(self):
        # Setup
        request = factory.get('/some-path/?foo=bar&baz=qux')
        context = template.Context({'request': request})

        # Execution
        result = url_replace(request, 'foo', 'new-bar')
        rendered_result = template.Template(result).render(context)

        # Assertion
        assert rendered_result == 'foo=new-bar&baz=qux'
