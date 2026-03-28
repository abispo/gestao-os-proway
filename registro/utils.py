from django.core.mail import send_mail
from django.http.request import HttpRequest
from django.urls import reverse

from .models import PreRegistro

def enviar_email(request: HttpRequest, pre_registro: PreRegistro):
    mensagem_email = """
Você recebeu esse e-mail pois você ou alguém fez um pré-registro no sistema de gestão de OS.
Caso queira confirmar o registro, clique no link a seguir.
Caso não tenha sido você que fez o pré-registro, apenas ignore esse e-mail.

{}{}{}""".format(
    'https://' if request.is_secure() else 'http://',
    request.get_host(),
    reverse('registro:confirmar_registro', args=(pre_registro.token,))
)

    send_mail(
        subject='Link de confirmação de pré-registro',
        message=mensagem_email,
        from_email='admin@localhost',
        recipient_list=[pre_registro.email]
    )
