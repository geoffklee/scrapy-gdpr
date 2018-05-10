""" A scrapy module to find things that might of of interest
    when implementing GDPR rules """

from urllib.parse import urlparse
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WebThing(scrapy.Item):
    """ An item to hold our data """
    t_type = scrapy.Field()
    page = scrapy.Field()
    f_id = scrapy.Field()
    name = scrapy.Field()
    action = scrapy.Field()
    inputs = scrapy.Field()


class GDPRAudit(CrawlSpider):
    """ Find things of interest to a GDPR audit """

    name = 'gdpr_audit'
    allowed_domains = None
    start_urls = None

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    out_filename = 'out.csv'
    out_file = None
    exporter = None

    def __init__(self, *args, **kwargs):
        super(GDPRAudit, self).__init__(*args, **kwargs)
        self.start_urls = open(self.urlfile, 'r').read().split('\n')
        self.allowed_domains = [urlparse(u)[1] for u in self.start_urls]
        print('ALLOWED DOMAINS: ' + ','.join(self.allowed_domains))

    def parse_item(self, response):
        """ For each response, find the items we
        are interested in """
        forms = self.find_forms(response)
        for form in forms:
            yield form

        frames = self.find_iframes(response)
        for frame in frames:
            yield frame

    def find_forms(self, response):
        """ Look for HTML forms and collect some data about them """
        # Find any <form> elements, ignoring things that look like
        # search boxes. FIXME: parameterise the ignore list.
        form_selector = '//form[not(contains(@id, "search"))]'
        for form in response.xpath(form_selector):
            form_data = WebThing()
            form_data['t_type'] = 'form'
            form_data['page'] = response.request.url
            form_data['action'] = form.xpath('@action').extract_first()
            form_data['f_id'] = form.xpath('@id').extract_first()
            form_data['name'] = form.xpath('@name').extract_first() or ''
            # Ignore hidden form inputs
            form_data['inputs'] = ";".join(
                form.xpath('.//input[not(@type="hidden")]/@name').extract())
            yield form_data

    def find_iframes(self, response):
        """ Look for iframes and collect some data about them """
        iframe_selector = '//iframe'
        for iframe in response.xpath(iframe_selector):
            frame_data = WebThing()
            frame_data['t_type'] = 'iframe'
            frame_data['page'] = response.request.url
            frame_data['action'] = iframe.xpath('@src').extract_first()
            yield frame_data
