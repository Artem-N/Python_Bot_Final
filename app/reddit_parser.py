import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                  ' Version/15.3 Safari/605.1.15'
}


def parse_reddit_hot():
    url = 'https://www.reddit.com/hot/'
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.content, 'lxml')

    hot_data = soup.find_all('div', class_='_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3')

    list_posts = []
    for post in hot_data:
        list_posts.append({
            'time': post.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s').get_text(strip=True),
            'title': post.find('h3', class_='_eYtD2XCVieq6emjKBH3m').get_text(strip=True),
            'comment': post.find('span', class_='FHCV02u6Cp2zYL0fhQPsO').get_text(strip=True),
            'link': post.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s').get('href')
        })
    return list_posts


def parse_reddit_new():
    url = 'https://www.reddit.com/new/'
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.content, 'lxml')

    new_data = soup.find_all('div', class_='_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3')

    list_posts = []
    for post in new_data:
        list_posts.append({
            'time': post.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s').get_text(strip=True),
            'title': post.find('h3', class_='_eYtD2XCVieq6emjKBH3m').get_text(strip=True),
            'comment': post.find('span', class_='FHCV02u6Cp2zYL0fhQPsO').get_text(strip=True),
            'link': post.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s').get('href')
        })
    return list_posts


def parse_reddit_top():
    url = 'https://www.reddit.com/top/'
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.content, 'lxml')

    new_data = soup.find_all('div', class_='_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3')

    list_posts = []
    for post in new_data:
        list_posts.append({
            'time': post.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s').get_text(strip=True),
            'number_vote': post.find('div', class_='_1E9mcoVn4MYnuBQSVDt1gC').get_text(strip=True),
            'title': post.find('h3', class_='_eYtD2XCVieq6emjKBH3m').get_text(strip=True),
            'comment': post.find('span', class_='FHCV02u6Cp2zYL0fhQPsO').get_text(strip=True),
            'link': post.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s').get('href')
        })
    return list_posts
