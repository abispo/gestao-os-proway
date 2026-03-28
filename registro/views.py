from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from . import forms
from .models import PreRegistro
from .utils import enviar_email
from .validators import (
    todos_dados_foram_preenchidos,
    nome_de_usuario_ja_existe,
    senhas_nao_sao_iguais
)

# Apesar de não ser obrigatório, podemos indicar o tipo dos parâmetros de funções e também o tipo de retorno. Muitos consideram uma boa prática, e é muito útil também no uso de IDEs que não conseguem automaticamente inferir o tipo de dado que está sendo tratado.
def pre_registro(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(
            request,
            "registro/pre_registro.html",
            {"form": forms.PreRegistroForm}
        )
    
    elif request.method == "POST":
        form = forms.PreRegistroForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            erros = []

            pre_registro_valido_ja_existe = PreRegistro.objects.filter(
                email=email, valido=True
            ).exists()

            if pre_registro_valido_ja_existe:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Já existe um pré-registro com esse e-mail, finalize ou aguarde o link expirar."
                )

            usuario_ja_registrado = User.objects.filter(
                email=email
            ).exists()

            if usuario_ja_registrado:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Já existe um registro com esse e-mail. Escolha outro."
                )

            if messages.get_messages(request):
                return render(
                    request,
                    "registro/pre_registro.html",
                    {
                        "form": forms.PreRegistroForm,
                    }
                )
            
            else:
                pre_registro = PreRegistro(email=email)
                pre_registro.save()

                enviar_email(request, pre_registro)

                return redirect(reverse(
                    "registro:envio_email_pre_registro"
                ))
            
            User.objects.create_user()

def envio_email_pre_registro(request):
    return render(
        request,
        "registro/envio_email_pre_registro.html"
    )

def confirmar_registro(request: HttpRequest, token: str):

    if request.method == "GET":

        pre_registro = PreRegistro.objects.filter(
            token=token, valido=True
        ).first()

        if not pre_registro:
            return render(
                request,
                "registro/pre_registro_invalido.html"
            )
        
        pre_registro_expirado = (
            timezone.now() - pre_registro.criado_em
        ).total_seconds() > settings.LIMITE_CONFIRMACAO_PRE_REGISTRO

        if pre_registro_expirado:
            pre_registro.valido = False
            pre_registro.save()

            return render(
                request,
                "registro/pre_registro_expirado.html"
            )

        return render(
            request,
            "registro/confirmar_registro.html",
            {
                "pre_registro": pre_registro
            }
        )
    
    elif request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        nome_de_usuario = request.POST.get("nome_de_usuario")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        pre_registro = PreRegistro.objects.filter(
            token=token, valido=True
        ).first()

        dados_preenchidos = todos_dados_foram_preenchidos(
            nome, sobrenome, nome_de_usuario, email, senha, confirmar_senha
        )

        if not dados_preenchidos:
            messages.add_message(
                request,
                messages.ERROR,
                "Você deve preencher todos os dados do formulário."
            )

        username_ja_existe = nome_de_usuario_ja_existe(nome_de_usuario)
        if username_ja_existe:
            messages.add_message(
                request,
                messages.ERROR,
                "O nome de usuário informado já existe. Escolha outro."
            )

        if senhas_nao_sao_iguais(senha, confirmar_senha):
            messages.add_message(
                request,
                messages.ERROR,
                "A senha e a confirmação da senha não conferem."
            )

        if messages.get_messages(request):
            return render(
                request,
                "registro/confirmar_registro.html",
                {
                    "pre_registro": pre_registro
                }
            )
        
        User.objects.create_user(
            username=nome_de_usuario,
            first_name=nome,
            last_name=sobrenome,
            email=email,
            password=senha
        )

        return redirect(reverse('registro:registro_confirmado'))
    
def pre_registro_invalido(request):
    return render(
        request,
        "registro/pre_registro_invalido.html"
    )

def pre_registro_expirado(request):
    return render(
        request,
        "registro/pre_registro_expirado.html"
    )

def registro_confirmado(request):
    return render(
        request,
        "registro/registro_confirmado.html"
    )
