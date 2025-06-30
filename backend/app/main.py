from pathlib import Path
from app.models.book import Book
from typing import List, Optional
from app.services.book_service import BookService
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import RecommendationService

app = FastAPI(title='Book Recommender API',
              description='AI-powered book recommendation system',
              version='1.0.0')

# Global variables for service
book_service = BookService()
recommendation_service = RecommendationService()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:5173'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Add mount static files directory
noCoverPath = Path.cwd()
app.mount('/static', StaticFiles(directory=noCoverPath), name='static')

# Helper function to check service availability in the route
def check_service_availability(service_instance, service_name: str):
    if service_instance is None:
        raise HTTPException(
            status_code=500,
            detail=f"{service_name} not available. Server internal error. Please check server logs for initialization errors."
        )


# --- ROUTES HERE ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Recommender API!"}


@app.get('/books', response_model=List[Book])
def get_books():
    check_service_availability(book_service, "BookService")
    books = book_service.get_all_books()
    return books[:20]


@app.get('/books/{isbn13}', response_model=Book)
def get_book_by_isbn(isbn13: str):
    check_service_availability(book_service, "BookService")

    if not isbn13.strip():
        raise HTTPException(status_code=400, detail="ISBN13 cannot be empty.")
    if len(isbn13) != 13 or not isbn13.isdigit():
        raise HTTPException(status_code=400, detail="ISBN13 must be a 13-digit number string.")

    book = book_service.get_book_by_isbn(isbn13)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail='Book not found')
    

@app.get('/search', response_model=List[Book])
def search_books(q: str = Query(..., min_length=1, description="Search query for book titles or authors."), 
                 limit: int = Query(10, gt=0, description="Maximum number of search results to return.")):
    check_service_availability(book_service, "BookService")
    
    results = book_service.search_books(q, limit)
    return results


@app.post('/recommendations', response_model=List[Book])
def recommendation_request(request: RecommendationRequest):
    check_service_availability(recommendation_service, "RecommendationService")

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query for recommendations cannot be empty.")
    
    valid_categories = ["All", "Fiction", "Nonfiction", "Children's Fiction", "Children's Nonfiction"]
    valid_tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

    if request.category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category: '{request.category}'. Valid categories are: {', '.join(valid_categories)}")
    if request.tone not in valid_tones:
        raise HTTPException(status_code=400, detail=f"Invalid tone: '{request.tone}'. Valid tones are: {', '.join(valid_tones)}")
    
    if request.initial_top_k <= 0:
        raise HTTPException(status_code=400, detail="initial_top_k must be greater than 0.")
    if request.final_top_k <= 0:
        raise HTTPException(status_code=400, detail="final_top_k must be greater than 0.")
    if request.final_top_k > request.initial_top_k:
        raise HTTPException(status_code=400, detail="final_top_k cannot be greater than initial_top_k.")

    recommended_books = recommendation_service.get_semantic_recommendations(
        query=request.query,
        category=request.category,
        tone=request.tone,
        initial_top_k=request.initial_top_k,
        final_top_k=request.final_top_k
    )
    
    return recommended_books


@app.get("/categories")
def get_categories():
    return {
        "categories": ["All", "Fiction", "Nonfiction", "Children's Fiction", "Children's Nonfiction"],
        "tones": ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]
    }