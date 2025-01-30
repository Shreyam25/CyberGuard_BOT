import requests
from bs4 import BeautifulSoup

# URL for scraping
URL = "https://en.wikipedia.org/wiki/Digital_privacy"

# Make a request to the URL
response = requests.get(URL)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract paragraphs from the page
paragraphs = soup.find_all("p")
text_data = [para.get_text() for para in paragraphs]
text_data = " ".join(text_data)  # Combine into a single string

# Save the text data to a file
with open("dp_corpus.txt", "w", encoding="utf-8") as file:
    file.write(text_data)
