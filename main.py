import requests
import lxml
from bs4 import BeautifulSoup


HOME = 'https://www.pagina12.com.ar/'


def get_hot_section_links():
    try:
        P12 = requests.get(HOME)
        if P12.status_code == 200:
            P12_SOUP = BeautifulSoup(P12.text, 'lxml')
            hot_sections = P12_SOUP.find('ul', attrs={
                'class': 'horizontal-list main-sections hide-on-dropdown'}).find_all('li')
            links_hot_section = [section.find('a').get(
                'href') for section in hot_sections]
            return links_hot_section
    except Exception as ex:
        print('Error:')
        print(ex)
        print('\n')


def get_news_links(list_section_links):
    all_news_links = []
    for section_link in list_section_links:
        try:
            section = requests.get(section_link)
            if section.status_code == 200:
                section_soup = BeautifulSoup(section.text, 'lxml')
                for i in range(2,5):
                    hn = f'h{i}'
                    nodes = section_soup.find_all(hn, attrs={'class': 'title-list'})
                    for node in nodes:
                        temp_link = node.find('a').get('href')
                        all_news_links.append(HOME + temp_link)
        except Exception as ex:
            print('Error:')
            print(ex)
            print('\n')
    return all_news_links


def get_new(url):
    try:
        new = requests.get(url)
        if new.status_code == 200:
            new_soup = BeautifulSoup(new.text, 'lxml')
            title = new_soup.find('h1').get_text()
            time = new_soup.find('time').get('datetime')
            section = new_soup.find(
                'h5', attrs={'class': 'current-tag'}).get_text()
            volanta = new_soup.find('h4').get_text()
            copete = new_soup.find('h3').get_text()
            text_temp = new_soup.find(
                'div', attrs={'class': 'article-main-content article-text'}).find_all('p')
            text = ''
            for part in text_temp:
                text += part.text
            new_dict = {'title': title,
                        'time': time,
                        'section': section,
                        'volanta': volanta,
                        'copete': copete,
                        'text': text}
            return new_dict

    except Exception as ex:
        print('Error:')
        print(ex)
        print('\n')


def run():
    all_news_dict = []
    hot_section_links = get_hot_section_links()
    all_news_links = get_news_links(hot_section_links)
    for link in all_news_links:
        temp_dict = get_new(link)
        all_news_dict.append(temp_dict)
    print(all_news_dict)
    # all_new_links = get_news_links(list_hot_sections_links)
    # for link in all_new_links:
    #     temp_dict = get_new(link)
    #     all_news_dict.append(temp_dict)
    # print(all_news_dict)
    

if __name__ == '__main__':
    run()