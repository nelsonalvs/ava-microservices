// js/recommendations.js - Sistema Avançado de Recomendações

const RECOMMENDATION_API = 'http://localhost:8000/recommendation';

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
                user_id: 'user_' + Date.now(),
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

