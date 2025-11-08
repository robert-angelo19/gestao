document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript carregado! Todas as funcionalidades ativas.');
    
    //confirmacao de exclusao
    setupDeleteConfirmations();
    
    //busca em gerenciar membros
    setupMemberSearch();
    
    //feedback do forms
    setupFormFeedback();
    
    //contador de membros
    setupMemberCounter();
    
    //mensagens auto
    setupAutoHideMessages();
});

//confirmacao de exclusao
function setupDeleteConfirmations() {
    const deleteForms =document.querySelectorAll('form[action*="excluir"]');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let itemName = '';
            let itemType = '';
            
            if (form.action.includes('empresa')) {
                itemType = 'empresa';
                itemName= form.querySelector('b') ? form.querySelector('b').textContent :'esta empresa';
            } else if (form.action.includes('projeto')) {
                itemType = 'projeto'; 
                itemName =form.querySelector('b')? form.querySelector('b').textContent : 'este projeto';
            }
            
            const confirmMessage = `Tem certeza que deseja excluir ${itemName}?\n\nEsta ação NÃO pode ser desfeita!`;
            
            if(!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });
    
    //estilo botao excluir
    const deleteButtons = document.querySelectorAll('form[action*="excluir"] button');
    deleteButtons.forEach(button => {
        button.style.cssText = `
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s ease;
        `;
        
        button.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#c82333';
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseout', function() {
            this.style.backgroundColor = '#dc3545';
            this.style.transform = 'scale(1)';
        });
    });
}

//busca membros
function setupMemberSearch() {
    const memberCheckboxes = document.querySelectorAll('input[name="membros"]');
    if (memberCheckboxes.length === 0) return;
    
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = '🔍 Buscar usuários...';
    searchInput.style.cssText = `
        margin-bottom: 15px;
        padding: 8px;
        width: 100%;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
    `;
    
    const form = memberCheckboxes[0].closest('form');
    form.parentNode.insertBefore(searchInput, form);
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const labels = document.querySelectorAll('form label');
        
        labels.forEach(label => {
            const username = label.textContent.toLowerCase();
            const shouldShow = username.includes(searchTerm);
            label.style.display = shouldShow ? 'block' : 'none';
        });
    });
}

//feedback forms
function setupFormFeedback() {
    const forms = document.querySelectorAll('form:not([action*="excluir"])');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = '⏳ Salvando...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
            }
        });
    });
}

//contador membros
function setupMemberCounter() {
    const checkboxes = document.querySelectorAll('input[name="membros"]');
    if (checkboxes.length === 0) return;
    
    const counter = document.createElement('div');
    counter.style.cssText = `
        margin: 10px 0;
        padding: 8px;
        background: #e9ecef;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
    `;
    
    const form = checkboxes[0].closest('form');
    form.parentNode.insertBefore(counter, form);
    
    function updateCounter() {
        const selected = document.querySelectorAll('input[name="membros"]:checked').length;
        const total = checkboxes.length;
        counter.textContent = `✅ ${selected} de ${total} membro(s) selecionado(s)`;
        counter.style.background = selected > 0 ? '#d4edda' : '#e9ecef';
    }
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateCounter);
    });
    
    updateCounter();
}

//mensagens automaticas
function setupAutoHideMessages() {
    const messages = document.querySelectorAll('ul li');
    
    messages.forEach(message => {
        if (message.textContent.includes('sucesso') || 
            message.textContent.includes('criado') ||
            message.textContent.includes('atualizado')) {
            
            setTimeout(() => {
                message.style.transition = 'opacity 0.5s ease';
                message.style.opacity = '0';
                setTimeout(() => {
                    if (message.parentNode) {
                        message.remove();
                    }
                }, 500);
            }, 4000);
        }
    });
}