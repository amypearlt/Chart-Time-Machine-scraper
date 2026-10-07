I used Scrapy, a Python framework for web crawling and scraping, in order to extract data from [The Chart Time Machine](https://www.charttimemachine.com).

Run `scrapy crawl charts -O charts.csv`

## A brief definition of web crawling and web scraping

##### **Web Crawler:** An Internet bot that systematically browses the World Wide Web.

A web crawler starts with an initial list of URLs to visit, which are called *seeds*. When visiting these URLs, the crawler identifies all of the hyperlinks in the retrieved webpages, and adds them to the list of URLs to visit, called the *crawl frontier*. URLs from the frontier are recursively visited. 

##### **Web Scraper:** A process in which data is extracted from webpages and entered into a local database.

A web scraper parses a webpage's DOM and identifies the HTML elements which contain relevant data. The data is extracted and converted into a structured format.[^1]

## My web scraping process, via Scrapy

##### **(1)** Identify a suitable website to scrape data from.

I had to choose a UK charts website (Weekly UK Top 100 Singles Charts) where web scraping is permissible, defined by their *robots.txt* file. This meant I was forced to choose from older, often outdated websites (which wouldn't have to worry about Internet bots during the time in which they were active), but the structure of these websites were often simpler, and it would therefore be easier for me to identify CSS selectors which pointed to the desired data within the DOM.

##### **(2)** Identify and collect seed URLs.

In order to access chart information on the website, the user must fill in a dropdown menu requiring a date range and a range of chart positions. Since the website exposes search criteria through their URL's query parameters, the process of iterating through each weekly chart was convenient; I constructed the URL's query for every week within the desired time frame. 

##### **(3)** Identify CSS selectors which contain the relevant data.

Using my browser's *Inspect Element* feature, I could view the HTML code of the webpage and determine the CSS selectors used to contain data such as the song name, the song's artist, the peak position of the song, and so on.[^2]

##### **(4)** Choose a filetype to store the data.

I chose CSV as a standard format for storing data, making it convenient to export into spreadsheets or databases.

[^1]: https://oxylabs.io/blog/web-scraping
[^2]: https://docs.scrapy.org/en/latest/intro/tutorial.html