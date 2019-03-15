import scrapy, os, csv
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess

class fightFinder(CrawlSpider):
    name = 'fight_data_extractor'
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


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'data.csv'

})

URL = 'https://www.sherdog.com/fighter/Khabib-Nurmagomedov-56035'

# get input url from user
#print('Root fighter URL: ')
#URL = input()

process.crawl(fightFinder, start_urls=[URL])
process.start()

total_wins = 0
total_losses = 0

# open generate csv and print contents
with open('data.csv', 'r') as csvFile:
    #reader = csv.DictReader(csvFile, fieldnames=('name', 'wins', 'losses', 'class'))
    reader = csv.reader(csvFile)
    opp_list = list(reader)
    for row in opp_list[1:]:
        print(row)
        total_wins += int(row[1])
        total_losses += int(row[2])

csvFile.close()

# delete csv when finished
os.remove('data.csv')

print ("\nTotal wins for opponents: %i" % (total_wins))
print ("\nTotal losses for opponents: %i" % (total_losses))
print ("\nWin/loss ratio for opponents combined: %d" % (total_wins/total_losses))
