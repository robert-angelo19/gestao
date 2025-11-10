document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ JavaScript carregado - Fase 1 (Funcionalidades Seguras)');
    
    
    setupDeleteConfirmations();
    setupFormFeedback();
    setupAutoHideMessages();
});

//confim para exclusao
function setupDeleteConfirmations() {
    const deleteForms = document.querySelectorAll('form[action*="excluir"]');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let itemName = '';
            
            if (form.action.includes('empresa')) {
                itemName = form.querySelector('b') ? form.querySelector('b').textContent : 'esta empresa';
            } else if (form.action.includes('projeto')) {
                itemName = form.querySelector('b') ? form.querySelector('b').textContent : 'este projeto';
            }
            
            if (!confirm(`Tem certeza que deseja excluir ${itemName}?\n\nEsta ação NÃO pode ser desfeita!`)) {
                e.preventDefault();
            }
        });
    });
}

//feedback nos forms
function setupFormFeedback() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Pula forms de login e logout
        if (form.action.includes('/login/') || 
            form.action.includes('/logout/') ||
            form.querySelector('input[name="username"]') ||
            form.querySelector('input[name="password"]')) {
            return; // Skip login/logout forms
        }
        
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('logout-btn')) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = '⏳ Salvando...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
                
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.textContent = originalText;
                        submitBtn.disabled = false;
                        submitBtn.style.opacity = '1';
                    }
                }, 5000);
            }
        });
    });
}

//mensagens auto
function setupAutoHideMessages() {
    const messages = document.querySelectorAll('.messages li');
    
    messages.forEach(message => {
        // Apenas esconder mensagens de sucesso
        if (message.textContent.includes('sucesso') || 
            message.textContent.includes('Sucesso') ||
            message.textContent.includes('criado') ||
            message.textContent.includes('atualizado') ||
            message.textContent.includes('excluído')) {
            
            setTimeout(() => {
                message.style.transition = 'opacity 0.5s ease';
                message.style.opacity = '0';
                setTimeout(() => {
                    if (message.parentNode) {
                        message.style.display = 'none'; // Apenas esconder, não remover
                    }
                }, 500);
            }, 4000);
        }
    });
}