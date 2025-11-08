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
    const forms = document.querySelectorAll('form:not([action*="excluir"])');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = '⏳ Salvando...';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
                
                // Restaurar após 5 segundos (caso haja erro no envio)
                setTimeout(() => {
                    if (submitBtn.disabled) { // Se ainda estiver disabled, significa que não recarregou
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