import api from './api'

export const bookService = {
    // Get books
    getBooks: async () => {
        const response = await api.get('/books');
        return response.data;
    },

    // Get book by ISBN
    getBookByIsbn: async (isbn13) => {
        const response = await api.get(`/books/${isbn13}`);
        return response.data;
    },

    // Search books
    searchBooks: async (query, limit = 10) => {
        const response = await api.get(`/search?q=${encodeURIComponent(query)}&limit=${limit}`);
        return response.data;
    },

    // Get recommendations
    getRecommendations: async (requestData) => {
        const response = await api.post('/recommendations', requestData);
        return response.data;
    },

    // Get categories
    getCategories: async () => {
        const response = await api.get('categories');
        return response.data;
    }
};