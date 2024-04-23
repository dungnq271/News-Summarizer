from abc import ABC, abstractmethod
from typing import Optional


class BaseScraper(ABC):

    def __init__(
        self,
        output_dpath: str,
        top_recent: Optional[int] = None,
        num_workers: Optional[int] = 1,
    ):
        self.output_dpath = output_dpath
        self.top_recent = top_recent
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
