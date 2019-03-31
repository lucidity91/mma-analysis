# Eric Mu
# Apr. 1, 2019
# 001201773
# CPSC 4310 Project
# File: fightdata.py
# Purpose: Contains classes used for extracting fight data

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
        visited = []

        fightHistory = self.soup.find_all('div', {'class': 'module fight_history'})

        for div in fightHistory:
            # make sure we are grabbing links from fight history div
            if ('History' in div.find('h2').text.strip()):
                contentTable = div.find('div', {'class': 'content table'})
                oppUrls = contentTable.find_all('a', href=True)

                for urls in oppUrls:
                    # only get urls that link to another fighter
                    if ('fighter' in str(urls) and str(urls) not in visited):
                        # mark as visited and extract data
                        visited.append(str(urls))
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
        matchTable = self.soup.find('div', {'class': 'module event_match'})
        prelims = matchTable.find_all('tr', {'itemprop': 'subEvent'})

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

class UpcomingEvents(object):
    def __init__(self):
        while True:
            print('Select one of the following MMA promotions: ')
            print('1) UFC')
            print('2) Bellator')
            choice = int(input())

            if choice == 1:
                promo = "https://www.sherdog.com/organizations/Ultimate-Fighting-Championship-UFC-2"
                break
            elif choice == 2:
                promo = "https://www.sherdog.com/organizations/Bellator-MMA-1960"
                break
            else:
                print('Invalid choice, try again.')

        org = requests.get(promo)

        # store base url for later use
        parsed_uri = urlparse(promo)
        self.base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        # load url into bs4 for parsing
        self.soup = BeautifulSoup(org.text, 'html.parser')

    def getUpcoming(self):
        tbody = self.soup.find('table', {'class': 'event'})
        events = tbody.find_all('tr', {'itemtype': 'http://schema.org/Event'})

        count = 0
        print()

        # list all upcoming events
        for event in events:
            eventName = event.find('span', {'itemprop': 'name'}).text.strip()
            print(str(count) + ") " + eventName)
            count = count + 1

        # get user selection
        while True:
            selection = int(input("\nSelect one of the above events to analyze: "))
            if selection < 0 or selection > len(events)-1:
                print('Invalid selection, try again.')
            else:
                eventUrl = urljoin(self.base, events[selection].find('a', {'itemprop': 'url'})['href'])
                break

        return str(eventUrl)