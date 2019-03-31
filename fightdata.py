# Eric Mu
# Apr. 1, 2019
# 001201773
# CPSC 4310 Project
# File: fightdata.py
# Purpose: Program for extracting fighter data

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class Fighter(object):
    def __init__(self, name, wins, losses, wtclass):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.wtclass = wtclass

    # function for printing fighter data
    def print(self):
        print('Name: ' + self.name + ' | Record: ' + self.wins + '-' + self.losses + 
              ' | Weightclass: ' + self.wtclass)

class ExtractFighterInfo(object):
    # default constructor
    def __init__(self, link):
        # specified root url
        url = requests.get(link)

        # store base url for later use
        parsed_uri = urlparse(link)
        self.base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        # load url into bs4 for parsing
        self.soup = BeautifulSoup(url.text, 'html.parser')

    # function for extracting fighter data, returns a fighter
    def getInfo(self):
        # extract name
        name = self.soup.find('span', {'class': 'fn'}).text.strip()

        # extract wins & loss
        record = self.soup.find_all('span', {'class': 'counter'})
        wins = record[0].text.strip()
        losses = record[1].text.strip()

        # extract weightclass
        wtclass = self.soup.find('strong', {'class': 'title'}).text.strip()

        return Fighter(name, wins, losses, wtclass)

    # function for parsing opponents, returns a list of fighters
    def getOppInfo(self):
        opponents = []

        fightHistory = self.soup.find_all('div', {'class': 'module fight_history'})

        for div in fightHistory:
            # make sure we are grabbing links from fight history div
            if ('History' in div.find('h2').text.strip()):
                contentTable = div.find('div', {'class': 'content table'})
                oppUrls = contentTable.find_all('a', href=True)

                for urls in oppUrls:
                    # only get urls that link to another fighter
                    if ('fighter' in str(urls)):
                        print('Extracting data from opponent: ' + str(urls.text.strip()))

                        # make a new request to join opponent page
                        link = urljoin(self.base, urls['href'])
                        url = requests.get(link)
                        self.soup = BeautifulSoup(url.text, 'html.parser')

                        opponents.append(self.getInfo())

        return opponents

class EventParser(object):
    def __init__(self, link):
        # specified eveny url
        event = requests.get(link)

        # store base url for later use
        parsed_uri = urlparse(link)
        self.base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        # load url into bs4 for parsing
        self.soup = BeautifulSoup(event.text, 'html.parser')

        eventName = self.soup.find('span', {'itemprop': 'name'}).text.strip()
        print(eventName)

    def getMatch(self):
        match = []
        matchList = []

        # get main event
        mainEvent = self.soup.find('div', {'class': 'module fight_card'})
        matchHeader = mainEvent.find_all('h3')

        leftFighter = matchHeader[0].find('a', href=True)
        rightFighter = matchHeader[1].find('a', href=True)

        leftFighterURL = urljoin(self.base, leftFighter['href'])
        rightFighterURL = urljoin(self.base, rightFighter['href'])

        match.append(leftFighterURL)
        match.append(rightFighterURL)

        print('Adding match: ' + leftFighter.text.strip() + ' vs ' + rightFighter.text.strip())
        matchList.append(match)

        # get other matches
        tbody = self.soup.find('tbody')
        prelims = tbody.find_all('tr', {'itemprop': 'subEvent'})

        # each table row contains one preliminary fight
        # add them one by one to the match list
        for prelim in prelims:
            fight = prelim.find('meta', {'itemprop': 'name'})
            print('Adding match: ' + fight['content'])

            matchUrls = prelim.find_all('a', {'itemprop': 'url'})
            
            match = []
        
            for url in matchUrls:
                fullUrl = urljoin(self.base, url['href'])
                match.append(fullUrl)

            matchList.append(match)

        return matchList
