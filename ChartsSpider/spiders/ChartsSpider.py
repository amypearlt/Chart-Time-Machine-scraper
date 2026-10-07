import scrapy

class ChartsSpider(scrapy.Spider):
    name = "charts"
    start_urls = [
        "https://www.charttimemachine.com/?format=keyword&date_from=1975-01-05&date_to=1975-01-11&pos_high=1&pos_low=100&results=100",
    ]

    def parse(self, response):
        for chart in response.css("table.chart_table tr:has(td)"):
            yield {
                "position": chart.css("td              div::text").get(),
                "artist":   chart.css("td:nth-child(2) a::text").get(),
                "song":     chart.css("td:nth-child(3) a::text").get(),
                "week":     chart.css("td:nth-child(5) span.show_mobile::text").get(),
            }