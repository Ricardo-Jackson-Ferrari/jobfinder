from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def send_recovery_email(email: str) -> bool:
    subject = _('Recovery Account - Change Password')
    user = User.objects.filter(email=email)

    if not user.exists():
        raise ObjectDoesNotExist(_('Não existe um usuário com este email.'))

    user = user.first()
    link = generate_change_password_link(user)

    context = {
        'name': user.first_name,
        'link': link,
    }

    html_content = render_to_string('account/emails/recovery_email.html', context)
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    send_email = EmailMultiAlternatives(subject, text_content, from_email, [email])
    send_email.attach_alternative(html_content, 'text/html')

    return send_email.send()


def generate_change_password_link(user: User) -> str:
    # TODO: Terminar lógica de geração do link para troca de senha.
    return f'http://localhost:8000?name={user.first_name}'