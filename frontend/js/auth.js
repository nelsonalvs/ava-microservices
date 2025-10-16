// js/auth.js - Funções de autenticação

const API_BASE = 'http://localhost:8000/auth';

// Salvar token no localStorage
function saveToken(token) {
    localStorage.setItem('ava_token', token);
}

// Obter token do localStorage
function getToken() {
    return localStorage.getItem('ava_token');
}

// Fazer login
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');
    
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Login bem-sucedido
            saveToken(data.token);
            messageDiv.innerHTML = `<div class="success">✅ Login realizado com sucesso!</div>`;
            
            // Redirecionar para dashboard após 1 segundo
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
            
        } else {
            // Erro no login
            messageDiv.innerHTML = `<div class="error">❌ ${data.message}</div>`;
        }
        
    } catch (error) {
        messageDiv.innerHTML = `<div class="error">❌ Erro de conexão. Verifique se os serviços estão rodando.</div>`;
    }
}

// Registrar novo usuário
async function handleRegister(event) {
    event.preventDefault();
    
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const messageDiv = document.getElementById('register-message');
    
    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Registro bem-sucedido
            saveToken(data.token);
            messageDiv.innerHTML = `<div class="success">✅ Conta criada com sucesso!</div>`;
            
            // Redirecionar para dashboard após 1 segundo
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
            
        } else {
            // Erro no registro
            messageDiv.innerHTML = `<div class="error">❌ ${data.message}</div>`;
        }
        
    } catch (error) {
        messageDiv.innerHTML = `<div class="error">❌ Erro de conexão. Verifique se os serviços estão rodando.</div>`;
    }
}

// Verificar se usuário está logado
function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Fazer logout
function logout() {
    localStorage.removeItem('ava_token');
    window.location.href = 'index.html';
}