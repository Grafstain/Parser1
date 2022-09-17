from bs4 import BeautifulSoup
import requests
import os.path


class Parser:
    raw_html = ""
    html = ""
    result = []

    def __init__(self, url, path):
        self.url = url
        self.path = path

    def get_raw_html(self):
        """
        Получает сырую html с запроса
        """
        req = requests.get(self.url)
        self.raw_html = req.text

    def save_html(self):
        """
        Сохранение страницы в файл index.html
        """
        with open("index.html", 'w', encoding="utf-8") as file:
            file.write(self.raw_html)

    def get_html_from_file(self, file="index.html"):
        """
        Открывает файл с html кодом
        :return: получает html из файла, по-умолчанию index.html
        """
        with open(file, encoding="utf-8") as file:
            self.raw_html = file.read()
            self.html = BeautifulSoup(self.raw_html, 'lxml')

    def parsing(self):
        """
        Парсит данные в список словарей
        result{
            title,
            desc,
            href
            }
        :return: result[{},{}]
        """
        category = self.html.find("div", class_="category-wrapper")
        blocks = category.find_all("li")

        for item in blocks:
            title = item.find("div", class_='category-name').text
            desc = item.find("p", class_='meta-desc').text
            href = "https://techbeacon.com/" + item.a.get('href')
            # print(f"TITLE: {title}, DESC: {desc}, HREF: {href}")
            self.result.append({
                "title": title,
                "desc": desc,
                "href": href,
            })
        if bool(self.result):
            print("Парсинг в список result завершен")
        else:
            print("Что-то пошло не так")

    def make_result_file(self):
        """
        Сохраняет результат парсинга в файл result.txt с удобным форматированием
        """
        with open("result.txt", 'w', encoding="utf-8") as file:
            i = 1
            for item in self.result:
                file.write(
                    f'{str(i)}. Категория:  {item["title"]}\n\n'
                    f'Описание: {item["desc"]}\n\n'
                    f'Ссылка: {item["href"]}'
                    f'\n*************************************************************\n\n')

                i += 1

    def first_run(self):
        self.get_raw_html()
        self.save_html()

    def run(self):
        """Запускает методы парсера
        создает result.txt с данными
        """
        if not os.path.exists('index.html'):
            self.first_run()
            print("Файл index.html создан")
        self.get_html_from_file()
        self.parsing()
        self.make_result_file()
        if os.path.exists('result.txt'):
            print("Файл result.txt создан")
        elif os.path.getsize('result.txt'):
            print("Что-то пошло не так, файл пустой")
        else:
            print("Что-то пошло не так, файл не создан")
