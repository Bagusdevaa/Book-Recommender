import React, { useState, useEffect } from 'react';
import { bookService } from '../../services/bookService';

const RecommendationForm = ({ onGetRecommendations, loading = false }) => {
  const [formData, setFormData] = useState({
    query: '',
    category: 'All',
    tone: 'All',
    final_top_k: 16
  });

  const [categories, setCategories] = useState([]);
  const [tones, setTones] = useState([]);

  // Fetch categories and tones on component mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const data = await bookService.getCategories();
        setCategories(data.categories || []);
        setTones(data.tones || []);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchOptions();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.query.trim() && onGetRecommendations) {
      onGetRecommendations(formData);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 space-y-4">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        🎯 Get Personalized Recommendations
      </h2>

      {/* Query Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Describe what you're looking for:
        </label>
        <textarea
          value={formData.query}
          onChange={(e) => handleChange('query', e.target.value)}
          placeholder="e.g., 'I want a thrilling mystery novel with complex characters' or 'Looking for inspiring non-fiction about leadership'"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
          rows={3}
          disabled={loading}
        />
      </div>

      {/* Category and Tone Filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category:
          </label>
          <select
            value={formData.category}
            onChange={(e) => handleChange('category', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mood/Tone:
          </label>
          <select
            value={formData.tone}
            onChange={(e) => handleChange('tone', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          >
            {tones.map(tone => (
              <option key={tone} value={tone}>{tone}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Results:
          </label>
          <select
            value={formData.final_top_k}
            onChange={(e) => handleChange('final_top_k', parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          >
            <option value={8}>8 books</option>
            <option value={16}>16 books</option>
            <option value={24}>24 books</option>
            <option value={32}>32 books</option>
          </select>
        </div>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={!formData.query.trim() || loading}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-300 text-white font-medium py-3 px-6 rounded-md transition-all duration-300 transform hover:scale-105 disabled:scale-100"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Getting Recommendations...
          </span>
        ) : (
          '✨ Get Recommendations'
        )}
      </button>
    </form>
  );
};

export default RecommendationForm;