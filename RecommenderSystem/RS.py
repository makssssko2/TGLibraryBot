import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
from typing import List, Type, Any, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from DB.models import Base, Books, Users, UserShelf
from DB.TypedDict.BooksTypedDict import BookInfoTypedDict
from joblib import dump, load
import os

nltk.download('stopwords')
russian_stop_words = stopwords.words('russian')


class RecommenderSystem:
    def __init__(self, db_url='sqlite:///AI.db'):
        self.__engine = create_engine(db_url)
        Base.metadata.create_all(self.__engine)
        self.__sessionmaker = sessionmaker(bind=self.__engine)
        self.tfidf_matrix = None
        self.tfidf = TfidfVectorizer(stop_words=russian_stop_words)
        self.df = None
        self.model_filename = 'tfidf_model.joblib'
        self.update_model()

    def update_model(self, force_update=False):
        """Обновляет модель TF-IDF на основе данных из базы данных.
        Если force_update=True или модель не найдена на диске, модель будет перестроена и сохранена.
        """

        if not force_update:
            try:
                self.tfidf_matrix, self.tfidf, self.df = load(self.model_filename)
                print("Модель TF-IDF загружена с диска.")
                return
            except FileNotFoundError:
                print("Модель TF-IDF не найдена. Создание новой модели...")

        with self.__sessionmaker() as session:
            books = session.query(Books.id, Books.description, Books.genres).all()
            self.df = pd.DataFrame(
                [(book.id, book.description, book.genres.split(',')) for book in books],
                columns=['id', 'description', 'genres_list']
            )
            books = []
            self.df['content'] = self.df['description'].fillna('') + ' ' + self.df[
                'genres_list'].apply(lambda x: ' '.join([str(i) for i in x]))
            self.tfidf_matrix = self.tfidf.fit_transform(self.df['content'])

        dump((self.tfidf_matrix, self.tfidf, self.df), self.model_filename)
        print("Модель TF-IDF сохранена на диск.")

    def get_recommendations(self, book_ids: List[int], top_n: int = 5) -> list[Any] | list[dict[str, int]]:
        """Возвращает рекомендации на основе списка ID прочитанных книг.

        Args:
            book_ids (List[int]): Список ID прочитанных книг.
            top_n (int, optional): Количество рекомендаций, которые нужно вернуть. По умолчанию 5.

        Returns:
            List[BookInfoTypedDict]: Список словарей с информацией о рекомендованных книгах.
        """

        if self.tfidf_matrix is None:
            return []

        book_indices = self.df[self.df['id'].isin(book_ids)].index

        if len(book_indices) == 0:
            return []

        user_profile = self.tfidf_matrix[book_indices].mean(axis=0)
        user_profile = np.asarray(user_profile)

        cosine_sim = cosine_similarity(user_profile, self.tfidf_matrix)

        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[len(book_ids):top_n + len(book_ids)]
        book_indices = [i[0] for i in sim_scores]
        recommended_books = self.df.iloc[book_indices]

        recommendations = []
        for _, book in recommended_books.iterrows():
            recommendations.append({
                "book_id": int(book['id']),
            })

        return recommendations
