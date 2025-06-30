import os
from pathlib import Path
import numpy as np
import pandas as pd
from typing import List, Optional
from app.models.book import Book
from dotenv import load_dotenv

class BookService:
    def __init__(self):
        try:
            load_dotenv()
            # cwd = Path.cwd()
            # noCoverPath = f'{cwd.parent}\\cover-not-found.jpg'
            noCoverPath = "http://localhost:8000/static/cover-not-found.jpg"
            self.books = pd.read_csv('data/books_with_emotions.csv')
            self.books['isbn13'] = self.books['isbn13'].astype(str)
            # Generate large_thumbnail logic
            self.books["large_thumbnail"] = self.books["thumbnail"] + "&fife=w800"
            self.books["large_thumbnail"] = np.where(
                self.books["large_thumbnail"].isna(),
                noCoverPath,
                self.books["large_thumbnail"],
            )

            self.books_filtered = pd.DataFrame({'isbn13': self.books['isbn13'],
                                'title': self.books['title'],
                                'authors': self.books['authors'],
                                'description': self.books['description'],
                                'average_rating': self.books['average_rating'],      
                                'large_thumbnail': self.books['large_thumbnail'],
                                'simple_categories': self.books['simple_categories'],
                                'joy': self.books['joy'],
                                'surprise': self.books['surprise'],
                                'anger': self.books['anger'],
                                'fear': self.books['fear'],
                                'sadness': self.books['sadness']})
        except FileNotFoundError as e:
            print(e)
    
    def get_all_books(self) -> List[dict]:
        return self.books_filtered.to_dict('records')

    def get_book_by_isbn(self, isbn13: str) -> Optional[dict]:
        found_book_df = self.books_filtered[self.books_filtered['isbn13'] == isbn13]

        if found_book_df.empty:
            return None
        
        return found_book_df.iloc[0].to_dict()
    
    def search_books(self, query:str, limit: int = 10) -> List[dict]:
        title_match = self.books_filtered['title'].str.contains(query, case=False, na=False)
        authors_match = self.books_filtered['authors'].str.contains(query, case=False, na=False)

        combined_match = title_match | authors_match
        found_book_df = self.books_filtered[combined_match]

        limited_books_df = found_book_df.head(limit)
        results = limited_books_df.to_dict('records')

        return results