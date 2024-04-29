import requests
from bs4 import BeautifulSoup
import json

# Функция для получения информации о книгах на странице
import requests
from bs4 import BeautifulSoup

def get_books_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []
    book_elements = soup.find_all('article', class_='product_pod')
    for element in book_elements:
        title = element.h3.a['title']
        price = float(element.find('p', class_='price_color').text[1:].replace('£', '')) # обработка валюты
        
        # Получить ссылку на страницу с описанием товара
        description_link = element.find('h3').a['href']
        description_url = url.replace('index.html', '') + description_link
        
        # Сделать запрос на страницу с описанием товара
        description_response = requests.get(description_url)
        description_soup = BeautifulSoup(description_response.content, 'html.parser')
        
        # Получить информацию о наличии товара
        stock_text = description_soup.find('p', class_='instock availability').text.strip()
        # Можно добавить дополнительные проверки на наличие цифр в stock_text
        in_stock = int(''.join(filter(str.isdigit, stock_text))) if any(char.isdigit() for char in stock_text) else 0

        # Получить описание товара
        description = description_soup.find('article', class_='product_page').find_all('p')[3].text

        book = {
            'title': title,
            'price': price,
            'in_stock': in_stock,
            'description': description
        }
        books.append(book)
        
    return books

# Функция для получения информации о книгах во всех категориях
def scrape_books():
    main_url = 'http://books.toscrape.com/'
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = soup.find('ul', class_='nav').find_all('li')

    all_books = []
    for category in categories:
        category_link = category.a['href']
        category_url = main_url + category_link
        books_data = get_books_data(category_url)
        all_books.extend(books_data)

    return all_books


# Вызываем функцию для скрейпинга книг
books = scrape_books()

# Сохраняем информацию в JSON-файле
with open('books_data.json', 'w', encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False, indent=4)
