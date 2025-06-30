import { useState, useEffect } from 'react'
import { bookService } from './services/bookService'
import { BookCard } from './components/book'
import { Loading, ErrorMessage } from './components/common'
import { SearchForm, RecommendationForm } from './components/search'
import './App.css'

function App() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentView, setCurrentView] = useState('browse') // 'browse', 'search', 'recommendations'
  const [searchResults, setSearchResults] = useState([])
  const [recommendations, setRecommendations] = useState([])

  // Load initial books
  useEffect(() => {
    fetchInitialBooks()
  }, [])

  const fetchInitialBooks = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await bookService.getBooks()
      setBooks(data)
      setCurrentView('browse')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (query) => {
    if (!query) {
      setCurrentView('browse')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const results = await bookService.searchBooks(query, 20)
      setSearchResults(results)
      setCurrentView('search')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleGetRecommendations = async (formData) => {
    setLoading(true)
    setError(null)
    try {
      const results = await bookService.getRecommendations(formData)
      setRecommendations(results)
      setCurrentView('recommendations')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleBookClick = (book) => {
    alert(`Book: ${book.title}\nISBN: ${book.isbn13}\nRating: ${book.average_rating}`)
    // TODO: Implement book details modal or page
  }

  const getCurrentBooks = () => {
    switch (currentView) {
      case 'search':
        return searchResults
      case 'recommendations':
        return recommendations
      default:
        return books
    }
  }

  const getCurrentTitle = () => {
    switch (currentView) {
      case 'search':
        return `Search Results (${searchResults.length} found)`
      case 'recommendations':
        return `Recommendations for You (${recommendations.length} books)`
      default:
        return 'Featured Books'
    }
  }

  if (error && currentView === 'browse' && books.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <ErrorMessage
          message={error}
          onRetry={fetchInitialBooks}
        />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            📚 Book Recommender
          </h1>
          <p className="text-gray-600 text-lg">
            Discover your next favorite book with AI-powered recommendations
          </p>
        </div>

        {/* Search Form */}
        <div className="mb-8">
          <SearchForm onSearch={handleSearch} loading={loading} />
        </div>

        {/* Recommendation Form */}
        <div className="mb-8">
          <RecommendationForm onGetRecommendations={handleGetRecommendations} loading={loading} />
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-gray-700">
              {getCurrentTitle()}
            </h2>
            {currentView !== 'browse' && (
              <button
                onClick={() => setCurrentView('browse')}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                ← Back to Browse
              </button>
            )}
          </div>

          {loading && <Loading message="Loading books..." />}

          {error && currentView !== 'browse' && (
            <ErrorMessage message={error} showRetry={false} />
          )}

          {/* Books Grid */}
          {!loading && getCurrentBooks().length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {getCurrentBooks().map((book, index) => (
                <BookCard
                  key={`${book.isbn13}-${index}`}
                  book={book}
                  onClick={handleBookClick}
                />
              ))}
            </div>
          )}

          {!loading && getCurrentBooks().length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg">No books found</p>
              <p className="text-sm">Try adjusting your search or recommendation criteria</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App