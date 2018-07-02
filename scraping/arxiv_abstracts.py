'''
Created on Jul 2, 2018

@author: rachel


module to scrape arxive search result and get abstracts of all listed links
 
'''

import urllib.request as urlrequest
from bs4 import BeautifulSoup as BS

def generate_link_list(search_page):
    # generate a list of links from the requested arxive search results
    search_web = urlrequest.urlopen(search_page)
    search_soup = BS(search_web)
    # get links
    link_list = search_soup.find_all("div", class_="level is-marginless")
    links = []
    for l in link_list:
        link = l.find("a").get("href")
        links.append(link)
    return links


def get_title_abstract(link):
    link_web = urlrequest.urlopen(link)
    link_soup = BS(link_web)
    # get title
    title = link_soup.find("h1", class_="title mathjax").contents[1]
    # get abstract
    abstract = link_soup.find("blockquote", class_="abstract mathjax")
    abstract = abstract.contents[2]
    return title, abstract

def get_abstracts_from_search(search_page=("https://arxiv.org/search/advanced?advanced="
                                    "1&terms-0-operator=AND&terms-0-term="
                                    "emg&terms-0-field=title&classification-"
                                    "computer_science=y&classification-physics"
                                    "_archives=all&date-filter_by=all_dates"
                                    "&date-year=&date-from_date=&date-to_date="
                                    "&size=50&order=-announced_date_first")):
    links = generate_link_list(search_page)
    abstracts = {}
    for link in links:
        title, abstract = get_title_abstract(link)
        abstracts[title] = abstract
    return abstracts
        
if __name__=='__main__':
    get_abstracts_from_search()        