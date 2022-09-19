import requests
import json
from scrapy import Selector


class Filmmodu():
    def start(self, pageUrl, filmmoduDomain, year):
        i = 1
        while (i<20):
            print(i)
            newPageUrl = pageUrl + str(i) + "&publish_year=" + year + "&quality="
            response = requests.get(url=newPageUrl)
            selector = Selector(text=response.content)
            mList = selector.xpath(
                "//div[@class='row movie-list']//div[@class='col-md-3 col-xs-6 movie']//div[@class='poster']//a//@href").getall()
            if len(mList) == 0:
                break
            for m in mList:
                self.details(url=m, filmmoduDomain=filmmoduDomain)
            i += 1

    def getName(self, selector):
        name = None
        try:
            name = selector.xpath(
                "//div[@class='col-md-7 col-xs-12 titles']//h1[@itemprop='name']//@title").get()
            return name
        except:
            return name

    def getOriginalName(self, selector):
        originalName = None
        try:
            originalName = selector.xpath(
                "//div[@class='col-md-7 col-xs-12 titles']//h2[@itemprop='alternateName']//@title").get()
            return originalName
        except:
            return originalName

    def getYear(self, selector):
        year = "2018"
        try:
            year = selector.xpath("//span[@itemprop='dateCreated']//text()").get()
            return year
        except:
            return year

    def getDirector(self, selector):
        directors = []
        try:
            directors = selector.xpath("//a[@itemprop='director']//span[@itemprop='name']//text()").getall()
            return directors
        except:
            return directors

    def getActor(self, selector):
        actors = []
        try:
            actors = selector.xpath("//a[@itemprop='actor']//span[@itemprop='name']//text()").getall()
            # print(actors)
            return actors
        except:
            return actors

    def getDescription(self, selector):
        description = "......."
        try:
            description = selector.xpath("//meta[@property='og:description']//@content").get()
            return description
        except:
            return description

    def getPicture(self, selector, filmmoduDomain):
        picture = None
        try:
            picture = selector.xpath("//img[@itemprop='image']//@src").get()
            picture = filmmoduDomain + picture
            return picture
        except:
            return picture

    def getGenre(self, selector):
        genres = []
        try:
            listGen = selector.xpath("//p//a//@href").getall()
            for genre in listGen:
                if 'tur/' in genre:
                    genre = genre.split("tur/")[1]
                    if '-' in genre:
                        genre = genre.split('-')[0]
                        genres.append(genre)
                    else:
                        genres.append(genre)
            return genres
        except:
            return genres

    def getFragman(self, selector):
        fragman = None
        try:
            fragman = selector.xpath("//div[@class='embed-responsive embed-responsive-16by9']//iframe//@src").get()
            return fragman
        except:
            return fragman

    def getUrlList(self, selector):
        movieUrlList = []
        try:
            urlList = selector.xpath(
                "//div[@class='btn-group']//a[@class='btn btn-white dropdown-toggle']//@href").getall()
            for url in urlList:
                movieUrlList.append(url)
            return movieUrlList
        except:
            return movieUrlList

    def getMovieId(self, picture):
        movieId = None
        try:
            movieId = picture.split("poster/")[1]
            movieId = movieId.split("/")[0]
            return movieId
        except:
            return movieId

    def getIframeList(self, urlList, movieId, filmmoduDomain):
        # print(urlList,movieId)
        iframeList = []
        try:
            for url in urlList:
                if 'altyazili' in url:
                    # print("sub",url)
                    urlJsonInfoSub = filmmoduDomain + '/get-source?movie_id=' + movieId + '&type=en'
                    responseSub = requests.get(url=urlJsonInfoSub)
                    responseSub = responseSub.text
                    responseSub = json.loads(responseSub)
                    subtitleUrl = filmmoduDomain + responseSub['subtitle']
                    m3u8ListSub = responseSub['sources']
                    for m3u8 in m3u8ListSub:
                        ifrm = m3u8['src']
                        # ifrm=str(ifrm)
                        iframeList.append(ifrm + "***" + subtitleUrl + "***" + "14")

                if 'dublaj' in url:
                    # print("dub",url)
                    urlJsonInfoDub = filmmoduDomain + '/get-source?movie_id=' + movieId + '&type=tr'
                    responseDub = requests.get(url=urlJsonInfoDub)
                    responseDub = responseDub.text
                    responseDub = json.loads(responseDub)
                    m3u8ListDub = responseDub['sources']
                    for m3u8 in m3u8ListDub:
                        ifrmD = m3u8['src']
                        # ifrmD=str(ifrmD)
                        # print(ifrmD)
                        iframeList.append(ifrmD)
            return iframeList
        except:
            return iframeList

    def getImdbId(self, iframe):
        imdbId = None
        try:
            imdbId = iframe.split("/tt")[1]
            imdbId = imdbId.split(".")[0]
            imdbId = "tt" + imdbId
            return imdbId
        except:
            return imdbId

    def details(self, url, filmmoduDomain):
        response = requests.get(url=url)
        selector = Selector(text=response.content)
        # filmmoduDomain = "https://www.filmmodu3.com"
        name = self.getName(selector=selector)
        originalName = self.getOriginalName(selector=selector)
        if originalName is None:
            originalName = name
        year = self.getYear(selector=selector)
        directors = self.getDirector(selector=selector)
        actors = self.getActor(selector=selector)
        description = self.getDescription(selector=selector)
        picture = self.getPicture(selector=selector, filmmoduDomain=filmmoduDomain)
        genre = self.getGenre(selector=selector)
        fragman = self.getFragman(selector=selector)
        urlList = self.getUrlList(selector=selector)
        movieId = self.getMovieId(picture=picture)
        if movieId is not None and len(urlList) != 0:
            iframeList = self.getIframeList(urlList=urlList, movieId=movieId, filmmoduDomain=filmmoduDomain)
            imdbId = self.getImdbId(iframe=iframeList[0])
            print("src:", url)
            print("name:", name)
            print("org Name:", originalName)
            print("picture:", picture)
            print("genre:", genre)
            print("year:", year)
            print("directors:", directors)
            print("actors:", actors)
            print("description:", description)
            print("fragman:", fragman)
            print("urlList:", urlList)
            print("movieId:", movieId)
            print("iframeList:", iframeList)
            print("imdbId:", imdbId)
            print("*****************************************************\n")


if __name__ == '__main__':
    filmmoduDomain = "https://www.filmmodu8.com"
    year = "2022"
    Filmmodu().details(url=filmmoduDomain + "/breaking-news-in-yuba-county-izle", filmmoduDomain=filmmoduDomain)
    Filmmodu().start(pageUrl=filmmoduDomain + "/filmler?genre=&imdb=&language=&order=created_at&page=",
                     filmmoduDomain=filmmoduDomain, year=year)
