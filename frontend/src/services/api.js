import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Request interceptor
api.interceptors.request.use((config) => {
    console.log('Making request to: ', config.url);
    return config;
}, (error) => Promise.reject(error));

// Response interceptor
api.interceptors.response.use((response) => response, (error) => {
    console.log('API Error: ', error.response?.data || error.message);
    return Promise.reject(error);
});

export default api;