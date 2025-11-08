document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ JavaScript carregado - versão mínima e segura');
    
    // APENAS confirmações de exclusão básicas
    const deleteForms = document.querySelectorAll('form[action*="excluir"]');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let itemName = '';
            
            if (form.action.includes('empresa')) {
                itemName = form.querySelector('b') ? form.querySelector('b').textContent : 'esta empresa';
            } else if (form.action.includes('projeto')) {
                itemName = form.querySelector('b') ? form.querySelector('b').textContent : 'este projeto';
            }
            
            if (!confirm(`Tem certeza que deseja excluir ${itemName}?`)) {
                e.preventDefault();
            }
        });
    });
});