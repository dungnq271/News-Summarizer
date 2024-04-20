import os.path as osp
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests  # type: ignore
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.utils import create_dir, get_text_from_tag

from .base_scraper import BaseScraper


class VnExpressScraper(BaseScraper):
    def __init__(self, save_dir, top_k, num_workers):
        super().__init__(save_dir, top_k, num_workers)
        create_dir(self.save_dir)
        self.base_url = "https://vnexpress.net/rss/{article_type}.rss"

    def extract_content(self, url):
        """Extract content from the url."""
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        title = soup.find("h1", class_="title-detail").text
        description = (
            get_text_from_tag(p)
            for p in soup.find("p", class_="description").contents
        )
        paragraphs = (
            get_text_from_tag(p) for p in soup.find_all("p", class_="Normal")
        )
        return url, title, description, paragraphs

    def extract_urls(self, url):
        """Extract all urls from a top url."""

        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")
        items = soup.find_all("item")
        urls = [item.find("guid").text for item in items]
        pubdates = [item.find("pubdate").text for item in items]

        return urls, pubdates

    def scrape(self, article_type, url=None):
        """Start scraping process of all news contents."""

        out_fpath = osp.join(self.save_dir, article_type + ".csv")
        scrape_url = self.base_url.format(article_type=article_type)
        urls, pubdates = self.extract_urls(scrape_url)
        print(len(urls))
        self.process_multithread(urls, out_fpath, pubdates=pubdates)

    def process_multithread(self, urls, output_fpath, **kwargs):
        cols = ["url", "title", "description", "full_text"]
        news_df = {col: [] for col in cols}

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            for contents in tqdm(
                executor.map(self.extract_content, urls),
                total=len(urls),
                desc="URLs",
            ):
                for i, content in enumerate(contents):
                    news_df[cols[i]].append(content)

        news_df["pubdate"] = kwargs["pubdates"]
        news_df = pd.DataFrame(news_df)
        news_df.to_csv(output_fpath, index=False)
