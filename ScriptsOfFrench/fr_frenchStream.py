import requests
from scrapy import Selector
import re

class frenchStream:

    def start(self, url):
        i = 1

        while i <= 948:
            baseUrl = url + "page/" + str(i) + "/"
            response = requests.get(url=baseUrl)
            if response.ok is True:
                selector = Selector(text=response.content)
                for movie in selector.xpath("//div[@id='dle-content']//div[@class='short']//div[@class='short-in nl']"):
                    movieUrl = (movie.xpath(".//a[@class='short-poster img-box with-mask']//@href").get())
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    if movieUrl is not None:
                        self.details(url=movieUrl)
                print("SAYFA: ",i)
                i += 1

    def parseImage(self,selector):
        image=selector.xpath("//div[@class='fposter']//img//@src").get()
        return image

    def parseYear(self,selector):
        year=""
        yearList=selector.xpath("//div[@class='flist clearfix']//ul//li//text()").getall()
        # print(yearList)
        try:
            for realYear in yearList:
                year=year+realYear
            # print(year)
            dummy=re.findall("\d\d\d\d", year)
            # print(dummy)
            if int(dummy[0]) <= 2022:
                year = dummy[0]
                return year
            if int(dummy[1]) <= 2022:
                year = dummy[0]
                return year

        except:
            year="2018"
            return year

    def parseName(self,selector):
        name=selector.xpath("//div[@class='fmid']//h1/text()").get()
        if name is not None:
            if "'" in name:
                name=name.replace("'","")
            if name[0] == " ":
                name[0].replace(" ","")

        return name

    def parseDescription(self,selector):
        try:
            description=selector.xpath("//div[@class='fmid']//div[@id='s-desc']//text()").get()
            if '\n' in description:
                description=description.replace("\n","")
            return description
        except:
            return "......."

    def parseGenre(self, selector):
        sourceList=[]
        try:
            genreList=selector.xpath("//div[@class='flist clearfix']//ul[@id='s-list']//li[@rel='nofollow']//a//@href").getall()
            for genre in genreList:
                if "genre" in genre:
                    genre=genre.split("genre")[1]
                    genre=genre.split("/")[1]
                    if "%" not in genre:
                        sourceList.append(genre)
            if sourceList.__len__()<1:
                sourceList.append("Comédie")
                sourceList.append("Drame")

            return sourceList
        except:
            sourceList.append("Action")
            return sourceList
    def iframeList(self,selector):
        sourceList=[]
        try:
            iframList=selector.xpath("//div[@class='tabs-sel']//nav[@id='primary_nav_wrap']//nav//ul//li//a//@href").getall()
            dummy=""
            for iframe in iframList:
                if "uqload" in iframe:
                    if dummy not in iframe:
                        sourceList.append(iframe)
                    dummy = iframe

            if len(sourceList) ==0:
                for ifr in iframList:
                    if "uqload" in ifr:
                        sourceList.append(ifr)
                        break

            return sourceList
        except:
            return sourceList

    def parseDirector(self,selector):
        sourceList=[]
        try:
            directorList=selector.xpath("//div[@class='flist clearfix']//ul[@id='s-list']//li[@rel='nofollow']//a//@href").getall()
            for director in directorList:
                if "director" in director:
                    director=director.split("director")[1]
                    director=director.split("/")[1]
                    director=director.replace("+"," ")
                    if "%" not in director:
                        sourceList.append(director)
            return sourceList
        except:
            return sourceList
    def parseActor(self,selector):
        sourceList = []
        try:
            actorList = selector.xpath("//div[@class='flist clearfix']//ul[@id='s-list']//li[@rel='nofollow']//a//@href").getall()
            for actor in actorList:
                if "actors" in actor:
                    actor = actor.split("actor")[1]
                    actor = actor.split("/")[1]
                    actor = actor.replace("+", " ")
                    if "%" not in actor:
                        sourceList.append(actor)
            return sourceList
        except:
            sourceList

    def details(self, url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        print(url)

        name = self.parseName(selector=selector)
        print("Name:", name)

        year = self.parseYear(selector=selector)
        print("Year:", year)

        image = self.parseImage(selector=selector)
        print("Picture: ", image)

        genreList = self.parseGenre(selector=selector)
        print("Genre: ",genreList)

        directorList=self.parseDirector(selector=selector)
        print("Director: ",directorList)

        actorList=self.parseActor(selector=selector)
        print("Actor: ",actorList)

        description = self.parseDescription(selector=selector)
        print("Description: ", description)

        iframeList = self.iframeList(selector=selector)
        print("Iframe List:",iframeList)


if __name__ == '__main__':
    frenchStream().start(url="https://french-stream.re/xfsearch/qualit/")