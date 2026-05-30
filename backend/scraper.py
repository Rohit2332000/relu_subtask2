import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rapidfuzz import fuzz

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

IMPORTANT_PAGES = [
    "about",
    "about-us",
    "company",
    "services",
    "solutions",
    "products",
    "contact",
    "contact-us",
]


def fetch_page(url: str) -> str:
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code == 200:
            return response.text

    except Exception:
        pass

    return ""


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_emails(text: str):
    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    return list(set(emails))


def extract_phones(text: str):
    phones = re.findall(
        r"\+?\d[\d\s\-\(\)]{8,}",
        text
    )

    phones = [p.strip() for p in phones]

    return list(set(phones))


def get_sitemap_links(base_url: str):

    sitemap_url = urljoin(
        base_url,
        "/sitemap.xml"
    )

    xml_content = fetch_page(sitemap_url)

    if not xml_content:
        return []

    try:
        soup = BeautifulSoup(
            xml_content,
            "xml"
        )

        links = [
            loc.text.strip()
            for loc in soup.find_all("loc")
        ]

        return links

    except Exception:
        return []


def get_homepage_links(base_url: str):

    html = fetch_page(base_url)

    if not html:
        return []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = []

    for a in soup.find_all(
        "a",
        href=True
    ):

        href = a["href"]

        full_url = urljoin(
            base_url,
            href
        )

        if (
            urlparse(full_url).netloc
            ==
            urlparse(base_url).netloc
        ):
            links.append(full_url)

    return list(set(links))


def select_relevant_pages(links):

    scored = []

    for link in links:

        score = max(
            fuzz.partial_ratio(
                link.lower(),
                keyword
            )
            for keyword in IMPORTANT_PAGES
        )

        scored.append(
            (link, score)
        )

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [x[0] for x in scored[:8]]


def html_to_text(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "header",
            "footer"
        ]
    ):
        tag.decompose()

    text = soup.get_text(
        separator=" "
    )

    text = clean_text(text)

    return text[:5000]


def scrape_company(url: str):

    sitemap_links = get_sitemap_links(url)

    if sitemap_links:
        links = sitemap_links
    else:
        links = get_homepage_links(url)

    relevant_pages = select_relevant_pages(
        links
    )

    all_text = []

    emails = []
    phones = []

    homepage_html = fetch_page(url)

    if homepage_html:

        homepage_text = html_to_text(
            homepage_html
        )

        all_text.append(
            homepage_text
        )

        emails.extend(
            extract_emails(homepage_text)
        )

        phones.extend(
            extract_phones(homepage_text)
        )

    for page in relevant_pages:

        html = fetch_page(page)

        if not html:
            continue

        page_text = html_to_text(html)

        all_text.append(
            page_text
        )

        emails.extend(
            extract_emails(page_text)
        )

        phones.extend(
            extract_phones(page_text)
        )

    return {
        "content": "\n".join(all_text)[:20000],
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "pages": relevant_pages
    }