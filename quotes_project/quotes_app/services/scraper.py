from django.db import transaction

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

from ..models import Author, Tag, Quote



def init_driver():
    """Initialize a headless Chrome WebDriver using WebDriver Manager."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def scrape_quotes():
    """
    Scrape quotes, authors, and tags from https://quotes.toscrape.com/
    across multiple pages and return newly added quotes.
    """
    try:
        with init_driver() as driver:
            driver.get('http://quotes.toscrape.com/')
            all_quotes = []
            page = 1
            while True:
                try:
                    cards = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'quote'))
                    )
                    for card in cards:
                        all_quotes.append({
                            'Quote': card.find_element(By.CLASS_NAME, 'text').text,
                            'Author': card.find_element(By.CLASS_NAME, 'author').text,
                            'Tags': [tag.text for tag in card.find_elements(By.CSS_SELECTOR, 'a.tag')]
                        })
                    page += 1
                    driver.get(f'http://quotes.toscrape.com/page/{page}/')
                except TimeoutException:
                    break
        return save_quotes_to_db(all_quotes)
    except (TimeoutException, WebDriverException) as e:
        print(f"Error initializing driver: {e}")
        return []


@transaction.atomic
def save_quotes_to_db(quotes_data):
    """
    Save scraped quotes to the database.
    """
    new_quotes = []
    
    for data in quotes_data:
        author, _ = Author.objects.get_or_create(name=data['Author'])
        quote, created = Quote.objects.get_or_create(text=data['Quote'], author=author)
        
        if created:
            for tag_name in data['Tags']:
                tag, _ = Tag.objects.get_or_create(name_tag=tag_name)
                quote.tags.add(tag)
            
            new_quotes.append({
                'id': quote.id,
                'text': quote.text,
                'author': quote.author.name,
                'tags': [tag.name_tag for tag in quote.tags.all()]
        })
            
    return new_quotes