import json
import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup

class MalprojectSpider(scrapy.Spider):
    name = "malProject"
    allowed_domains = ["myanimelist.net"]
    start_url = "http://myanimelist.net/people/"
    urls = []

    def start_requests(self):
        with open('cfg.json', 'r') as f:
            data = json.load(f)
            self.urls.append(self.start_url+data['id1'])
            self.urls.append(self.start_url+data['id2'])
            # for url in self.urls:
            yield SeleniumRequest(url=self.urls[0],
                                wait_time=50,
                                callback=self.parse_first)

    def parse_first(self, response):
        seiyuu = BeautifulSoup(response.text, 'lxml')
        animesList = seiyuu.findAll(class_="js-people-title")
        name = seiyuu.find(class_="title-name h1_bold_none").text.replace(', ', '')
        yield SeleniumRequest(url=self.urls[1],
                                wait_time=50,
                                callback=self.parse_second,
                                meta={'list': animesList, 'name': name})
        

    def parse_second(self, response):
        seiyuu = BeautifulSoup(response.text, 'lxml')
        animesList = seiyuu.findAll(class_="js-people-title")
        name = seiyuu.find(class_="title-name h1_bold_none").text.replace(', ', '')
        animesList1 = response.meta.get('list')
        name1 = response.meta.get('name')
        file_name = name1+'__'+name
        same_anime = [value for value in animesList1 if value in animesList]
        with open(file_name+".txt", "w") as file:
            for anime in same_anime:
                file.write(anime.text+'\n')
