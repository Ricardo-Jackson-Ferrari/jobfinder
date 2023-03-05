from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


def validate_file_size(value):
    upload_size = settings.MAX_UPLOAD_SIZE
    filesize = value.size

    if filesize > upload_size:
        raise ValidationError(
            _(
                f'You cannot upload file more than {filesizeformat(upload_size)}'
            )
        )
    else:
        return value
