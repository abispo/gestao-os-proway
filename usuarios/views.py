from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Perfil, Genero
from .validators import campos_nao_preenchidos

@login_required
def perfil(request: HttpRequest):

    if request.method == "GET":
        return render(
            request,
            "usuarios/perfil.html",
            {"generos": Genero.choices}
        )

    if request.method == "POST":

        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        data_de_nascimento = request.POST.get("data_de_nascimento")
        genero = request.POST.get("genero")
        endereco = request.POST.get("endereco")

        ha_campos_nao_preenchidos = campos_nao_preenchidos(nome, sobrenome, endereco)

        if ha_campos_nao_preenchidos:
            return render(
                request,
                "usuarios/perfil.html",
                {
                    "erros": ha_campos_nao_preenchidos,
                    "generos": Genero.choices
                }
            )
        
        user: User = request.user
        user.first_name = nome
        user.last_name = sobrenome

        perfil = Perfil.objects.filter(usuario_id=user.id).first()

        if not perfil:
            perfil_obj = Perfil.objects.create(
                data_nascimento=data_de_nascimento,
                genero=genero,
                endereco=endereco,
                usuario=user
            )
            user.perfil = perfil_obj

        else:
            user.perfil.data_nascimento = datetime.strptime(
                data_de_nascimento,
                "%Y-%m-%d"
            ).date()
            user.perfil.genero = genero
            user.perfil.endereco = endereco
            user.perfil.save()

        user.save()

        return redirect(reverse("usuarios:perfil"))