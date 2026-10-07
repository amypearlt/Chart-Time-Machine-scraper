**Weekly UK Top 100 Singles Charts**

###### 

###### A brief definition of web crawling and web scraping



**Web Crawler:** An Internet bot that systematically browses the World Wide Web.

A web crawler starts with an initial list of URLs to visit, which are called *seeds*. When visiting these URLs, the crawler identifies all of the hyperlinks in the retrieved webpages, and adds them to the list of URLs to visit, called the *crawl frontier*. URLs from the frontier are recursively visited. 



**Web Scraper:** A process in which data is extracted from webpages and entered into a local database.

A web scraper parses a webpage's DOM and identifies the HTML elements which contain relevant data. The data is extracted and converted into a structured format.[^1]



I used Scrapy, a Python framework for web crawling and scraping, in order to extract data from my target website/s.



**Web scraping process, via Scrapy**

(1) Identify a website to scrape from, that also allows scraping.

I had to choose a UK charts website where web scraping is permissible, defined by their *robots.txt* file. This meant I was forced to choose from older, often outdated websites (which wouldn't have to worry about Internet bots during the time in which they were active), but the structure of these websites were often simpler, and it would therefore be easier for me to identify CSS selectors which pointed to the desired data within the DOM. Since the old websites would use old HTML queries within their URLs, it made iterating through each weekly chart also easier.

(2) Identify and collect seed URLs.

In this case.....

I iterated through the URLs, constructing the URL's query for every week within the time frame. 

(3) Identify and input CSS selectors which contain the relevant data.

(4) Choose filetype

I chose CSV as a simple format for storing the data. 



I created a subclass of Scrapy's Spider class, giving a *name* and *start\_urls* for the scraper. Overwrite the parse function, which takes a webpage as an argument in *response*, and use Path library to write the body of each URL into a new file. The *.css()* method allows to search the webpage's HTML using a given CSS selector, which is composed of an HTML element and its class. *.get()* retrieves the first match, while *.getall()* retrieves all matches. Inspect element to find CSS selectors.[^2]



Run *scrapy crawl charts -O charts.csv*



[^1]: https://oxylabs.io/blog/web-scraping

[^2]: https://docs.scrapy.org/en/latest/intro/tutorial.html

