from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from xlsxwriter import Workbook
import requests
import re


class HabrPars:
    def __int__(self, driver):
        self.driver = driver

    @staticmethod
    def pars_comments():
        comments_container = driver.find_element(By.CSS_SELECTOR, ".tm-comments-wrapper__wrapper")
        comments_container_html = comments_container.get_attribute('innerHTML')
        soup = BeautifulSoup(comments_container_html, features='html.parser')

        comments = soup.select('.tm-comment__body-content_v2')
        comments_content = []

        for comment in comments:
            body = '\n'.join(soup.find_all('p')[0].stripped_strings)
            pattern = re.compile('((?!создает).)*')
            r3 = re.findall(r'нейро', comment.div.p.text)
            COM = re.findall(r'(.+\D{2}?нейр\D{5,}\b.*)', comment.div.p.text)
            RE = True if r3 else False
            try:
                comments_content.append([comment.div.p.text, RE, COM[0]])
            except:
                comments_content.append([comment.div.p.text, RE, ''])

        return comments_content


def excel_save(filename, data):
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()

    header = ['Текст комментария', 'Результат работы регулярки', 'Фрагмент текста']
    worksheet.write_row(0, 0, header)

    for row, record in enumerate(data, 1):
        worksheet.write_row(row, 0, record)

    workbook.close()


driver = webdriver.Chrome()
pars = HabrPars()


url = 'https://habr.com/ru/post/698852/'
driver.get(url)

coments = pars.pars_comments()

excel_save('comments.xlsx', coments)
