from abc import ABC, abstractmethod
from typing import Optional


class BaseScraper(ABC):

    def __init__(self, save_dir, top_k, num_workers):
        self.save_dir = save_dir
        self.top_k = top_k
        self.num_workers = num_workers

    @abstractmethod
    def extract_content(self, url):
        """Extract content from the url."""

    @abstractmethod
    def extract_urls(self, url):
        """Extract all urls of type from a top url."""

    @abstractmethod
    def scrape(article_type, url: Optional[str] = None):
        """Start scraping process of all news contents."""
