from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    isbn13: str
    title: str
    authors: str
    description: str
    average_rating: float     
    large_thumbnail: Optional[str] = None 
    simple_categories: Optional[str] = None 
    joy: Optional[float] = None
    surprise: Optional[float] = None
    anger: Optional[float] = None
    fear: Optional[float] = None
    sadness: Optional[float] = None