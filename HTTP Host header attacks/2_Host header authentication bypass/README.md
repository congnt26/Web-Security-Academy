# Host header authentication bypass
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-authentication-bypass

## Phân tích
- Bắt gói `GET /` vào Repeater, đổi Host header sang 1 host khác xem thử có access homepage ko. Ta thấy vẫn get 200 OK
![img.png](img.png)
- Access vào file `robots.txt` xem có gì hay ho ko. Ta thấy có /admin panel nhưng đã bị chặn
![img_1.png](img_1.png)

![img_2.png](img_2.png)

- Giải thích thêm về file [robots.txt](#a1)
- Ta thấy chỉ local users mới access đc

## Resolve lab

- Thay Host với localhost, mục đích để đánh lừa server là request được gởi từ máy local. Ta thấy có thể thấy đc path để xóa user
![img_3.png](img_3.png)

![img_4.png](img_4.png)
- User đã đc xóa (nhận gói 302)

![img_5.png](img_5.png)


<a id='a1'></a>
## robots.txt file
- A robots.txt file is a text file that webmasters create to instruct web robots (or web crawlers) how to crawl and index pages on their website. 
The robots.txt file is a standard used by websites to communicate with web crawlers and other automated agents accessing the site.

- A bot is an automated computer program that interacts with websites and applications. 
There are good bots and bad bots, and one type of good bot is called a web crawler bot. 
These bots "crawl" webpages and index the content so that it can show up in search engine results. 
A robots.txt file helps manage the activities of these web crawlers so that they don't overtax the web server hosting the website, or index pages that aren't meant for public view.

- In a robots.txt file with multiple user-agent directives, each disallow or allow rule only applies to the useragent(s) specified in that particular line break-separated set. If the file contains a rule that applies to more than one user-agent, a crawler will only pay attention to (and follow the directives in) the most specific group of instructions.

- Here’s an example:
![img_6.png](img_6.png)
  - Msnbot, discobot, and Slurp are all called out specifically, so those user-agents will only pay attention to the directives in their sections of the robots.txt file. All other user-agents will follow the directives in the user-agent: * group.
## What is a web crawler bot?
- A web crawler, also known as a spider or bot, is a program or automated script designed to browse the internet, visit web pages, and index their content.
- Search engines use web crawlers to gather information about web pages, index that information, and provide relevant search results to users.
- Web crawlers systematically follow links on web pages to discover and index new content. They play a crucial role in the functioning of search engines.


## List of web crawlers
The bots from the major search engines are called:

  - Google: Googlebot (actually two crawlers, Googlebot Desktop and Googlebot Mobile, for desktop and mobile searches)
  - Bing: Bingbot
  - DuckDuckGo: DuckDuckBot
  - Yahoo! Search: Slurp
  - Yandex: YandexBot
  - Baidu: Baiduspider
  - Exalead: ExaBot

## Internals of Search Engines
- To work effectively, search engines must understand the kind of information that is requested, and what kind of webpages from the web are relevant to the requested information. 
- For this purpose, search engines perform three important steps; crawling, indexing, and ranking.

### Crawling: The Digital Expedition
Crawling is the foundational step in the process of a search engine's operation. It's the mechanism by which search engines send out web crawlers, or bots, to explore the vast terrain of the internet. Think of them as intrepid digital explorers, mapping the online world.

Web Crawlers: What Are They?
Web crawlers, also known as spiders, are automated scripts that browse the web in a methodical and automated manner. Their mission is to discover, retrieve, and index content.

![img_7.png](img_7.png)

### Indexing: Organizing the Digital Library
Once web crawlers have successfully scoured the internet, the next crucial step is indexing. This is where the search engine takes the raw data collected by the crawlers and transforms it into a structured format, ready for rapid querying. It's akin to meticulously cataloging books in a vast digital library.
![img_8.png](img_8.png)

### Ranking: The Science of Relevance
The process of ranking is where the search engine truly shines. It's not just about finding all the webpages that match a query; it's about finding the most relevant, useful, and authoritative pages among those matches. This is a complex and continually evolving field, blending mathematics, computer science, psychology, and even art.
![img_9.png](img_9.png)


## What is Search Engine Optimization (SEO)?
Before summarizing what we learned in this article, let's take a brief look at why understanding search engine mechanism is so important, and discuss what Search Engine Optimization (SEO) is.

In the competitive world of the internet, visibility is key. That's where SEO comes in. SEO is a blend of art and science, employing techniques to enhance a website's visibility in search engine results.

Search engine optimization is used by business owners and website owners so that the search engine crawls their site more frequently, and so that it appears at the top of search engine results. Strategies are used to optimize, update and produce relevant content on the website so that it is displayed more frequently on the Search Engine Result Page (SERP).

In general, if one wants their website to get a higher rank, they should focus on the features that search engines use to rank pages that we discussed in earlier sections. Improving user experience, using more keywords, producing high-quality content along with proper layout are some of the important points to keep in mind when optimizing a webpage for search engines. These changes would allow the search engine crawlers to locate the site easily and give a higher rank as compared to other sites.
