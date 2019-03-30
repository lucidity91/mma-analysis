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
    def getOppInfo(self, depth = 1):
        opponents = []

        contentTable = self.soup.find('div', {'class': 'content table'})
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


extractor = ExtractFighterInfo('https://www.sherdog.com/fighter/Khabib-Nurmagomedov-56035')

fighter = extractor.getInfo()

fighter.print()

opponents = extractor.getOppInfo(1)

for opp in opponents:
    opp.print()