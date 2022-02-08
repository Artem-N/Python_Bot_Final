from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.80 Safari/537.36'
}


def parse_pinterest_cats():
    serv = Service('/Users/artemnovickij/Downloads/chromedriver')
    url = 'https://www.pinterest.com/search/pins/?q=cats&rs=typed&term_meta[]=cats%7Ctyped'
    driver = webdriver.Chrome(service=serv)
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    data = soup.findAll(['img', 'video'])
    lst_image = []
    for pic in data:
        lst_image.append(pic['src'])
    return lst_image


def parse_pinterest_dogs():
    serv = Service('/Users/artemnovickij/Downloads/chromedriver')
    url = 'https://www.pinterest.com/search/pins/?q=dogs&rs=typed&term_meta[]=dogs%7Ctyped'
    driver = webdriver.Chrome(service=serv)
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    data = soup.findAll(['img', 'video'])
    lst_image = []
    for pic in data:
        lst_image.append(pic['src'])
    return lst_image


def parse_pinterest_mems():
    serv = Service('/Users/artemnovickij/Downloads/chromedriver')
    url = 'https://www.pinterest.com/search/pins/?rs=ac&len=2&q=%D0%BC%D0%B5%D0%BC%D1%8B&eq=%D0%BC%D0%B5%D0%BC&etsl' \
          'f=8368&term_meta[]=%D0%BC%D0%B5%D0%BC%D1%8B%7Cautocomplete%7C0'
    driver = webdriver.Chrome(service=serv)
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    data = soup.findAll(['img', 'video'])
    lst_image = []
    for pic in data:
        lst_image.append(pic['src'])
    return lst_image
