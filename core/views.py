from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empresa, Projeto
from .forms import EmpresaForm, ProjetoForm
from django.db.models import Q
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    # mostra empresas q o user pode ver (que ele criou ou projetos q participa)
    empresas = Empresa.objects.filter(Q(criador=request.user) | Q(projetos__membros=request.user)).distinct()
    return render(request, 'core/dashboard.html', {'empresas': empresas})

# EMPRESA
@login_required
def empresa_list(request):
    #mostra empresas onde o user participa
    empresas = Empresa.objects.filter(Q(criador=request.user) | Q(projetos__membros=request.user)).distinct()
    return render(request, 'core/empresas/list.html', {'empresas': empresas})

@login_required
def empresa_create(request):
    #criar empresa
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.criador = request.user
            empresa.save()
            messages.success(request, 'Empresa criada.')
            return redirect('core:empresa_list')
    else:
        form = EmpresaForm()
    return render(request, 'core/empresas/form.html', {'form': form})

@login_required
def empresa_detail(request, pk):
    #mostrart projetos da empresa q o user pode ver
    empresa = get_object_or_404(Empresa, pk=pk)
    projetos = empresa.projetos.filter(Q(criador=request.user) | Q(membros=request.user)).distinct()
    return render(request, 'core/empresas/detail.html', {'empresa': empresa, 'projetos': projetos})

@login_required
def empresa_update(request, pk):
    #editar, só o criador
    empresa = get_object_or_404(Empresa, pk=pk)
    if empresa.criador != request.user:
        messages.error(request, 'Apenas o criador pode editar.')
        return redirect('core:empresa_detail', pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada.')
            return redirect('core:empresa_detail', pk=pk)
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'core/empresas/form.html', {'form': form})

@login_required
def empresa_delete(request, pk):
    #delete, só o criador
    empresa = get_object_or_404(Empresa, pk=pk)
    if empresa.criador != request.user:
        messages.error(request, 'Apenas o criador pode excluir.')
        return redirect('core:empresa_detail', pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa excluída.')
        return redirect('core:empresa_list')
    return render(request, 'core/empresas/confirm_delete.html', {'empresa': empresa})

# PROJETO
@login_required
def projeto_create(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST, user=request.user)  # ← Adicione user aqui
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.criador = request.user
            projeto.save()
            form.save_m2m()
            messages.success(request, 'Projeto criado.')
            return redirect('core:empresa_detail', pk=projeto.empresa.pk)
    else:
        form = ProjetoForm(user=request.user)  # ← E aqui também
    return render(request, 'core/projetos/form.html', {'form': form})

@login_required
def projeto_detail(request, pk):
    #ver projeto se for criador ou membro
    projeto = get_object_or_404(Projeto, pk=pk)
    # Verifica se o usuário tem visibilidade
    if not (projeto.criador == request.user or request.user in projeto.membros.all()):
        messages.error(request, 'Você não tem acesso a este projeto.')
        return redirect('core:dashboard')
    return render(request, 'core/projetos/detail.html', {'projeto': projeto})

@login_required
def projeto_update(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if projeto.criador != request.user:
        messages.error(request, 'Apenas o criador pode editar.')
        return redirect('core:projeto_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto, user=request.user)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado.')
            return redirect('core:projeto_detail', pk=pk)
    else:
        form = ProjetoForm(instance=projeto, user=request.user)  
    return render(request, 'core/projetos/form.html', {'form': form})

@login_required
def projeto_delete(request, pk):
    #deleta projeto, só o criador
    projeto = get_object_or_404(Projeto, pk=pk)
    if projeto.criador != request.user:
        messages.error(request, 'Apenas o criador pode excluir.')
        return redirect('core:projeto_detail', pk=pk)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, 'Projeto excluído.')
        return redirect('core:empresa_detail', pk=projeto.empresa.pk)
    return render(request, 'core/projetos/confirm_delete.html', {'projeto': projeto})

@login_required
def projeto_membros_manage(request, pk):
    #add/remove membros, só o criador 
    projeto = get_object_or_404(Projeto, pk=pk)
    if projeto.criador != request.user:
        messages.error(request, 'Apenas o criador pode gerenciar membros.')
        return redirect('core:projeto_detail', pk=pk)
    if request.method == 'POST':
        # Espera um array com ids de usuários
        membros_ids = request.POST.getlist('membros')
        projeto.membros.set(membros_ids)
        messages.success(request, 'Membros atualizados.')
        return redirect('core:projeto_detail', pk=pk)
    # GET
    all_users = User.objects.all()
    return render(request, 'core/projetos/membros.html', {'projeto': projeto, 'all_users': all_users})
