import scrapy
from datetime import date, timedelta

class ChartsSpider(scrapy.Spider):
    name = "charts"

    def get_date(self):
        minimum_date = date(1952,11,14)
        maximum_date = date(1999,12,26)
        options = ["year", "decade", "week"]
        selected_option = [arg for arg in options if hasattr(self, arg)]
        if hasattr(self, "from_date") != hasattr(self, "to_date"):
            raise ValueError("Expected both arguments: -a from_date=YYYY-MM-DD, -a to_date=YYYY-MM-DD")
        if hasattr(self, "from_date"):
            selected_option.append("range")
        if len(selected_option) > 1:
            raise ValueError("Expected one search option: -a year=YYYY | -a decade=YYYY | -a week=YYYY-MM-DD | -a from_date=YYYY-MM-DD, -a to_date=YYYY-MM-DD")

        if "year" in selected_option:
            year = int(self.year)
            from_date = date(year,1,1)
            to_date = date(year,12,31)
        elif "decade" in selected_option:
            decade = int(self.year)
            if decade % 10 != 0:
                raise ValueError("Expected decade to end with 0")
            from_date = date(decade,1,1)
            to_date = date(decade+9,12,31)
        elif "week" in selected_option:
            from_date = date.fromisoformat(self.week)
            to_date = from_date + timedelta(days=6)
        elif "range" in selected_option:
            from_date = date.fromisoformat(self.from_date)
            to_date = date.fromisoformat(self.to_date)
        else:
            from_date = minimum_date
            to_date = maximum_date

        if from_date > to_date:
            raise ValueError("from_date cannot be greater than end_date")
        if from_date < minimum_date:
            raise ValueError("from_date cannot be before 1952-11-14")
        if to_date > maximum_date:
            raise ValueError("to_date cannot be after 1999-12-26")
        return from_date, to_date

    def start_requests(self):
        try:
            from_date, to_date = self.get_date()
        except ValueError as error:
            self.logger.error(f"Invalid arguments: {error}")
            return
        
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