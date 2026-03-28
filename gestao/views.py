import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.request import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from .models import OrdemDeServico, StatusOrdemDeServico

def index(request: HttpRequest):
    return render(
        request,
        "gestao/index.html"
    )

def nova_ordem_de_servico(request: HttpRequest):

    if request.method == "GET":
        return render(
            request,
            "gestao/nova_ordem_de_servico.html"
        )
    
    elif request.method == "POST":

        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")

        os = OrdemDeServico(
            titulo=titulo,
            descricao=descricao,
            cliente=request.user
        )

        os.save()

        messages.success(
            request=request,
            message=f"Ordem de serviço #{os.pk} criada com sucesso."
        )

        return redirect(reverse("gestao:ordens_de_servico"))
    
def ordens_de_servico_atribuidas(request: HttpRequest):
    
    ordens_de_servico = OrdemDeServico.objects.filter(tecnico=request.user)

    return render(
        request,
        "gestao/lista_ordens.html",
        {"ordens_de_servico": ordens_de_servico}
    )


class OrdemDeServicoListView(LoginRequiredMixin, ListView):
    model = OrdemDeServico
    template_name = 'gestao/lista_ordens.html'
    context_object_name = 'ordens_de_servico'

    def get_queryset(self):
        """
        Docstring for get_queryset
        
        Estamos modificando o método herdado get_queryset. Abaixo é verificado se o usuário tem a permissão 'gestao.pode_visualizar_todas_os'. Se ele tiver, todos os dados da model serão mostrados. Se não, vamos filtrar apenas as ordens de serviço criadas pelo próprio usuário.
        """
        user = self.request.user

        if user.has_perm("gestao.pode_visualizar_todas_os"):
            return OrdemDeServico.objects.all()
        
        return OrdemDeServico.objects.filter(cliente=user)


class OrdemDeServicoDetailView(LoginRequiredMixin, DetailView):
    model = OrdemDeServico

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = StatusOrdemDeServico.choices

        return context
    

class OrdemDeServicoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrdemDeServico

    permission_required = 'gestao.change_ordemdeservico'
    fields = ['titulo', 'descricao']

    def post(self, request, *args, **kwargs):

        os_sendo_atribuida = request.POST.get("atribuir")
        os = get_object_or_404(OrdemDeServico, pk=kwargs.get("pk"))
        timestamp = datetime.datetime.now(datetime.timezone.utc)

        if os_sendo_atribuida:

            os.tecnico = request.user
            os.status = StatusOrdemDeServico.EM_ANDAMENTO.value

            descricao = f"""
    {os.descricao}
--- OS atribuída a {request.user} em {timestamp.strftime('%H:%M:%S %d/%m/%Y')} ----------------
"""
            os.descricao = descricao
            os.save()

        else:
            descricao = request.POST.get("descricao")
            status = request.POST.get("status")

            os.descricao = f"{descricao}\n\n---\nTicket fechado em {timestamp.strftime('%H:%M:%S %d/%m/%Y')} por {request.user}"
            os.status = status
            os.save()

        return redirect(reverse('gestao:ordens_de_servico'))
    
    def form_valid(self, form):
        return super().form_valid(form)
    