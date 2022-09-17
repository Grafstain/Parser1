# utf-8
from bs4 import BeautifulSoup
import requests
from lxml import etree

url = "https://techbeacon.com/"

req = requests.get(url)
src = req.text
print(src)

# Сохранение страницы в файл
with open("index.html", 'w', encoding="utf-8") as file:
    file = file.write(src)

# Чтение из файла
with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
category = soup.find("div", class_="category-wrapper")
news = category.find_all("li")


results = []

for item in news:
    title = item.find("div", class_='category-name').text
    desc = item.find("p", class_='meta-desc').text
    href = "https://techbeacon.com/"+item.a.get('href')
    print(f"TITLE: {title}, DESC: {desc}, HREF: {href}")
    results.append({
        "title": title,
        "desc": desc,
        "href": href,
    })

file = open("result.txt", 'w', encoding="utf-8")
i = 1
for item in results:
    file.write(
               f'{str(i)} Категория:  {item["title"]}\n\n'
               f'Описание: {item["desc"]}\n\n'
               f'Ссылка: {item["href"]}'
               f'\n*************************************************************\n\n')

    i += 1
file.close()
# print(results[1]["title"])
