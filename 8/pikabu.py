import bs4
import requests


def tags_scrapper(cookies, xcsrf):
    url = 'https://pikabu.ru/'
    headers = {
        'Accept': 'application/json, text/javascript, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'pikabu.ru',
        'Referer': 'https://pikabu.ru/',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'X-Csrf-Token': xcsrf,
        'Cookie': cookies}

    params = dict(twitmode=1,
                  of='v2',
                  page=2,
                  _=1561505656272)

    session = requests.Session()

    home = session.get(url, headers=headers).text
    parsed = bs4.BeautifulSoup(home, 'html.parser')
    stories = parsed.find_all('div', 'story__tags')

    while len(stories) < 100:
        new_page = session.get(url, params=params, headers=headers).json()
        params['page'] += 1
        data = new_page['data']['stories']
        for story in [elem['html'] for elem in data]:
            if len(stories) < 100:
                stories.append(bs4.BeautifulSoup(story, 'html.parser').find('div', 'story__tags'))

    return stories


def counter(list_of_tags):
    tags = []
    counted = []
    for elem in list_of_tags:
        for tag in elem:
            try:
                tags.append(tag.text)
            except AttributeError:
                pass

    for elem in set(tags):
        counted.append((elem, tags.count(elem)))

    counted = sorted(counted, key=lambda x: x[1], reverse=True)
    return counted


if __name__ == '__main__':
    t = tags_scrapper(input('Paste your cookies: '), input('Paste your XCSRF token: '))
    sorted_tags = counter(t)
    with open('top_10_tags.txt', 'w', encoding='utf-8') as f:
        for entry in sorted_tags[0:10]:
            f.write(f'{entry[0]}: {entry[1]}\n')
