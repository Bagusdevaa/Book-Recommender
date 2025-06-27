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
            self.books = pd.read_csv('data/books_with_emotions.csv')
            self.books['isbn13'] = self.books['isbn13'].astype(str)

            self.books["large_thumbnail"] = self.books["thumbnail"] + "&fife=w800"
            self.books["large_thumbnail"] = np.where(
            self.books["large_thumbnail"].isna(),
            "cover-not-found.jpg",
            self.books["large_thumbnail"],
            )

            self.raw_documents = TextLoader("data/tagged_description.txt", encoding='utf-8').load()
            self.text_splitter = CharacterTextSplitter(separator="\n", chunk_size=0, chunk_overlap=0)
            self.documents = self.text_splitter.split_documents(self.raw_documents)
            self.db_books = Chroma.from_documents(self.documents, OpenAIEmbeddings())

        except FileNotFoundError as e:
            print(e)
    
    async def get_semantic_recommendations(self, query: str, category: str = 'All',
                                     tone: str = 'All',initial_top_k: int = 50 ,
                                     final_top_k: int = 16) -> List[dict]:
            
            recs = await self.db_books.similarity_search(query, k=initial_top_k)
            books_list = [str(rec.page_content.strip('"').split()[0]) for rec in recs]
            book_recs = self.books[self.books["isbn13"].isin(books_list)].head(initial_top_k)

            if category != "All":
                book_recs = book_recs[book_recs["simple_categories"] == category].head(final_top_k)
            else:
                book_recs = book_recs.head(final_top_k)

            if tone == "Happy":
                book_recs.sort_values(by="joy", ascending=False, inplace=True)
            elif tone == "Surprising":
                book_recs.sort_values(by="surprise", ascending=False, inplace=True)
            elif tone == "Angry":
                book_recs.sort_values(by="anger", ascending=False, inplace=True)
            elif tone == "Suspenseful":
                book_recs.sort_values(by="fear", ascending=False, inplace=True)
            elif tone == "Sad":
                book_recs.sort_values(by="sadness", ascending=False, inplace=True)

            return book_recs.to_dict('records')