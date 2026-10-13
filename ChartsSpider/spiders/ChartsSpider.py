import scrapy
from datetime import date, timedelta

class ChartsSpider(scrapy.Spider):
    name = "charts"

    def start_requests(self):
        start_date = date(1975,1,5)
        end_date = date(1975,12,31)
        while start_date <= end_date:
            start_week = start_date + timedelta(days=6)
            url = f"https://www.charttimemachine.com/?format=keyword&date_from={start_date}&date_to={start_week}&pos_high=1&pos_low=100&results=100"
            yield scrapy.Request(url, self.parse)
            start_date += timedelta(days=7)

    def parse(self, response):
        for chart in response.css("table.chart_table tr:has(td)"):
            yield {
                "position": chart.css("td              div::text").get(),
                "artist":   chart.css("td:nth-child(2) a::text").get(),
                "song":     chart.css("td:nth-child(3) a::text").get(),
                "week":     chart.css("td:nth-child(5) span.show_mobile::text").get(),
                "url":      response.url,
            }