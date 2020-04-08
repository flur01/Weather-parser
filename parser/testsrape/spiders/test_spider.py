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
        data['Sky_middle'] = []
        data['Wind'] = []
        data['Rainfall'] = []
        data['Date'] = []
        
        temperature = response.css('div.values')
        for t_value in temperature: 
            data['Temperature'].append(t_value.css('span.unit.unit_temperature_c::text').getall())
        
        data['Sky'].append(response.css('div.widget__row.widget__row_table.widget__row_icon').css('span.tooltip::attr(data-text)').getall())
        data['Sky_middle'].append(response.css('div.tab.tooltip::attr(data-text)').get())

        wind = response.css('div.widget__row.widget__row_table.widget__row_wind-or-gust').css('div.widget__item')
        for wind_value in wind.css('div.w_wind'):
            data['Wind'].append(wind_value.css('span.unit.unit_wind_m_s::text').getall()[0].replace(' ', '').replace(f'\n', '')) 
        
        if response.css('div.w_prec__without::text'):
            data['Rainfall'].append(response.css('div.w_prec__without::text').getall()[0])

        else:
            for rain in response.css('div.w_prec__value::text'):
                data['Rainfall'].append(rain.getall()[0].replace(' ', '').replace(f'\n', ''))
        
        data['Date'].append(response.css('div.tab.tooltip').css('div.date::text').getall()[0].replace(' ', '').replace(f'\n', ''))

        yield data
