import os.path as osp
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from types import NoneType
from typing import List, Optional

import pandas as pd
import requests  # type: ignore
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.logger import log
from src.utils import calculate_time, create_dir, get_text_from_tag

from .base_scraper import BaseScraper

requests.packages.urllib3.util.connection.HAS_IPV6 = False


class VnExpressScraper(BaseScraper):
    def __init__(
        self,
        output_dpath: str,
        top_recent: Optional[int] = None,
        num_workers: Optional[int] = 1,
        postprocessors: Optional[List] = [],
        **kwargs,
    ):
        super().__init__(output_dpath, top_recent, num_workers)
        self.logger = log.get_logger(__name__)
        create_dir(self.output_dpath)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/81.0.4044.141 Safari/537.36"
        }
        self.base_url = "https://vnexpress.net/rss/{article_type}.rss"
        self.postprocessors = postprocessors

    @calculate_time
    def extract_content(self, url):
        """Extract content from the url."""
        self.logger.info(f"Start scraping contents from {url}...")
        content = requests.get(url, headers=self.headers).content
        soup = BeautifulSoup(content, "html.parser")

        try:
            title = soup.find("h1", class_="title-detail").text
        except AttributeError:
            self.logger.info(f"Title tag does no match in {url}...")
            title = None

        description = (
            get_text_from_tag(p)
            for p in soup.find("p", class_="description").contents
        )
        description = "\n\n".join(description)

        try:
            paragraphs = (
                get_text_from_tag(p)
                for p in soup.find_all("p", class_="Normal")
            )
            paragraphs = "\n\n".join(paragraphs)
        except AttributeError:
            self.logger.info(f"Paragraph tags does no match in {url}...")
            paragraphs = None

        contents = {
            "Link": url,
            "Title": title,
            "Description": description,
            "Full_text": paragraphs,
        }

        if self.postprocessors:
            for name, processor in self.postprocessors.items():
                output = processor.run(url, title, description, paragraphs)
                contents[name] = output

        return contents

    @calculate_time
    def extract_urls(self, url):
        """Extract all urls from a top url."""

        self.logger.info(f"Start extracting urls from {url}...")
        content = requests.get(
            url,
            headers=self.headers,
        ).content
        soup = BeautifulSoup(content, "html.parser")
        items = soup.find_all("item")
        urls = [item.find("guid").text for item in items]
        pubdates = [item.find("pubdate").text for item in items]

        return urls, pubdates

    def scrape(self, article_type, url=None):
        """Start scraping process of all news contents."""

        out_fpath = osp.join(self.output_dpath, article_type + ".csv")
        scrape_url = self.base_url.format(article_type=article_type)
        urls, pubdates = self.extract_urls(scrape_url)
        self.logger.info(f"Number of extracted urls: {len(urls)}.")
        self.scrape_multithread(urls, out_fpath, pubdates=pubdates)

    def scrape_multithread(self, urls, output_fpath, **kwargs):
        # cols = ["url", "title", "description", "full_text"]
        # news_df = {col: [] for col in cols}

        news_df = defaultdict(list)

        if self.top_recent:
            top_urls = deepcopy(urls[: self.top_recent])
            news_df["Time"] = kwargs["pubdates"][: self.top_recent]
        else:
            top_urls = deepcopy(urls)
            news_df["Time"] = kwargs["pubdates"]

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            for contents in tqdm(
                executor.map(self.extract_content, top_urls),
                total=len(top_urls),
                desc="URLs",
            ):
                # for i, content in enumerate(contents):
                for name, content in contents.items():
                    assert isinstance(content, (str, NoneType))
                    # news_df[cols[i]].append(content)
                    news_df[name].append(content)

        news_df = pd.DataFrame(news_df)
        news_df.to_csv(output_fpath, index=False)
        self.logger.info(f"Saved scraped news to {output_fpath}.")
