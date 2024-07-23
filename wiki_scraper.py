import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_wiki_url(url):
    """
    Check if the URL is a valid Wikipedia URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc == 'en.wikipedia.org' and parsed_url.path.startswith('/wiki/')

def scrape_links(url, cycles):
    """
    Scrape Wikipedia links from the provided URL and repeat the process for `n` cycles.
    """
    visited = set()
    to_visit = [url]
    all_links = set()  # Use a set to avoid duplicate links

    while to_visit and cycles > 0:
        current_url = to_visit.pop(0)
        
        if current_url in visited:
            continue
        
        visited.add(current_url)
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all Wikipedia links on the current page
        new_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/') and 'http' not in href:
                full_url = urljoin('https://en.wikipedia.org', href)
                if full_url not in visited:
                    new_links.add(full_url)

        # Add newly found links to the set of all links
        all_links.update(new_links)
        to_visit.extend(new_links)

        cycles -= 1  # Decrement cycle count

    return all_links

def main():
    url = input("Enter Wikipedia URL: ")
    if not is_valid_wiki_url(url):
        print("Invalid Wikipedia URL")
        return

    try:
        cycles = int(input("Enter the number of cycles (1 to 3): "))
        if cycles < 1 or cycles > 3:
            print("Please enter a number between 1 and 3")
            return
    except ValueError:
        print("Invalid number")
        return

    links = scrape_links(url, cycles)
    print(f"Found {len(links)} unique links:")
    for link in links:
        print(link)

if __name__ == '__main__':
    main()