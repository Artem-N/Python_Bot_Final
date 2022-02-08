import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                  ' Version/15.3 Safari/605.1.15'
}


def parse_politics():
    url = 'https://www.ukr.net/news/politics.html'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        politics = soup.find_all('section', class_='im')
        list_ = []
        for pol in politics:
            list_.append({
                'time': pol.find('time', class_='im-tm').get_text(strip=True),
                'title': pol.find('a', class_='im-tl_a').get_text(strip=True),
                'publishing': pol.find('div', class_='im-pr').get_text(strip=True),
                'link': pol.find('a', class_='im-tl_a').get('href')
            })
        return list_
    else:
        return "Server does not answer!"


def parse_economics():
    url = 'https://www.ukr.net/news/economics.html'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        economics = soup.find_all('section', class_='im')
        list_ = []
        for eco in economics:
            list_.append({
                'time': eco.find('time', class_='im-tm').get_text(strip=True),
                'title': eco.find('a', class_='im-tl_a').get_text(strip=True),
                'publishing': eco.find('div', class_='im-pr').get_text(strip=True),
                'link': eco.find('a', class_='im-tl_a').get('href')
            })
        return list_
    else:
        return "Server does not answer!"


def parse_sports():
    url = 'https://www.ukr.net/news/sport.html'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        sports = soup.find_all('section', class_='im')
        list_ = []
        for spo in sports:
            list_.append({
                'time': spo.find('time', class_='im-tm').get_text(strip=True),
                'title': spo.find('a', class_='im-tl_a').get_text(strip=True),
                'publishing': spo.find('div', class_='im-pr').get_text(strip=True),
                'link': spo.find('a', class_='im-tl_a').get('href')
            })
        return list_
    else:
        return "Server does not answer!"


def parse_sience():
    url = 'https://www.ukr.net/news/science.html'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        sience = soup.find_all('section', class_='im')
        list_ = []
        for sie in sience:
            list_.append({
                'time': sie.find('time', class_='im-tm').get_text(strip=True),
                'title': sie.find('a', class_='im-tl_a').get_text(strip=True),
                'publishing': sie.find('div', class_='im-pr').get_text(strip=True),
                'link': sie.find('a', class_='im-tl_a').get('href')
            })
        return list_
    else:
        return "Server does not answer!"


def parse_technology():
    url = 'https://www.ukr.net/news/technologies.html'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        technologe = soup.find_all('section', class_='im')
        list_ = []
        for tech in technologe:
            list_.append({
                'time': tech.find('time', class_='im-tm').get_text(strip=True),
                'title': tech.find('a', class_='im-tl_a').get_text(strip=True),
                'publishing': tech.find('div', class_='im-pr').get_text(strip=True),
                'link': tech.find('a', class_='im-tl_a').get('href')
            })
        return list_
    else:
        return "Server does not answer!"


def parse_avto():
    url = 'https://www.ukr.net/news/auto.html'
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        avto = soup.find_all('section', class_='im')
        list_ = []
        for av in avto:
            list_.append({
                'time': av.find('time', class_='im-tm').get_text(strip=True),
                'title': av.find('a', class_='im-tl_a').get_text(strip=True),
                'publishing': av.find('div', class_='im-pr').get_text(strip=True),
                'link': av.find('a', class_='im-tl_a').get('href')
            })
        return list_
    else:
        return "Server does not answer!"
