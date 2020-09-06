#
#   Rube Codeberg submission for Craig Quirke at Pyconline AU 2020
#
#   scrapes rulesurl for bold list of rules, finds a random page on wikipedia with the category "Programming languages" 
#    and outputs the number of times the given letter appears (case insensitive)
#
import requests
from bs4 import BeautifulSoup
from html import unescape

rulesurl = 'https://2020.pycon.org.au/program/sun/'
url = "https://en.wikipedia.org/wiki/Special:RandomInCategory"
categoryname = "Programming+languages"
categorydata = unescape("wpcategory={}&wpEditToken=%2B%5C&title=Special%3ARandomInCategory&redirectparams=".format(categoryname))

sessionindex = 0
soupindex = 1
urlindex = 2
characterinfo = [] 

def url_post(url, rawPOSTdata="") -> list:
    # Returns requests session object, page contents as bs4 object, and link to page (if found on wikipedia)
    headers    = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    session    = requests.Session()
    resp       = session.post(url,headers=headers, data=rawPOSTdata)
    soup        = BeautifulSoup(resp.content, 'html.parser')
    if "wikipedia" in url.lower():
        url = soup.find('link', {'rel': 'canonical'}).get('href')
    return [session, soup, url]

def url_get(url) -> list:
    # Returns requests session object, page contents as bs4 object, and link to page (if found on wikipedia)
    headers    = {'User-Agent': 'Mozilla/5.0'} #, 'Content-Type': 'application/x-www-form-urlencoded'}
    print(url)
    session    = requests.Session()
    resp       = session.get(url,headers=headers)
    soup        = BeautifulSoup(resp.content, 'html.parser')
    return [session, soup, url]

def get_charcount(bs4page, character) -> int:
    contentdivtext = bs4page.find(id="mw-content-text")
    charcount = contentdivtext.get_text().lower().count(character.lower())
    return charcount

def outputchars(string):
    stringlist = list(string)
    print("ID   | Char | CharCount | URL")
    for index, character in enumerate(stringlist):    
        print ("{:<3}  | '{}'  |".format(index, character),  end = ' ')
        result = url_post(url, categorydata)
        charcount = get_charcount(result[soupindex] ,character)
        print("{:<9} | {} ".format(charcount, unescape(result[urlindex])))

rulespage = url_get(rulesurl)[soupindex]
maindiv = rulespage.find('main')
allbold = maindiv.find_all('strong')
rules = []
for bold in allbold:
    rules.append(bold.get_text())
rules = rules[rules.index('Your Program must'):rules.index('To enter')]
rules
for rule in rules:
    outputchars(rule)
    print('\n------\n')
