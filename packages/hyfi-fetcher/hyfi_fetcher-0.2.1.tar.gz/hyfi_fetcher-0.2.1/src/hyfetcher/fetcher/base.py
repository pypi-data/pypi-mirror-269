"""Base Fetcher"""

import logging
import multiprocessing as mp
import time
from functools import partial
from pathlib import Path
from typing import Callable, List, Literal, Optional

import requests
from bs4 import BeautifulSoup
from hyfi.composer import BaseModel
from hyfi.main import HyFI
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


class Response(BaseModel):
    """
    A class representing a response with text and status code.

    Explanation:
    This class defines a response object with attributes for text and status code.

    Args:
    - text (str): The text content of the response.
    - status_code (int): The status code of the response.
    """

    text: str = ""
    status_code: int = 0


class By:
    """Set of supported locator strategies."""

    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"


class BaseFetcher(BaseModel):
    """
    Base Fetcher

    Explanation:
    This class serves as the base class for fetchers in the HyFI framework. It provides common functionality for fetching links and articles from web pages.

    Attributes:
    - article_filename (str): The filename for storing the fetched articles.
    - base_url (str): The base URL for the web pages to be fetched.
    - delay_between_requests (float): The delay (in seconds) between consecutive requests.
    - key_field (str): The field in the fetched data used as the key for deduplication.
    - keyword_placeholder (str): The placeholder in the search URL to be replaced with keywords.
    - link_filename (str): The filename for storing the fetched links.
    - max_num_articles (Optional[int]): The maximum number of articles to fetch.
    - max_num_pages (Optional[int]): The maximum number of pages to fetch.
    - num_workers (int): The number of parallel workers for fetching.
    - output_dir (str): The output directory for storing the fetched data.
    - overwrite_existing (bool): Whether to overwrite existing data files.
    - page_placeholder (str): The placeholder in the URL for pagination.
    - print_every (int): The interval for printing progress information.
    - search_keywords (List[str]): The list of keywords to search for.
    - search_url (str): The URL for searching web pages.
    - start_page (Optional[int]): The starting page number for pagination.
    - start_urls (List[str]): The list of starting URLs for fetching.
    - use_playwright (bool): Whether to use Playwright for fetching.
    - verbose (bool): Whether to print verbose information during fetching.
    """

    _config_name_: str = "base"
    _config_group_: str = "/fetcher"

    article_filename: str = "articles.jsonl"
    base_url: str = ""
    delay_between_requests: float = 0.5
    key_field: str = "url"
    keyword_placeholder: str = "{keyword}"
    link_filename: str = "links.jsonl"
    max_num_articles: Optional[int] = 30
    max_num_pages: Optional[int] = 2
    num_workers: int = 1
    output_dir: str = f"workspace/datasets{_config_group_}/{_config_name_}"
    overwrite_existing: bool = False
    page_placeholder: str = "{page}"
    print_every: int = 10
    search_keywords: List[str] = []
    search_url: str = ""
    start_page: Optional[int] = 1
    start_urls: List[str] = []
    use_playwright: bool = False
    verbose: bool = True

    _links: List[dict] = []
    _articles: List[dict] = []
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def __call__(self):
        self.fetch()

    def fetch(self):
        """
        Fetch links and articles.

        Explanation:
        This method fetches links and articles from web pages based on the specified configuration.
        """
        self.fetch_links()
        self.fetch_articles()

    def get_soup(self, url: str):
        """
        Retrieve and parse HTML content at the given endpoint.

        Args:
        - url (str): The URL of the web page to retrieve and parse.

        Returns:
        - BeautifulSoup: The parsed HTML content of the web page.
        """
        try:
            response = self.request(url, use_playwright=self.use_playwright)
            # Check if page exists (status code 200) or not (status code 404)
            if response.status_code == 404:
                logger.info("Page [%s] does not exist, stopping...", url)
                return None
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            logger.error("Error while fetching the page url: %s", url)
            logger.error("Error: %s", e)
            return None

    def request(
        self,
        url: str,
        use_playwright: bool = False,
        timeout: float | None = None,
        params: dict | None = None,
        **kwargs,
    ) -> Response:
        """
        Sends a GET request.

        Args:
        - url (str): URL for the request
        - params (dict, optional): Dictionary, list of tuples or bytes to send
            in the query string for the Request. Defaults to None.
        - **kwargs: Optional arguments that `request` takes.

        Returns:
        - Response: Response object containing response text and status code
        """
        if use_playwright:
            res, status_code = sync_playwright_request(url, timeout=timeout, **kwargs)
            return Response(text=res, status_code=status_code)
        res = requests.get(url, params=params, headers=self._headers, **kwargs)
        return Response(text=res.text, status_code=res.status_code)

    @property
    def start_urls_encoded(self):
        if self.start_urls:
            return self.start_urls
        if self.keyword_placeholder in self.search_url:
            # Generate start URLs by replacing keyword placeholder with encoded keywords
            start_urls = [
                self.search_url.replace(
                    self.keyword_placeholder, self.encode_keyword(keyword)
                )
                for keyword in self.search_keywords
            ]
        else:
            start_urls = [self.search_url]
        return start_urls

    def encode_keyword(self, keyword: str):
        """
        Encode a keyword for use in a URL.

        Args:
        - keyword (str): The keyword to encode.

        Returns:
        - str: The encoded keyword.
        """
        return keyword.replace(" ", "+")

    @property
    def links(self):
        return self._links or self._load_links()

    @property
    def articles(self):
        return self._articles or self._load_articles()

    @property
    def link_filepath(self) -> str:
        _path = Path(self.output_dir) / self.link_filename
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path.absolute())

    @property
    def article_filepath(self) -> str:
        _path = Path(self.output_dir) / self.article_filename
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path.absolute())

    @property
    def link_filepath_tmp(self) -> str:
        _path = Path(self.output_dir) / f"{self.link_filename}.tmp"
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path)

    @property
    def article_filepath_tmp(self) -> str:
        _path = Path(self.output_dir) / f"{self.article_filename}.tmp"
        _path.parent.mkdir(parents=True, exist_ok=True)
        return str(_path)

    def _load_links(self) -> List[dict]:
        if Path(self.link_filepath).exists():
            self._links = HyFI.load_jsonl(self.link_filepath)
        return self._links

    def _load_articles(self) -> List[dict]:
        if Path(self.article_filepath).exists():
            self._articles = HyFI.load_jsonl(self.article_filepath)
        return self._articles

    def fetch_links(self):
        parse_page_func = partial(
            self.parse_page_links,
            print_every=self.print_every,
            verbose=self.verbose,
        )

        next_page_func = partial(
            self.next_page_func,
            page_placeholder=self.page_placeholder,
        )

        self._fetch_links(parse_page_func, next_page_func)

    def fetch_articles(self):
        parse_article_text = partial(self.parse_article_text)

        self._fetch_articles(parse_article_text)

    def _fetch_links(self, parse_page_func: Callable, next_page_func: Callable):
        num_workers = min(self.num_workers, len(self.search_keywords))
        num_workers = max(num_workers, 1)
        link_urls = [link["url"] for link in self.links]
        fetch_links_func = partial(
            crawl_links,
            parse_page_func=parse_page_func,
            next_page_func=next_page_func,
            start_page=self.start_page,
            max_num_pages=self.max_num_pages,
            link_urls=link_urls,
            link_filepath=self.link_filepath_tmp,
            delay_between_requests=self.delay_between_requests,
        )
        if links := self._fetch_links_mp(
            num_workers,
            fetch_links_func,
        ):
            self.save_links(links)
        else:
            logger.info("No more links found")

    def save_links(self, links: List[dict]):
        """
        Save the fetched links to a file.

        Args:
        - links (List[dict]): The list of links to save.
        """
        self._links.extend(links)
        original_len = len(self._links)
        self._links = HyFI.remove_duplicates_from_list_of_dicts(
            self._links, key=self.key_field
        )
        logger.info(
            "Removed %s duplicate links from %s links",
            original_len - len(self._links),
            original_len,
        )
        HyFI.save_jsonl(self._links, self.link_filepath)
        logger.info("Saved %s links to %s", len(self._links), self.link_filepath)

    def _fetch_links_mp(
        self,
        num_workers: int,
        batch_func: Callable,
    ) -> List[dict]:
        with mp.Pool(num_workers) as pool:
            results = pool.map(batch_func, self.start_urls_encoded)
        links = []
        for result in results:
            links.extend(result)
        return links

    def _fetch_articles(self, parse_article_func: Callable):
        num_workers = min(self.num_workers, len(self.links))
        article_urls = [article["url"] for article in self.articles]
        fetch_articles_func = partial(
            scrape_article_text,
            parse_article_func=parse_article_func,
            article_urls=article_urls,
            overwrite_existing=self.overwrite_existing,
            article_filepath=self.article_filepath_tmp,
            max_num_articles=self.max_num_articles,
            delay_between_requests=self.delay_between_requests,
            print_every=self.print_every,
            verbose=self.verbose,
        )
        if articles := self._fetch_articles_mp(num_workers, fetch_articles_func):
            self.save_articles(articles)
        else:
            logger.info("No more articles found")

    def save_articles(self, articles: List[dict]):
        """
        Save the fetched articles to a file.

        Args:
        - articles (List[dict]): The list of articles to save.
        """
        self._articles.extend(articles)
        original_len = len(self._articles)
        self._articles = HyFI.remove_duplicates_from_list_of_dicts(
            self._articles, key=self.key_field
        )
        logger.info(
            "Removed %s duplicate articles from %s articles",
            original_len - len(self._articles),
            original_len,
        )
        HyFI.save_jsonl(self._articles, self.article_filepath)
        logger.info(
            "Saved %s articles to %s",
            len(self._articles),
            self.article_filepath,
        )

    def _fetch_articles_mp(
        self,
        num_workers: int,
        batch_func: Callable,
    ) -> List[dict]:
        articles = []
        if len(self.links) < 1:
            return articles
        batch_size = len(self.links) // num_workers
        batches = [
            self.links[i : i + batch_size]
            for i in range(0, len(self.links), batch_size)
        ]
        with mp.Pool(num_workers) as pool:
            results = pool.map(batch_func, batches)
        for result in results:
            articles.extend(result)
        return articles

    def next_page_func(
        self,
        start_url: str,
        current_url: Optional[str],
        page: int,
        page_placeholder: Optional[str],
    ) -> Optional[str]:
        if page_placeholder and page_placeholder in start_url:
            # Return next page url by replacing placeholder with page number
            page_url = start_url.replace(page_placeholder, str(page))
        elif current_url is None:
            page_url = start_url
        else:
            # TODO: implement your next page logic to return None if no more pages
            raise NotImplementedError("Next page logic not implemented in base class")
        logger.info("Page url: %s", page_url)
        return page_url

    def parse_page_links(
        self,
        page_url: str,
        print_every: int = 10,
        verbose: bool = False,
    ) -> Optional[List[dict]]:
        """Get the links from the given page."""

        # TODO: Parse the page and extract all links
        raise NotImplementedError("Parsing links is not implemented in base class")

    def parse_article_text(self, url: str) -> dict:
        # TODO: Scrape the article page and extract the text
        raise NotImplementedError(
            "Parsing article text is not implemented in base class"
        )


def crawl_links(
    start_url: str,
    parse_page_func: Callable,
    next_page_func: Callable,
    start_page: int = 1,
    max_num_pages: Optional[int] = 2,
    link_urls: Optional[List[str]] = None,
    link_filepath: Optional[str] = None,
    delay_between_requests: float = 0.0,
) -> List[dict]:
    """Crawl links for article links with the given keyword.

    Args:
        keyword (str): Keyword to search for.
        search_url (str, optional): URL to search for the keyword. Defaults to "https://www.khmertimeskh.com/page/{page}/?s={keyword}".
        links (List[dict], optional): List of links to append to. Defaults to None.
        max_num_pages (Optional[int], optional): Maximum number of pages to crawl. Defaults to 2.
        link_filepath (Optional[str], optional): Filepath to save the links to. Defaults to None.
        print_every (int, optional): Print progress every n pages. Defaults to 10.
        verbose (bool, optional): Print progress. Defaults to False.

    Returns:
        List[dict]: List of links.
    """

    page = start_page
    page_cnt = 0
    page_url = None
    links = []
    link_urls = link_urls or []
    logger.info("Fetching links for url: %s", start_url)
    while True:
        # get next page url
        page_url = next_page_func(start_url, page_url, page)
        # Parse page
        page_links = parse_page_func(page_url)

        # Check if page_links is None
        if page_links is None:
            logger.info("No more links found, stopping...")
            break

        for link in page_links:
            if link["url"] not in link_urls:
                link["page_url"] = page_url
                link["page"] = page
                links.append(link)
                link_urls.append(link["url"])
                if link_filepath:
                    HyFI.append_to_jsonl(link, link_filepath)
            else:
                logger.info(
                    "Link %s already exists, skipping...",
                    link["url"],
                )

        page += 1
        page_cnt += 1

        if max_num_pages and page_cnt > max_num_pages:
            logger.info("Reached max number of pages, stopping...")
            break
        # Delay between requests
        if delay_between_requests > 0:
            logger.info("Sleeping for %s seconds...", delay_between_requests)
            time.sleep(delay_between_requests)

    logger.info("Finished fetching links for url: %s", start_url)
    logger.info("Total links fetched: %s", len(links))
    return links


def scrape_article_text(
    links: List[dict],
    parse_article_func: Callable,
    article_urls: Optional[List[dict]] = None,
    overwrite_existing: bool = False,
    max_num_articles: Optional[int] = 10,
    article_filepath: Optional[str] = None,
    delay_between_requests: float = 0.0,
    print_every: int = 10,
    verbose: bool = False,
) -> List[dict]:
    """Scrape the article text from the given links.

    Args:
        links (List[dict]): List of links to scrape.
        articles (Optional[List[dict]], optional): List of articles to append to. Defaults to None.
        overwrite_existing (bool, optional): Overwrite existing articles. Defaults to False.
        max_num_articles (Optional[int], optional): Maximum number of articles to scrape. Defaults to 10.
        article_filepath (Optional[str], optional): Filepath to save the articles to. Defaults to None.
        print_every (int, optional): Print progress every n articles. Defaults to 10.
        verbose (bool, optional): Print progress. Defaults to False.

    Returns:
        List[dict]: List of articles.
    """
    articles = []
    article_urls = article_urls or []
    for i, link in enumerate(links):
        if max_num_articles is not None and i >= max_num_articles:
            logger.info("Reached max number of articles, stopping...")
            break

        url = link["url"]
        title = link["title"]
        if url in article_urls and not overwrite_existing:
            logger.info("Article [%s](%s) already exists, skipping...", title, url)
            continue

        # Parse article
        _article = parse_article_func(url)
        if _article is None:
            logger.info(
                "Article [%s](%s) does not exist, skipping...",
                title,
                url,
            )
            continue
        article = link.copy()
        article.update(_article)
        articles.append(article)
        article_urls.append(url)
        if article_filepath:
            HyFI.append_to_jsonl(article, article_filepath)
        if (verbose and (i + 1) % print_every == 0) or delay_between_requests > 0:
            logger.info("Article [%s](%s) scraped", title, url)

        # Delay between requests
        if delay_between_requests > 0 and i < len(links) - 1:
            logger.info("Sleeping for %s seconds...", delay_between_requests)
            time.sleep(delay_between_requests)

    logger.info("Finished scraping articles")
    logger.info("Total articles scraped: %s", len(articles))
    return articles


def sync_playwright_request(
    url: str,
    timeout: float | None = None,
    wait_until: (
        Literal["commit", "domcontentloaded", "load", "networkidle"] | None
    ) = None,
    referer: str | None = None,
    **kwargs,
) -> str:
    """
    Make a synchronous request using Playwright to scrape content from a URL.

    Explanation:
    This function performs a synchronous request using Playwright to scrape content from a specified URL. It returns the scraped content and the status code of the request.

    Args:
    - url (str): The URL to scrape content from.
    - timeout (float | None): The timeout for the request.
    - wait_until (Literal["commit", "domcontentloaded", "load", "networkidle"] | None): The event to wait for before considering the navigation succeeded.
    - referer (str | None): The referer header value for the request.
    - **kwargs: Additional keyword arguments for launching the browser.

    Returns:
    - Tuple[str, int]: A tuple containing the scraped content as a string and the status code of the request.

    Raises:
    - Exception: If an error occurs during the scraping process.

    Examples:
    N/A
    """

    logger.info("Started scraping...")
    results = ""
    status_code = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, **kwargs)
        try:
            page = browser.new_page()
            page.goto(url, wait_until=wait_until, timeout=timeout, referer=referer)

            results = page.content()
            status_code = 200
            logger.info("Content scraped from %s", url)
        except Exception as e:
            results = f"Error: {e}"
            status_code = 500
            logger.error("Error: %s", e)
        browser.close()
    return results, status_code
