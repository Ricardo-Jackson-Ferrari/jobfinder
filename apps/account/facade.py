from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def send_recovery_email(email: str) -> bool:
    subject = _('Password Reset Requested')
    user = User.objects.filter(email=email)

    if not user.exists():
        raise ObjectDoesNotExist(_('There is no user with this email.'))

    user = user.first()

    context = {
        'name': user.first_name,
        'domain': settings.DOMAIN,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }

    html_content = render_to_string(
        'account/emails/recovery_email.html', context
    )
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    send_email = EmailMultiAlternatives(
        subject, text_content, from_email, [email]
    )
    send_email.attach_alternative(html_content, 'text/html')
    try:
        send_email.send()
        return True
    except BadHeaderError:
        return False
