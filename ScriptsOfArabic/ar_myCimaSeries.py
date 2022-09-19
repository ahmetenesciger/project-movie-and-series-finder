import requests
from scrapy import Selector

class MyCimaSeries:

    def siteLoop(self,url):
        pageNo=1
        while pageNo <= 67:
            tempUrl = url+str(pageNo)+"/"
            self.seriesListPage(url=tempUrl)
            # print("gelen url:",url)
            print("kacinci sayfa:",pageNo,"*************************")
            pageNo=pageNo+1



    def seriesListPage(self,url):
        seriesSourceList=[]
        response = requests.get(url=url)
        selector = Selector(text=response.content)
        seriesList=selector.xpath("//div[@class='Grid--MycimaPosts']//div[@class='GridItem']//a//@href").getall()
        print("seriesList:",seriesList)
        timer=0

        while len(seriesList) > timer:
            seriesSourceList.append(seriesList[timer])
            timer=timer+2

        timerNew=0

        while len(seriesSourceList) > timerNew:
            # print(seriesSourceList[timerNew])
            try:
                self.getSeries(url=seriesSourceList[timerNew])
                timerNew=timerNew+1
            except:
                print("dizi patladi")
                timerNew = timerNew + 1




    def getSeries(self,url):
        seasonNumber="1"
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        description = selector.xpath("//meta[@name='description']//@content").get()
        name = selector.xpath("//div[@class='Title--Content--Single-begin']//h1//text()").get()
        if name is not None:
            if "(" in name:
                name=name.split("(")[0]
                name=name.replace("\n","").replace("\t","")
        year=selector.xpath("//div[@class='Title--Content--Single-begin']//h1//a//text()").get()

        genre = []
        genreList = selector.xpath("//ul[@class='Terms--Content--Single-begin']//li//p//a//@href").getall()
        for gen in genreList:
            if "genre" in gen:
                gen=gen.replace("/","***").replace("-","+*+*+")
                if "+*+*+" in gen:
                    gen=gen.split("+*+*+")[1]
                    gen=gen.split("***")[0]
                    if "%" not in gen:
                        genre.append(gen)

        if len(genre)==0:
            genre.append("Drama")
            genre.append("Comedy")

        genreDenemeTimer=0
        while(len(genre) > 0):
            if "a" ==genre[genreDenemeTimer] or "n-a" == genre[genreDenemeTimer] or "n\A" == genre[genreDenemeTimer] or "n" == genre[genreDenemeTimer] or "A" == genre[genreDenemeTimer] or "-" == genre[genreDenemeTimer]:
                genre.remove(genre[genreDenemeTimer])
                break
            break

        if len(genre)==0:
            genre.append("Drama")
            genre.append("Comedy")

        image = selector.xpath("//mycima[@class='separated--top']//@style").get()
        image = image.split(")")[0]
        image = image.split("(")[1]

        seasonCheck=selector.xpath("//div[@class='List--Seasons--Episodes']").get()
        # print(seasonCheck)
        if seasonCheck is not None:
            seasonUrls=[]
            textUrl=[]
            season=selector.xpath("//div[@class='List--Seasons--Episodes']//a//@href").getall()
            seasonText=selector.xpath("//div[@class='List--Seasons--Episodes']//a//text()").getall()
            for text in seasonText:
                text=text.split(" ")
                if len(text) == 2:
                    text=text[0]+text[1]
                    textUrl.append(text)
                # print(text)
            # print(textUrl)
            timerText=0
            while len(textUrl) > timerText:
                seasonUrls.append(season[timerText])
                timerText=timerText+1
            # print(seasonUrls)

            timerSeason=0

            while len(seasonUrls) > timerSeason:
                self.getHaveSeasonEpisode(src=url,url=seasonUrls[timerSeason], name=name, image=image, description=description, genre=genre,seasonNumber=timerSeason+1,year=year)
                timerSeason=timerSeason+1




        else:
            episode=selector.xpath("//div[@class='Episodes--Seasons--Episodes Full--Width']//a//@href").getall()
            episode.reverse()

            # print("name",name)
            # print("year:",year)
            # print("image:",image)
            # print("episode",episode)
            # print("description",description)
            # print("genre:",genre)

            episodeLength=len(episode)
            timer=0
            while episodeLength > timer:
                self.getJustHaveEpisode(url=episode[timer],name=name,image=image,description=description,genre=genre,seasonNumber=seasonNumber,episodeNumber=timer+1,year=year)
                timer=timer+1



    def getJustHaveEpisode(self,url,name,image,description,genre,seasonNumber,episodeNumber,year):
        iframeList=[]
        response = requests.get(url=url)
        selector = Selector(text=response.content)


        episodeIframe=selector.xpath("//ul[@class='WatchServersList']//ul//li//btn//@data-url").getall()
        for iframe in episodeIframe:
            if "\n" in iframe:
                iframe = iframe.replace("\n", "")
                if "&Expires" in iframe or "\r" in iframe:
                    iframe=iframe.split("&Expires")[0]
                    iframe=iframe.replace("\r","")
                    if "uqload" in iframe:
                        if "https:" not in iframe:
                            iframeList.append("https:" + iframe)
                        else:
                            iframeList.append(iframe)
            else:
                if "&Expires" in iframe or "\r" in iframe:
                    iframe=iframe.split("&Expires")[0]
                    iframe=iframe.replace("\r","")
                    if "uqload" in iframe:
                        if "https:" not in iframe:
                            iframeList.append("https:" + iframe)
                        else:
                            iframeList.append(iframe)
        # seasonNumber="1"


        print("src1111:",url)
        print("season Number:",seasonNumber)
        print("episode Number:",episodeNumber)
        if "'" in name:
            name=name.replace("'"," ")
        print("name:",name)
        print("year:",year)
        print("Image:",image)
        print("Description",description)
        print("Genre",genre)
        if len(iframeList) ==0:
            iframeList.append("https://uqload.com/embed-Slavel.html?Key=iCTx5IdptCqtKS_174q8LQ")
        print("Iframe List",iframeList)
        print("******************Just-1-Season********************************")




    def getHaveSeasonEpisode(self,src,url,name,image,description,genre,seasonNumber,year):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        seasonList=selector.xpath("//div[@class='Episodes--Seasons--Episodes']//a//@href").getall()
        seasonList.reverse()

        timerSeason=0
        while len(seasonList) > timerSeason:
            self.getHaveSeasonIframe(src=src,url=seasonList[timerSeason], name=name, image=image, description=description, genre=genre,
                                     seasonNumber=seasonNumber,episodeNumber=timerSeason+1,year=year)
            timerSeason=timerSeason+1


    def getHaveSeasonIframe(self,src,url,name,image,description,genre,seasonNumber,episodeNumber,year):
        iframeList = []
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        episodeIframe = selector.xpath("//ul[@class='WatchServersList']//ul//li//btn//@data-url").getall()
        for iframe in episodeIframe:
            if "\n" in iframe:
                iframe=iframe.replace("\n","")
                if "&Expires" in iframe or "\r" in iframe:
                    iframe=iframe.split("&Expires")[0]
                    iframe=iframe.replace("\r","")
                    if "uqload" in iframe:

                        if "https:" not in iframe:
                            iframeList.append("https:" + iframe)
                        else:
                            iframeList.append(iframe)
            else:
                if "&Expires" in iframe or "\r" in iframe:
                    iframe = iframe.split("&Expires")[0]
                    iframe = iframe.replace("\r", "")
                    if "uqload" in iframe:

                        if "https:" not in iframe:
                            iframeList.append("https:" + iframe)
                        else:
                            iframeList.append(iframe)

        print("src1111:",src)
        if "'" in name:
            name=name.replace("'"," ")
        print("name:", name)
        print("year:",year)
        print("Image:", image)
        print("Description", description)
        print("Genre", genre)
        print("season Number:",seasonNumber)
        print("episode Number:",episodeNumber)
        print("iframeList:",iframeList)
        print("******************Have-Season********************************")







if __name__ == '__main__':
    MyCimaSeries().siteLoop(url="https://mycima.wiki/seriestv/new/?page_number=")
    # MyCimaSeries().getSeries(url="https://mycima.wiki/series/lupin/")
