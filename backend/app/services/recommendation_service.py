import os
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Optional
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv

class RecommendationService:
    def __init__(self):
        try:
            load_dotenv()
            # cwd = Path.cwd()
            # noCoverPath = f'{cwd.parent}\\cover-not-found.jpg'
            noCoverPath = "http://localhost:8000/static/cover-not-found.jpg"
            self.books = pd.read_csv('data/books_with_emotions.csv')
            self.vector_db_path = 'data/vector_db'
            self._setup_vector_database()

            self.books['isbn13'] = self.books['isbn13'].astype(str)

            self.books["large_thumbnail"] = self.books["thumbnail"] + "&fife=w800"
            self.books["large_thumbnail"] = np.where(
            self.books["large_thumbnail"].isna(),
            noCoverPath,
            self.books["large_thumbnail"],
            )

        except FileNotFoundError as e:
            print(e)
    
    def _setup_vector_database(self):
        if os.path.exists(self.vector_db_path):
            print('Loading existing vector database')

            self.db_books = Chroma(persist_directory=self.vector_db_path,
                                   embedding_function=OpenAIEmbeddings())
            
            print('Vector database loaded from cache!')
        else:
            print('creating new vector database (this will use OpenAI API)')
            # create new vector database
            raw_documents = TextLoader('data/tagged_description.txt', encoding='utf8').load()
            text_splitter = CharacterTextSplitter(separator='\n', chunk_size=0, chunk_overlap=0)
            documents = text_splitter.split_documents(raw_documents)
            self.db_books = Chroma.from_documents(documents,
                                                  OpenAIEmbeddings(),
                                                  persist_directory=self.vector_db_path)
 
            print('Vector database created and saved')

    def get_semantic_recommendations(self, query: str, category: str = 'All',
                                           tone: str = 'All', initial_top_k: int = 50 ,
                                           final_top_k: int = 16) -> List[dict]:
        
        print(f"\n--- Starting recommendation for query='{query}', category='{category}', tone='{tone}', limit={final_top_k} ---")
        
        # Check if DB is ready and has documents
        if self.db_books is None:
            print("self.db_books is None. Cannot perform similarity search.")
            return []

        try:
            # Do a similarity search
            recs = self.db_books.similarity_search(query, k=initial_top_k)
            if not recs:
                return []

            # Extract ISBN and convert to string
            books_list = []
            for rec in recs:
                try:
                    isbn = str(rec.page_content.strip('"').split()[0])
                    books_list.append(isbn)
                except IndexError:
                    print(f"WARNING: Could not parse ISBN from page_content: '{rec.page_content}'")
                    continue

            # Filter books by ISBN found
            book_recs = self.books[self.books["isbn13"].isin(books_list)]
            if book_recs.empty:
                print("No matching books found in main DataFrame after ISBN filter.")
                return []

            # Take initial_top_k from ISBN filter result (if not already sliced)
            book_recs = book_recs.head(initial_top_k)

            # Category Filter
            if category != "All":
                # Make sure 'simple_categories' exists and its data type is consistent
                if "simple_categories" in book_recs.columns:
                    # Also make sure the category of the input is the exact same string.
                    book_recs = book_recs[book_recs["simple_categories"].astype(str) == category]
                else:
                    print("WARNING: 'simple_categories' column not found for category filtering.")

            # Filter tone (sorting)
            if tone != "All":
                sort_col = ""
                if tone == "Happy": sort_col = "joy"
                elif tone == "Surprising": sort_col = "surprise"
                elif tone == "Angry": sort_col = "anger"
                elif tone == "Suspenseful": sort_col = "fear"
                elif tone == "Sad": sort_col = "sadness"
                
                if sort_col and sort_col in book_recs.columns:
                    book_recs.sort_values(by=sort_col, ascending=False, inplace=True)
                else:
                    print(f"WARNING: Tone '{tone}' selected, but column '{sort_col}' not found or invalid. Skipping tone sort.")

            # Apply final_top_k
            book_recs = book_recs.head(final_top_k)
            
            # Select the relevant columns and return
            relevant_columns = ['isbn13', 'title', 'authors', 'description', 'simple_categories', 'average_rating', 'large_thumbnail']
            for col in ['joy', 'surprise', 'anger', 'fear', 'sadness']:
                 if col in self.books.columns: relevant_columns.append(col)
            
            cols_to_return = [col for col in relevant_columns if col in book_recs.columns]
            
            results = book_recs[cols_to_return].to_dict('records')
            return results
        
        except Exception as e:
            print(f"ERROR: An error occurred during semantic recommendations: {e}")
            import traceback
            traceback.print_exc() 
            return []