import os
import logging
from abc import ABC, abstractmethod

from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class BaseGrader(ABC):

    @abstractmethod
    def grade(self, expected: str, actual: str) -> float:
        """
        Compare expected answer and actual answer.
        Returns a score between 0.0 and 1.0.
        """
        pass


class MockGrader(BaseGrader):
    def grade(self, expected: str, actual: str) -> float:
        if not expected or not actual:
            return 0.0

        try:
            # Simple exact match check first for efficiency
            if expected.strip().lower() == actual.strip().lower():
                return 1.0

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([expected, actual])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error in MockGrader: {e}")
            return 0.0


class LLMGrader(BaseGrader):
    def __init__(self):
        api_key = getattr(settings, 'GOOGLE_API_KEY', os.getenv('GOOGLE_API_KEY'))
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            logger.warning("GOOGLE_API_KEY not found. LLMGrader will fail or return default scores.")

    def grade(self, expected: str, actual: str) -> float:
        if not self.model:
            logger.error("LLMGrader is not configured with an API key.")
            return 0.0

        prompt = (
            f"You are an automated grading assistant. \n"
            f"Expected Answer: {expected}\n"
            f"Student Answer: {actual}\n"
            f"Grade the student's answer based on the expected answer. "
            f"Return ONLY a numeric score between 0.0 and 1.0. "
            f"0.0 means completely wrong, 1.0 means perfect match."
        )

        try:
            response = self.model.generate_content(prompt)
            score_text = response.text.strip()
            # simple parsing, assuming the LLM obeys instructions
            return float(score_text)
        except Exception as e:
            logger.error(f"Error in LLMGrader: {e}")
            return 0.0


class GradingFactory:
    @staticmethod
    def get_grader() -> BaseGrader:
        engine = getattr(settings, 'GRADING_ENGINE', 'MOCK')

        if engine == 'LLM':
            return LLMGrader()
        else:
            return MockGrader()
