#
#   Rube Codeberg submission for Craig Quirke at Pyconline AU 2020
#
#   scrapes rulesurl for bold list of rules (between "Your Program must" and "To enter:", finds a random page on wikipedia with the category "Programming languages" 
#    and outputs the number of times the given letter appears (case insensitive)
#
#   This program will make a large number of synchronous web requests, runtime dependant on bandwith and wikipedia response times.
#   sample output included in sample.txt
#

from datetime import datetime
startTime = datetime.now()

import requests
from bs4 import BeautifulSoup
from html import unescape

rulesurl = 'https://2020.pycon.org.au/program/sun/'
url = "https://en.wikipedia.org/wiki/Special:RandomInCategory"
categoryname = "Programming+languages"
categorydata = unescape("wpcategory={}".format(categoryname))

sessionindex = 0
soupindex = 1
urlindex = 2
characterinfo = [] 
rules = []

def url_post(url, rawPOSTdata="") -> list:
    #   Returns requests session object, page contents as bs4 object, and link to page (if found on wikipedia)
    headers    = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    session    = requests.Session()
    response   = session.post(url,headers=headers, data=rawPOSTdata)
    soup       = BeautifulSoup(response.content, 'html.parser')
    if "wikipedia" in url.lower():
        url = soup.find('link', {'rel': 'canonical'}).get('href')
    return [session, soup, url]

def url_get(url) -> list:
    #   Returns requests session object, page contents as bs4 object, and link to page (if found on wikipedia)
    headers    = {'User-Agent': 'Mozilla/5.0'} #, 'Content-Type': 'application/x-www-form-urlencoded'}
    session    = requests.Session()
    response   = session.get(url,headers=headers)
    soup       = BeautifulSoup(response.content, 'html.parser')
    return [session, soup, url]

def get_charcount(bs4page, character) -> int:
    #   Counts occurence of character in article content
    contentdivtext = bs4page.find(id="mw-content-text")
    charcount = contentdivtext.get_text().lower().count(character.lower())
    return charcount

def outputchars(string):
    #   print "table" of each character in string, and number of occurrences on a random wikipedia page
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
for bold in allbold:
    rules.append(bold.get_text())
rules = rules[rules.index('Your Program must'):rules.index('To enter')]
for rule in rules:
    outputchars(rule)
    print('\n------\n')

print("runtime: {}".format(datetime.now() - startTime))
