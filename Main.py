from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from xlsxwriter import Workbook
import requests
import re

driver = webdriver.Chrome()
actions = ActionChains(driver)

url = 'https://habr.com/ru/post/698852/'
driver.get(url)
driver.implicitly_wait(40)

comments_container = driver.find_element(By.CSS_SELECTOR, ".tm-comments-wrapper__wrapper")
comments_container_html = comments_container.get_attribute('innerHTML')
soup = BeautifulSoup(comments_container_html, features='html.parser')

comments = soup.select('.tm-comment__body-content_v2')
comments_content = []

for comment in comments:
    body = '\n'.join(soup.find_all('p')[0].stripped_strings)
    pattern = re.compile('((?!нейросеть создает|нейросеть не создает).)*')
    r3 = re.findall(r'нейро' or 'ИИ', comment.div.p.text)
    if r3:
        RE = True
    else:
        RE = False
    comments_content.append([comment.div.p.text, RE])


workbook = Workbook('comments.xlsx')
worksheet = workbook.add_worksheet()

header = ['Текст комментария', 'Результат работы регулярки']
worksheet.write_row(0, 0, header)

for row, comment in enumerate(comments_content, 1):
    worksheet.write_row(row, 0, comment)

workbook.close()
