// Configuração da API para diferentes ambientes
const API_CONFIG = {
    development: {
        baseURL: 'http://localhost:5000/api',
        timeout: 10000
    },
    production: {
        baseURL: 'https://api-amar-assist.herokuapp.com/api', // Substitua pela URL real da API
        timeout: 15000
    }
};

// Detectar ambiente
const environment = window.location.hostname === 'localhost' ? 'development' : 'production';
const API_BASE_URL = API_CONFIG[environment].baseURL;
const API_TIMEOUT = API_CONFIG[environment].timeout;

// Função utilitária para fazer requisições à API
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        timeout: API_TIMEOUT
    };
    
    const requestOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, requestOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Exportar configurações globalmente
window.API_BASE_URL = API_BASE_URL;
window.apiRequest = apiRequest;

