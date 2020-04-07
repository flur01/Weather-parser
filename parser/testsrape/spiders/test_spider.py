import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    #start_urls =['https://www.gismeteo.ua/weather-zaporizhia-5093/']

    def start_requests(self):
        url = "https://www.gismeteo.ua/weather-zaporizhia-5093/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = {}
        data['Temperature'] = []
        data['Sky'] = []
        temperature = response.css('div.widget__row.widget__row_table.widget__row_temperature').css('div.values')
        for t_value in temperature.css('div.value'): 
            data['Temperature'].append(t_value.css('span.unit.unit_temperature_c::text').getall())
            data['Sky'].append(response.css('div.widget__row.widget__row_table.widget__row_icon').css('span.tooltip::attr(data-text)').get())
        yield data
