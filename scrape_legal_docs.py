import requests
from bs4 import BeautifulSoup
import os

# List of UK legal websites to scrape
LEGAL_SITES = [
    "https://www.legislation.gov.uk/",
    "https://www.gov.uk/browse/justice"
]

def scrape_legal_pages():
    for site in LEGAL_SITES:
        print(f"Scraping {site}...")
        response = requests.get(site)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract all links
            links = [a['href'] for a in soup.find_all('a', href=True) if 'pdf' in a['href']]
            
            # Download PDFs
            for link in links:
                download_pdf(link)
        else:
            print(f"Failed to access {site}")

def download_pdf(url):
    pdf_name = url.split("/")[-1]
    pdf_path = f"./legal_pdfs/{pdf_name}"
    
    os.makedirs("legal_pdfs", exist_ok=True)
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"✅ Downloaded: {pdf_name}")
    else:
        print(f"❌ Failed to download: {pdf_name}")

if __name__ == "__main__":
    scrape_legal_pages()
