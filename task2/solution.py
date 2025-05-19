import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_page(session, url, counts):
    html = await fetch_page(session, url)
    soup = BeautifulSoup(html, 'lxml')
    
    category_block = soup.find('div', class_='mw-category-columns')
    if not category_block:
        return None
    
    category_groups = category_block.find_all('div', class_='mw-category-group')
    
    for group in category_groups:
        letter = group.find('h3').text.strip()
        if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return 'break'
        if not letter.isalpha():
            continue
        counts[letter] += len(group.find_all('li'))
    
    next_page = soup.find('a', string='Следующая страница')
    return f"https://ru.wikipedia.org{next_page['href']}" if next_page else None

async def get_animals_count():
    counts = defaultdict(int)
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    
    async with aiohttp.ClientSession() as session:
        while url:
            url = await process_page(session, url, counts)
            if url == 'break':
                break
    
    return counts

def write_to_csv(counts):
    with open('beasts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])

async def main():
    print("Получение данных о животных...")
    print("Время ожидания ~25 секунд")
    animals_counts = await get_animals_count()
    write_to_csv(animals_counts)
    print("Данные успешно записаны в beasts.csv")

if __name__ == "__main__":
    asyncio.run(main())