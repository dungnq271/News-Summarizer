import argparse
import os

from dotenv import find_dotenv, load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI

from src.logger import log
from src.pipeline import NewsSummarizePipeline
from src.scraper import VnExpressScraper
from src.utils import utils

_ = load_dotenv(find_dotenv())  # read local .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # type: ignore


def main(config_fpath):
    config = utils.get_config(config_fpath)
    log.setup_logging(
        log_dir=config["output_dpath"], config_fpath=config["logger_fpath"]
    )
    # log.setup_request_logging()

    # Summarizer setup
    if config["summarize"]:
        llm = ChatOpenAI(
            temperature=0,
            # openai_api_key=openai_api_key,
            max_tokens=1000,
            model="gpt-3.5-turbo",
        )
        summarizer = NewsSummarizePipeline(
            llm=llm,
            splitter=CharacterTextSplitter(
                separator="\n\n", chunk_size=1000, chunk_overlap=100
            ),
        )

    # Scraper setup
    scraper = VnExpressScraper(
        postprocessors={"Summary": summarizer}, **config
    )

    # Start scraping
    scraper.scrape(article_type=config["article_type"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vietnamese News scraper (with url/type)"
    )
    parser.add_argument(
        "--config",
        default="scraper_config.yml",
        help="path to config file",
        dest="config_fpath",
    )
    args = parser.parse_args()
    main(**vars(args))
