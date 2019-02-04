# -*- coding: utf-8 -*-
import scrapy
import hext


class ToScrapeHextSpider(scrapy.Spider):
    name = "toscrape-hext"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]
    rule_quotes = hext.Rule(
        """<div class="quote">
             <span class="text" @text:text />
             <span>
               <small class="author" @text:author />
             </span>
             <div>
               <?a class="tag" @text:tags />
             </div>
           </div>""");
    rule_next_page_url = hext.Rule(
        """<li class="next">
             <a href:next_page_url />
           </li>""");

    def parse(self, response):
        html = hext.Html(response.text)
        quotes = self.rule_quotes.extract(html)
        yield from quotes

        next_page_url = self.rule_next_page_url.extract(html)
        url = next(iter(next_page_url), None)
        if url is not None:
            yield scrapy.Request(response.urljoin(url["next_page_url"]))

