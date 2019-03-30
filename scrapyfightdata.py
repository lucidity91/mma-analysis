import scrapy, os, csv
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess

class fighterRecords(CrawlSpider):
    name = 'record_extractor'
    allowed_domains = ['www.sherdog.com']

    rules = (
        Rule(LinkExtractor(allow=('fighter'), restrict_css=('.content.table',)), callback='parse_fighter'),
    )

    def parse_fighter(self, response):
        # these variables specify the location of data in the html file
        # using xpath or css
        NAME = '.module.bio_fighter.vcard .fn::text'
        WINS = '.module.bio_fighter.vcard .bio_graph .counter::text'
        LOSSES = '.module.bio_fighter.vcard .bio_graph.loser .counter::text'
        CLASS = '.module.bio_fighter.vcard .item.wclass .title a::text'

        yield {
            'name' : response.css(NAME).get(),
            'wins' : response.css(WINS).get(),
            'losses' : response.css(LOSSES).get(),
            'class' : response.css(CLASS).get(),
        }

        NEXT_PAGE = '.module.fight_history a::attr(href)'
        next = response.css(NEXT_PAGE).get()
        if next:
            yield scrapy.Request (
                response.urljoin(next),
                callback=self.parse_fighter
            )

class matchFinder(scrapy.Spider):
    pass


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'data.csv'
})

URL = 'https://www.sherdog.com/fighter/Khabib-Nurmagomedov-56035'
DEPTH = 3

# get input url from user
#print('Root fighter URL: ')
#URL = input()

# get maximum crawl depth 
#print('Specify depth limit: ')
#DEPTH = input()

process.crawl(fighterRecords, start_urls=[URL])
process.start()

total_wins = 0
total_losses = 0

# open generate csv and print contents
with open('data.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    opp_list = list(reader)
    for row in opp_list[1:]: # skip reading header
        print(row)
        total_wins += float(row[1])
        total_losses += float(row[2])

csvFile.close()

# delete csv when finished
os.remove('data.csv')

print ("\nTotal wins for opponents: %.0f" % (total_wins))
print ("Total losses for opponents: %.0f" % (total_losses))
print ("\nWin/loss ratio for opponents combined: %.2f" % (total_wins/total_losses))
