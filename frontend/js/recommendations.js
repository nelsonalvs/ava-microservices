// js/recommendations.js - Funções de recomendação

const RECOMMENDATION_API = 'http://localhost:8000/recommendation';

// Carregar recomendações
async function loadRecommendations() {
    const loadingDiv = document.getElementById('recommendations-loading');
    const listDiv = document.getElementById('recommendations-list');
    
    // Interesses padrão (poderia vir do perfil do usuário)
    const defaultInterests = ['python', 'beginner', 'programming'];
    
    try {
        loadingDiv.innerHTML = '<p>🔄 Buscando recomendações personalizadas...</p>';
        listDiv.innerHTML = '';
        
        const response = await fetch(`${RECOMMENDATION_API}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                user_id: 'user_' + Date.now(), // ID temporário
                interests: defaultInterests,
                top_n: 4
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            loadingDiv.innerHTML = '';
            
            if (data.recommendations && data.recommendations.length > 0) {
                data.recommendations.forEach(material => {
                    const materialCard = `
                        <div class="material-card">
                            <h4>${material.title}</h4>
                            <p><strong>Tipo:</strong> ${material.type} | <strong>Dificuldade:</strong> ${material.difficulty}</p>
                            <p>${material.description || 'Sem descrição'}</p>
                            <div class="tags">
                                ${material.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                        </div>
                    `;
                    listDiv.innerHTML += materialCard;
                });
            } else {
                listDiv.innerHTML = '<p>😔 Nenhuma recomendação encontrada para seus interesses.</p>';
            }
            
        } else {
            loadingDiv.innerHTML = `<div class="error">❌ Erro: ${data.error}</div>`;
        }
        
    } catch (error) {
        loadingDiv.innerHTML = '<div class="error">❌ Erro ao carregar recomendações. Verifique se o serviço está rodando.</div>';
    }
}

// Carregar todos os materiais
async function loadAllMaterials() {
    const materialsDiv = document.getElementById('all-materials');
    
    try {
        const response = await fetch(`${RECOMMENDATION_API}/materials`);
        const data = await response.json();
        
        if (response.ok) {
            materialsDiv.innerHTML = '<h4>Materiais Disponíveis:</h4>';
            
            data.materials.forEach(material => {
                const materialCard = `
                    <div class="material-card">
                        <h4>${material.title}</h4>
                        <p><strong>Tipo:</strong> ${material.type} | <strong>Dificuldade:</strong> ${material.difficulty}</p>
                        <p>${material.description || 'Sem descrição'}</p>
                        <div class="tags">
                            ${material.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    </div>
                `;
                materialsDiv.innerHTML += materialCard;
            });
            
        } else {
            materialsDiv.innerHTML = `<div class="error">❌ Erro ao carregar materiais</div>`;
        }
        
    } catch (error) {
        materialsDiv.innerHTML = '<div class="error">❌ Erro de conexão</div>';
    }
}

// Adicionar interesses
async function addInterests() {
    const interestsInput = document.getElementById('new-interests');
    const interestsDiv = document.getElementById('current-interests');
    
    const newInterests = interestsInput.value.split(',').map(i => i.trim()).filter(i => i);
    
    if (newInterests.length === 0) {
        alert('Por favor, digite pelo menos um interesse.');
        return;
    }
    
    interestsDiv.innerHTML = `<p>✅ Interesses adicionados: ${newInterests.join(', ')}</p>
                             <p><small>Recarregue as recomendações para ver os resultados.</small></p>`;
    
    interestsInput.value = '';
}