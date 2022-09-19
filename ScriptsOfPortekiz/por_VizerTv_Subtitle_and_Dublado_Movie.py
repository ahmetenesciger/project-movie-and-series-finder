import requests
import json
from scrapy import Selector

class VizerTV:

    def moviePages(self,baseUrl):
        i=0
        while(i<700):
            url=baseUrl+str(i)+"&saga=0&categoryFilterYearMin=1890&categoryFilterYearMax=2022&categoryFilterOrderBy=year&categoryFilterOrderWay=desc"
            print(url)
            movieIdList=[]
            response = requests.get(url=url)

            idList=response.text
            idList=idList.split('"list":')[1]
            idList=idList.split('","title":"')
            for id in idList:
                if ':{"url":"' in id:
                    id = id.split('{"url":"')[1]
                    id = "https://vizer.tv/filme/online/"+id
                    movieIdList.append(id)

            for movieId in movieIdList:
                self.details(url=movieId)

            print("sayfa sayisi:",i)
            i=i+1

    def getDubladoIframe(self,url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        movieMixdropUrl = selector.xpath("//script//text()").get()
        movieMixdropUrl=movieMixdropUrl.replace("\n","").replace('";','').replace("\t","")
        movieMixdropUrl=movieMixdropUrl.split('href="')[1]
        if 'https://subs.warezcdn.net/' in movieMixdropUrl:
            subUrl=movieMixdropUrl.split('?sub=')[1]
            subUrl=subUrl.split('&c1_label')[0]
            movieMixdropUrl=movieMixdropUrl.split('?sub=htt')[0]
            movieMixdropUrl= movieMixdropUrl+ "***" +subUrl+ "***" + "24"

        return movieMixdropUrl

    def iframeList(self,selector,url):
        iframeList=[]
        jsonPostId=selector.xpath("//body[@class='bodyMoviePage']//div[@class='wrap']//img//@src").getall()[1]
        jsonPostId=jsonPostId.split('/')
        jsonPostId=jsonPostId[len(jsonPostId)-1]
        jsonPostId=jsonPostId.split(".")[0]
        # print("++++++",jsonPostId)
        response = requests.post(url='https://vizer.tv/includes/ajax/publicFunctions.php', data={'watchMovie': str(jsonPostId)},
                                 headers={'referer': str(url)})
        try:
            movieId=response.text
            movieId = json.loads(movieId)
            # print("++++++",movieId)
            movieId = movieId['list']
            movieIdList=[]
            if len(movieId) > 1:
                movieIdSub = movieId['0']['id']
                movieIdDub = movieId['1']['id']
                movieIdList.append(movieIdDub)
                movieIdList.append(movieIdSub)
            else:
                movieIdSub = movieId['0']['id']
                movieIdList.append(movieIdSub)

            for movie in movieIdList:
                if movie is not None:
                    movie="https://vizer.tv/embed/getPlay.php?id="+movie+"&sv=mixdrop"

                    movieMixdropUrl=self.getDubladoIframe(url=movie)

                    iframeList.append(movieMixdropUrl)
            # print("iframelist",iframeList)
            return iframeList
        except:
            print("iframe Json patladi")
    def getName(self,selector):
        try:
            name=selector.xpath("//title").get()
            name=name.split("ssistir ")[1]
            name=name.split(" Online")[0]
            return name
        except:
            return None

    def getPicture(self,selector):
        try:
            picture=selector.xpath("//body[@class='bodyMoviePage']//div[@class='wrap']//img//@src").getall()[1]
            if "https://vizer.tv/" not in picture:
                picture="https://vizer.tv/"+picture
            return picture
        except:
            return None

    def getDescription(self,selector):
        try:
            descriptionBody=""
            description=selector.xpath("//span[@class='desc ']//text()").get()

            if description is None:
                return descriptionBody
            else:
                if "\n" in description:
                    description=description.replace("\n","")
                return description
        except:
            return "....."
    def getYear(self,selector):
        try:
            year=selector.xpath("//div[@class='infos']//div[@class='year']//text()").get()
            return year
        except:
            year="2018"
            return year

    def getImdb(self,selector):
        try:
            imdbId=selector.xpath("//body[@class='bodyMoviePage']//div[@class='infos']//a[@title='imdb']//@href").get()
            imdbId=imdbId.split("/title/")[1]
            return imdbId
        except:
            return None

    def getGenreList(self,imdbId):
        baseUrl="https://www.imdb.com/title/"
        response = requests.get(url=baseUrl+imdbId)
        selector = Selector(text=response.content)

        genreList=selector.xpath("//div[@data-testid='genres']//a//span//text()").getall()
        if genreList is None or len(genreList) == 0:
            genreList=["Action"]
        return genreList


    def details(self,url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)


        print("src:",url)

        name=self.getName(selector=selector)

        if name is not None:
            if "'" in name:
                name=name.replace("'","")
            print("name:",name)

        year=self.getYear(selector=selector)
        if year is None:
            year=2018
        print("year:", year)

        imdbId=self.getImdb(selector=selector)
        print("imdbId:",imdbId)
        if imdbId is not None and name is not None:
            genreList=self.getGenreList(imdbId=imdbId)
            print("genreList:",genreList)

            picture=self.getPicture(selector=selector)
            print("picture:",picture)

            iframeList=self.iframeList(selector=selector,url=url)
            if iframeList is None:
                iframeList=[]
            for iframe in iframeList:
                if 'removed.php' in iframe:
                    iframeList.remove(iframe)
            print("iframeList",iframeList)
            description=self.getDescription(selector=selector)
            print("description:",description)
            print("************************************************************************************\n")

if __name__ == '__main__':
    # VizerTV().details(url="https://vizer.tv/filme/online/ele-e-demais")
    VizerTV().moviePages(baseUrl="https://vizer.tv/includes/ajax/ajaxPagination.php?categoriesListMovies=all&search=&page=")
