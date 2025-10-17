// js/recommendations.js - Sistema Avançado de Recomendações

const RECOMMENDATION_API = 'http://localhost:8000/recommendation';

// Carregar recomendações baseadas nas áreas selecionadas
// Carregar recomendações baseadas nas áreas selecionadas
async function loadRecommendations() {
    const loadingDiv = document.getElementById('recommendations-loading');
    const listDiv = document.getElementById('recommendations-list');
    const infoDiv = document.getElementById('recommendations-info');
    
    // Obter áreas selecionadas
    const selectedAreas = getSelectedAreas();
    
    if (selectedAreas.length === 0) {
        infoDiv.innerHTML = '<div class="error">⚠️ Selecione pelo menos uma área de interesse</div>';
        return;
    }
    
    try {
        loadingDiv.innerHTML = '<p>🔄 Buscando recomendações personalizadas...</p>';
        listDiv.innerHTML = '';
        infoDiv.innerHTML = `<p>🎯 Buscando recomendações para: <strong>${selectedAreas.join(', ')}</strong> no nível <strong>${getNivelText()}</strong></p>`;
        
        const response = await fetch(`${RECOMMENDATION_API}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                user_id: 'user_current',
                areas: selectedAreas,
                nivel: currentNivel,
                top_n: 8
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            loadingDiv.innerHTML = '';
            
            if (data.recommendations && data.recommendations.length > 0) {
                listDiv.innerHTML = `<h3>🎯 ${data.total_recommended} Recomendações Encontradas</h3>`;
                
                data.recommendations.forEach(material => {
                    const materialCard = `
                        <div class="material-card">
                            <h4>${material.image} ${material.title}</h4>
                            <p><strong>Autor:</strong> ${material.author} | <strong>Nível:</strong> ${material.difficulty}</p>
                            <p><strong>Páginas:</strong> ${material.pages} | <strong>Ano:</strong> ${material.year}</p>
                            <p>${material.description}</p>
                            <div class="tags">
                                ${material.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                            <div style="margin-top: 10px;">
                                <button onclick="addToBooklist(${material.id})" class="btn btn-primary" style="padding: 8px 15px; font-size: 14px;">
                                    ➕ Adicionar à Minha Lista
                                </button>
                            </div>
                        </div>
                    `;
                    listDiv.innerHTML += materialCard;
                });
            } else {
                listDiv.innerHTML = '<div class="error">😔 Nenhuma recomendação encontrada para suas áreas selecionadas.</div>';
            }
            
        } else {
            loadingDiv.innerHTML = `<div class="error">❌ Erro: ${data.error}</div>`;
        }
        
    } catch (error) {
        loadingDiv.innerHTML = '<div class="error">❌ Erro ao carregar recomendações. Verifique se o serviço está rodando.</div>';
    }
}

// Obter áreas selecionadas
function getSelectedAreas() {
    const areas = [];
    const checkboxes = document.querySelectorAll('.area-checkbox input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            areas.push(checkbox.value);
        }
    });
    
    return areas;
}

// Obter texto do nível
function getNivelText() {
    return currentNivel === 1 ? 'Iniciante' : currentNivel === 2 ? 'Intermediário' : 'Avançado';
}

// Carregar todas as áreas disponíveis (para debug)
async function loadAreas() {
    try {
        const response = await fetch(`${RECOMMENDATION_API}/areas`);
        const data = await response.json();
        console.log('Áreas disponíveis:', data.areas);
    } catch (error) {
        console.log('Erro ao carregar áreas:', error);
    }
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    loadAreas();
});

// ==================== FUNÇÕES DA LISTA PESSOAL ====================

// Carregar lista pessoal do usuário
async function loadMyBooklist() {
    const booklistDiv = document.getElementById('my-booklist');
    const user_id = 'user_current'; // Em produção, pegar do token JWT
    
    try {
        booklistDiv.innerHTML = '<p>🔄 Carregando sua lista...</p>';
        
        const response = await fetch(`${RECOMMENDATION_API}/user/${user_id}/booklist`);
        const data = await response.json();
        
        if (response.ok) {
            if (data.books && data.books.length > 0) {
                let html = `<h4>📚 Sua Lista (${data.total} livros)</h4>`;
                
                data.books.forEach(book => {
                    const statusIcons = {
                        'quero_ler': '📖 Quero Ler',
                        'lendo': '🔍 Lendo', 
                        'lido': '✅ Lido'
                    };
                    
                    html += `
                        <div class="material-card">
                            <h4>${book.material.image} ${book.material.title}</h4>
                            <p><strong>Autor:</strong> ${book.material.author} | <strong>Status:</strong> ${statusIcons[book.status]}</p>
                            <p><strong>Adicionado em:</strong> ${new Date(book.added_at).toLocaleDateString()}</p>
                            <p>${book.material.description}</p>
                            <div class="tags">
                                ${book.material.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                            <div style="margin-top: 10px;">
                                <button onclick="removeFromBooklist(${book.id})" class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px;">
                                    🗑️ Remover
                                </button>
                            </div>
                        </div>
                    `;
                });
                
                booklistDiv.innerHTML = html;
            } else {
                booklistDiv.innerHTML = '<p>😔 Sua lista está vazia. Adicione livros das recomendações!</p>';
            }
        } else {
            booklistDiv.innerHTML = `<div class="error">❌ Erro ao carregar lista</div>`;
        }
        
    } catch (error) {
        booklistDiv.innerHTML = '<div class="error">❌ Erro de conexão</div>';
    }
}

// Adicionar livro à lista pessoal
// Adicionar livro à lista pessoal
async function addToBooklist(materialId) {
    const user_id = 'user_current';
    
    try {
        const response = await fetch(`${RECOMMENDATION_API}/user/${user_id}/booklist`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                material_id: materialId,
                status: 'quero_ler'
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Livro adicionado à sua lista!');
            loadMyBooklist(); // Atualiza a lista
        } else {
            alert(`❌ Erro: ${data.error}`);
        }
        
    } catch (error) {
        alert('❌ Erro de conexão');
    }
}

// Remover livro da lista
async function removeFromBooklist(bookId) {
    const user_id = 'user_current';
    
    if (!confirm('Tem certeza que quer remover este livro da sua lista?')) {
        return;
    }
    
    try {
        const response = await fetch(`${RECOMMENDATION_API}/user/${user_id}/booklist/${bookId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Livro removido da sua lista!');
            loadMyBooklist(); // Atualiza a lista
        } else {
            alert(`❌ Erro: ${data.error}`);
        }
        
    } catch (error) {
        alert('❌ Erro de conexão');
    }
}