from src.tools.tools import web_search , scrape_url
from rich import print

search_response = web_search.invoke("latest news of Tunisia")
scraping_response = scrape_url.invoke("https://www.aljazeera.com/where/tunisia")
print(scraping_response)
