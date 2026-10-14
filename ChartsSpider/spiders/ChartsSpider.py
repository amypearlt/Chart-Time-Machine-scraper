import scrapy
from datetime import date, timedelta

class ChartsSpider(scrapy.Spider):
    name = "charts"

    def start_requests(self):
        from_date = date.fromisoformat(self.from_date)
        to_date = date.fromisoformat(self.to_date)
        while from_date <= to_date:
            week_date = from_date + timedelta(days=6)
            url = f"https://www.charttimemachine.com/?format=keyword&date_from={from_date}&date_to={week_date}&pos_high=1&pos_low=100&results=100"
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={"from_date": from_date})
            from_date += timedelta(days=7)

    def parse(self, response, from_date):
        for chart in response.css("table.chart_table tr:has(td)"):
            item = {
                "position": chart.css("td div::text").get(),
                "artist":   chart.css("td:nth-child(2) a::text").get(),
                "song":     chart.css("td:nth-child(3) a::text").get(),
                "label":    chart.css("td:nth-child(4) a::text").get(),
                "week":     from_date.isoformat(),
            }
            song_url = chart.css("td:nth-child(3) a::attr(href)").get()
            yield response.follow(song_url, callback=self.parse_song, cb_kwargs={"item": item}, dont_filter=True)

    def parse_song(self, response, item):
        item["genre"] = response.css('div.artist_info_left:contains("Genre") + div.artist_info_right::text').get()
        item["subgenre"] = response.css('div.artist_info_left:contains("Style") + div.artist_info_right::text').get() or item["genre"]
        yield item