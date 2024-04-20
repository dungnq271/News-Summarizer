from src.scraper import VnExpressScraper

if __name__ == "__main__":
    scraper = VnExpressScraper(save_dir="./result", top_k=5, num_workers=8)
    scraper.scrape(article_type="tin-moi-nhat")
