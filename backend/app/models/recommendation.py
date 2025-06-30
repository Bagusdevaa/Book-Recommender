from pydantic import BaseModel
from typing import Optional

class RecommendationRequest(BaseModel):
    query: str
    category: Optional[str] = 'All'
    tone: Optional[str] = 'All'
    initial_top_k: Optional[int] = 50
    final_top_k: Optional[int] = 16