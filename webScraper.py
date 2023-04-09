import requests
from bs4 import BeautifulSoup

def scrape_headings(url):
    try:
        # Make a request to the website
        response = requests.get(url)
        response.raise_for_status()

        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all heading tags (h1, h2, h3, h4, h5, h6)
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

        # Extract and print the text from each heading tag
        for heading in headings:
            print(heading.name, heading.text.strip())

    except requests.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter the URL of the website you want to scrape: ")
    scrape_headings(url)
