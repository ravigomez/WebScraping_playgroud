import time
import requests
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

url = "http://www.b3.com.br/pt_br/noticias/"

# df = pd.read_excel('sample.xlsx', 'Sheet1', usecols=[0, 1, 2, 3])
# print(df)
# exit()

option = Options()
option.headless = True

driver = webdriver.Chrome(options=option)
driver = webdriver.Chrome()

driver.get(url)

noticias_content = driver.find_element_by_id(
    "noticias").get_attribute('outerHTML')

Linhas_soup = BeautifulSoup(noticias_content, 'html.parser')

n = []

for linha in Linhas_soup.findAll('div', class_='row'):
    for noticia in linha.findAll('a', id='link-noticia'):

        n.append([noticia.div.div.p.text, noticia.div.div.h4.text,
                  noticia.find('div').find('div').findChildren()[2].text])

        # print(noticia.div.div.p.text)
        # print(noticia.div.div.h4.text)
        # print(noticia.find('div').find('div').findChildren()[2].text)
        # print('')

ddf = pd.DataFrame(n, columns=['Data', 'Título', 'Resumo'])

print(ddf)

ddf.to_excel('path_to_file.xlsx', sheet_name='Sheet1', engine='xlsxwriter')


driver.quit()
