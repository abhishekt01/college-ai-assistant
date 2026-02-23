import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_website(start_url, max_pages=150):

    visited = set()
    to_visit = [start_url]
    all_pages = []

    while to_visit and len(visited) < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        print("Scraping:", url)
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted elements
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            # Extract main content
            main_content = soup.find("div", class_="kingster-page-wrapper")
            if not main_content:
                main_content = soup

            text = " ".join(main_content.get_text().split())

            if len(text) > 300:
                all_pages.append({
                    "url": url,
                    "text": text
                })

            # Find internal links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(start_url, link["href"])
                parsed = urlparse(full_url)

                if parsed.netloc == urlparse(start_url).netloc:
                    if "#" not in full_url and full_url not in visited:
                        to_visit.append(full_url)

        except Exception as e:
            print("Error:", e)

        time.sleep(0.5)

    return all_pages