import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    tag = None

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        self.tag = getattr(self, 'tag', None)
        if self.tag is not None:
            url = url + 'tag/' + self.tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            if self.tag is None:
                yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                }
            else:
                yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
