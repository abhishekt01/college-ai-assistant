# Import required libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# Function to extract clean text from a page
def extract_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        # Get visible text
        text = soup.get_text(separator="\n")
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return clean_text
    except:
        return ""


# Function to crawl website recursively
def crawl_website(start_url, max_pages=20):

    visited = set()       # Store visited links
    to_visit = [start_url]  # Links we need to visit
    all_text = []         # Store text from all pages

    while to_visit and len(visited) < max_pages:

        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        print("Scraping:", current_url)

        visited.add(current_url)

        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract text from this page
            page_text = extract_text(current_url)
            all_text.append(page_text)

            # Find new links on this page
            for link in soup.find_all("a", href=True):
                full_url = urljoin(start_url, link["href"])

                # Only visit links from same domain
                if urlparse(full_url).netloc == urlparse(start_url).netloc:
                    if full_url not in visited:
                        to_visit.append(full_url)

        except:
            continue

    return "\n\n".join(all_text)


# Main execution
if __name__ == "__main__":

    # 🔴 Change this to your college website
    website_url = "https://lbscek.ac.in/"

    content = crawl_website(website_url, max_pages=70)

    # Print first 3000 characters
    print(content[:3000])