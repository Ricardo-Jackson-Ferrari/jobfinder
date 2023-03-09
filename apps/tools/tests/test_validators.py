from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from tools.validators import validate_file_size


def test_validate_file_size():
    max_upload_size = settings.MAX_UPLOAD_SIZE
    too_big_file_size = max_upload_size + 1
    _file = SimpleUploadedFile('test.txt', b'test content')
    valid_file_size = max_upload_size - 1

    result = validate_file_size(
        SimpleUploadedFile('test.txt', b'a' * valid_file_size)
    )
    assert result.name == _file.name

    try:
        validate_file_size(
            SimpleUploadedFile('test.txt', b'test content' * too_big_file_size)
        )
    except ValidationError as e:
        assert e.message == str(
            _(
                f'You cannot upload file more than {filesizeformat(max_upload_size)}'
            )
        )
