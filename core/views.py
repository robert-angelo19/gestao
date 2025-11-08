from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Empresa, Projeto
from .forms import EmpresaForm, ProjetoForm
from django.db.models import Q
from django.contrib.auth.models import User
from .forms_user import UserForm, UserEditForm

@login_required
def dashboard(request):
    empresas = Empresa.objects.filter(
        Q(criador=request.user) | 
        Q(projetos__membros=request.user) |
        Q(projetos__criador=request.user)
    ).distinct()
    
    # determinar papel em cada empresa
    empresas_com_papel = []
    for empresa in empresas:
        papel = None
        
        if empresa.criador == request.user:
            papel = 'criador_empresa'
        else:
            # se é criador de algum projeto
            if empresa.projetos.filter(criador=request.user).exists():
                papel = 'criador_projeto'
            # verificar se é membro de algum projeto
            elif empresa.projetos.filter(membros=request.user).exists():
                papel = 'membro_projeto'
        
        empresas_com_papel.append({
            'empresa': empresa,
            'papel': papel
        })
    
    return render(request, 'core/dashboard.html', {
        'empresas_com_papel': empresas_com_papel
    })

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
            return redirect('core:empresa_detail', pk=empresa.pk)
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
        # espera um array com ids de usuarios
        membros_ids = request.POST.getlist('membros')

        #garantir que o criador sempre seja membro
        if str(projeto.criador.id) not in membros_ids:
            membros_ids.append(str(projeto.criador.id))

        projeto.membros.set(membros_ids)
        messages.success(request, 'Membros atualizados.')
        return redirect('core:projeto_detail', pk=pk)
    # GET
    all_users = User.objects.all()
    return render(request, 'core/projetos/membros.html', {'projeto': projeto, 'all_users': all_users})

#verificar se é superuser
def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(
        lambda u: u.is_superuser,
        login_url='/',
        redirect_field_name=None
    )(view_func))
    return decorated_view_func

@superuser_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'core/users/list.html', {'users': users})

@superuser_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            return redirect('core:user_list')
    else:
        form = UserForm()
    return render(request, 'core/users/form.html', {'form': form})

@superuser_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'core/users/detail.html', {'user_obj': user})

@superuser_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
            return redirect('core:user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'core/users/form.html', {'form': form})

@superuser_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuário {username} excluído com sucesso!')
        return redirect('core:user_list')
    return render(request, 'core/users/confirm_delete.html', {'user_obj': user})

@login_required
def projeto_create_global(request):
    "cria projeto vendo qualquer empresa"
    if request.method == 'POST':
        form = ProjetoForm(request.POST, user=request.user)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.criador = request.user
            projeto.save()
            form.save_m2m()
            messages.success(request, 'Projeto criado.')
            return redirect('core:empresa_detail', pk=projeto.empresa.pk)
    else:
        form = ProjetoForm(user=request.user)
        form.fields['empresa'].queryset = Empresa.objects.all()
    return render(request, 'core/projetos/form.html', {'form': form})