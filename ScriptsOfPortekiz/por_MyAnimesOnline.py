import re
import requests
from scrapy import Selector

class MyAnimesOnline:

    def start(self,url):
        i = 6
        Cartoon="https://www.myanimesonline.biz/Categorias/cartoon/"
        self.parseCartoonPage(Cartoon)
        while i > 0:
            baseUrl = url + "page/" + str(i) + "/"
            self.parsePage(url=baseUrl)
            print(baseUrl)
            print("+++++++++++++++++++++++++++++++++++++++++++++++")
            print("SAYFA:",i)
            i -= 1

    def parseCartoonPage(self,url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)
        print("-------------Cartoon-------------")
        serieList = selector.xpath("//ul[@class='videos']//li//div[@class='video-conteudo']//a//@href").getall()
        timer = 0
        while timer < len(serieList):
            self.parseSerieInformation(url=serieList[timer])
            timer = timer + 1
    def parsePage(self,url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        serieList=selector.xpath("//div[@class='videos-row']//ul[@class='videos']//li//div[@class='video-conteudo']//a//@href").getall()
        timer=0
        while timer< len(serieList):
            self.parseSerieInformation(url=serieList[timer])
            timer=timer+1



    def parseSerieInformation(self,url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)
        serieSeason=1

        serieName=selector.xpath("//div[@class='post-conteudo']//h1//text()").get()
        if "(" in serieName:
            serieName=serieName.split(" (Dublado")[0]

        serieDescription=selector.xpath("//div[@class='post-texto']//p//text()").get()


        serieImage=selector.xpath("//div[@class='post-capa']//img//@src").get()


        genreList=[]
        serieGenre=selector.xpath("//div[@class='post-tags']//a//@title").getall()

        for genres in serieGenre:
            genreList.append(genres)

        serieEpisodes=[]

        episodes=selector.xpath("//ul[@class='episodios']//li//a//@href").getall()

        for ep in episodes:
            serieEpisodes.append(ep)

        timer=0

        boobs=True
        yearList=selector.xpath("//ul[@class='post-infos']//li//span//text()").getall()
        seasonYear=2012 + len(genreList)
        for year in yearList:
            if 1 == len(re.findall("\d\d\d\d", year)):
                if "/" in year:
                    year=year.split("/")
                    year=year[len(year)-1]
                    seasonYear=year

        for gen in genreList:
            if "Cartoon" in gen:
                boobs=False

        while timer<len(serieEpisodes):
            episodeNumber=timer+1
            episodeurl=serieEpisodes[timer]
            if boobs is False:
                self.parseEpisodeIframe(url=episodeurl,name=serieName,image=serieImage,genre=genreList,description=serieDescription,season=serieSeason,episode=episodeNumber,year=seasonYear)
            timer=timer+1



    def parseEpisodeIframe(self,url,name,image,genre,description,season,episode,year):
        response = requests.get(url=url)
        selector = Selector(text=response.content)
        episodeIframe=[]
        iframe=selector.xpath("//div[@class='post-video']//iframe//@src").get()

        if iframe is not None:
            if "https://" not in iframe:
                episodeIframe.append("https://"+iframe)
            else:
                episodeIframe.append(iframe)


        print("src:",url)
        print("name:", name)
        print("year:",year)
        print("image:", image)
        print("genre:", genre)
        print("description:", description)
        print("season:", season)
        print("episode:", episode)
        print("iframe:",episodeIframe)
        print("**************************************")

if __name__ == '__main__':
    MyAnimesOnline().start(url="https://www.myanimesonline.biz/dublados/")
