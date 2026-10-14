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
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={"start_date": start_date})
            start_date += timedelta(days=7)

    def parse(self, response, start_date):
        for chart in response.css("table.chart_table tr:has(td)"):
            item = {
                "position":      chart.css("td div::text").get(),
                "artist":        chart.css("td:nth-child(2) a::text").get(),
                "song":          chart.css("td:nth-child(3) a::text").get(),
                "label":         chart.css("td:nth-child(4) a::text").get(),
                "week":          start_date.isoformat(),
            }
            song_url = chart.css("td:nth-child(3) a::attr(href)").get()
            yield response.follow(song_url, callback=self.parse_song, cb_kwargs={"item": item}, dont_filter=True)

    def parse_song(self, response, item):
        item["genre"] = response.css("div.artist_info_right:nth-of-type(14)::text").get()
        item["subgenre"] = response.css("div.artist_info_right:nth-of-type(17)::text").get()
        yield item