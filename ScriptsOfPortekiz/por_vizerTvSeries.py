import requests
import json
from scrapy import Selector


class VizerTvSeries:

    def seriePages(self, baseUrl):
        i = 73
        while (i >= 0):
            url = baseUrl + str(
                i) + "&saga=0&categoryFilterYearMin=1950&categoryFilterYearMax=2022&categoryFilterOrderBy=vzViews&categoryFilterOrderWay=desc"
            serieIdList = []
            # response = requests.get(url=url)
            response = requests.post(
                url=url,
                data={'page': i, 'saga': '0', 'categoryFilterOrderBy': 'vzViews', 'categoryFilterOrderWay': 'desc'},
                headers={'referer': 'https://vizer.tv/series/online'})

            idList = response.text
            idList = idList.split('"list":')[1]
            idList = idList.split('","title":"')
            for id in idList:
                if ':{"url":"' in id:
                    id = id.split('{"url":"')[1]
                    id = "https://vizer.tv/serie/online/" + id
                    serieIdList.append(id)

            for serieId in serieIdList:
                self.getSeries(url=serieId)

            print("sayfa sayisi:", i)
            i = i - 1

    def getSeries(self, url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        print("**************************************")

        imdbId = self.getImdb(selector=selector)
        print("imdb check",imdbId)

        if imdbId is not None:

            name = self.getName(imdbId=imdbId)
            year = self.getYear(selector=selector)
            genreList = self.getGenreList(imdbId=imdbId)
            picture = self.getPicture(imdbId=imdbId)
            description = self.getDescription(selector=selector)
            seriesSeasonSize = self.seriesSeasonSize(selector=selector)

            if name is not None and picture is not None and seriesSeasonSize is not None:
                self.getSeason(selector=selector, url=url, seriesSeasonSize=seriesSeasonSize, imdbId=imdbId, name=name,
                               picture=picture, year=year, genreList=genreList, description=description)

    def getImdb(self, selector):
        try:
            imdbId = selector.xpath(
                "//body[@class='bodyMoviePage bodySeriePage']//div[@class='infos']//a[@title='imdb']//@href").get()
            imdbId = imdbId.split("/title/")[1]
            return imdbId
        except:
            return None

    def getName(self, imdbId):
        try:
            selector = self.getImdbUrl(imdbId=imdbId)
            name = selector.xpath("//h1[@data-testid='hero-title-block__title']//text()").get()
            name=name.replace("'","").replace("\n","").replace("\t","")
            return name
        except:
            return None

    def getPicture(self, imdbId):
        try:
            selector = self.getImdbUrl(imdbId=imdbId)
            picture = selector.xpath("//meta[@property='og:image']//@content").get()
            return picture
        except:
            return None

    def getDescription(self, selector):
        try:
            description = selector.xpath("//span[@class='desc ']//text()").get()
            if "\n" in description:
                description = description.replace("\n", "").replace("\t","")
            return description
        except:
            return ".............."

    def getYear(self, selector):
        try:
            year = selector.xpath("//div[@class='infos']//div[@class='year']//text()").get()
            return year
        except:
            return "2018"

    def getImdbUrl(self, imdbId):
        baseUrl = "https://www.imdb.com/title/"
        imdbUrl = baseUrl + imdbId
        response = requests.get(url=imdbUrl)
        selector = Selector(text=response.content)
        return selector

    def getGenreList(self, imdbId):
        genreList=[]
        try:
            selector = self.getImdbUrl(imdbId=imdbId)
            genre = selector.xpath("//div[@data-testid='genres']//a//span//text()").getall()
            for gen in genre:
                genreList.append(gen)
            return genreList
        except:
            genreList.append("Action")
            return genreList

    def seriesSeasonSize(self, selector):
        try:
            seriesSize = selector.xpath("//div[@class='list bslider']//div[@class='item ']//@data-season-id").getall()
            return len(seriesSize)
        except:
            return None

    def getSeason(self, selector, url, seriesSeasonSize, imdbId, name, picture, year, genreList, description):
        jsonPostId = selector.xpath("//div[@class='list bslider']//div[@class='item ']//@data-season-id").getall()
        if jsonPostId is not None:
            jsonTimer = 0
            while jsonTimer < seriesSeasonSize:
                season = jsonTimer + 1
                self.getEpisodes(url=url, seasonId=jsonPostId[jsonTimer], season=season, imdbId=imdbId, name=name,
                                 picture=picture, year=year, genreList=genreList, description=description)
                jsonTimer = jsonTimer + 1

    def getEpisodes(self, url, seasonId, season, imdbId, name, picture, year, genreList, description):
        response = requests.post(url='https://vizer.tv/includes/ajax/publicFunctions.php',
                                 data={'getEpisodes': str(seasonId)}, headers={'referer': str(url),
                                                                               'cookie': "_ga=GA1.2.1590078998.1635254041; PHPSESSID=6dl5np3m2ebnnb32807ou901kf; _gid=GA1.2.1595985812.1636919604; _gat=1"})
        if response is not None:
            try:
                responseJson = json.loads(response.text)
                episodeTimer = 0
                if "list" in responseJson:
                    while episodeTimer < len(responseJson["list"]):
                        # print(responseJson["list"][str(episodeTimer)]["id"])
                        episodeId = responseJson["list"][str(episodeTimer)]["id"]
                        episodeIframeId=None
                        if episodeId is not None:
                            responseEpisodeId = requests.post(url='https://vizer.tv/includes/ajax/publicFunctions.php',
                                                              data={'getEpisodeLanguages': str(episodeId)},
                                                              headers={'referer': str(url),
                                                                       'cookie': "_ga=GA1.2.1590078998.1635254041; PHPSESSID=6dl5np3m2ebnnb32807ou901kf; _gid=GA1.2.1874722286.1637441422; _gat=1"})
                            episode = episodeTimer + 1
                            episodeIframeId = json.loads(responseEpisodeId.text)
                        if episodeIframeId is not None:
                            self.getEpisodeIframe(url=url, episodeJson=episodeIframeId, season=season, episode=episode,
                                                  imdbId=imdbId,
                                                  name=name, picture=picture, year=year, genreList=genreList,
                                                  description=description)
                            # print(episodeIframeId["list"])
                        episodeTimer = episodeTimer + 1
            except:
                print("json donusturme islemi patladi")
                return



    def getEpisodeIframe(self, url, episodeJson, season, episode, imdbId, name, picture, year, genreList, description):
        episodeTimer = 0
        try:
            if "list" in episodeJson:
                seriesIframeList = []
                while episodeTimer < len(episodeJson["list"]):
                    # print(episodeJson["list"][str(episodeTimer)])
                    episodeIframeType = episodeJson["list"][str(episodeTimer)]
                    # print("episodeIframeType",episodeIframeType)
                    if episodeIframeType["lang"] == '1':
                        seriesIframeUrl = "https://vizer.tv/embed/getPlay.php?id=" + episodeIframeType[
                            'id'] + "&sv=mixdrop"
                        response = requests.get(url=seriesIframeUrl)
                        selector = Selector(text=response.content)
                        seriesMixdropUrl = selector.xpath("//script//text()").get()


                        if seriesMixdropUrl is not None:
                            seriesMixdropUrl = seriesMixdropUrl.replace("\n", "").replace("\t", "")
                        if '";' in seriesMixdropUrl:
                            seriesMixdropUrl = seriesMixdropUrl.replace('";', '')
                        seriesMixdropUrl = seriesMixdropUrl.split('href="')[1]
                        if 'https://subs.warezcdn.net/' in seriesMixdropUrl:
                            subUrl = seriesMixdropUrl.split('?sub=')[1]
                            subUrl = subUrl.split('&c1_label')[0]
                            seriesMixdropUrl = seriesMixdropUrl.split('?sub=htt')[0]
                            seriesMixdropUrl = seriesMixdropUrl + "***" + subUrl + "***" + "24"

                        seriesIframeList.append(str(seriesMixdropUrl))
                    if episodeIframeType["lang"] == '2':
                        seriesIframeUrl = "https://vizer.tv/embed/getPlay.php?id=" + episodeIframeType['id'] + "&sv=mixdrop"
                        response = requests.get(url=seriesIframeUrl)
                        selector = Selector(text=response.content)
                        seriesMixdropUrl = selector.xpath("//script//text()").get()
                        if "\n" in seriesMixdropUrl:
                           seriesMixdropUrl = seriesMixdropUrl.replace("\n", "").replace("\t","")
                        if '";' in seriesMixdropUrl:
                           seriesMixdropUrl = seriesMixdropUrl.replace('";', '')
                        seriesMixdropUrl = seriesMixdropUrl.split('href="')[1]

                        if 'https://subs.warezcdn.net/' in seriesMixdropUrl:
                            subUrl = seriesMixdropUrl.split('?sub=')[1]
                            subUrl = subUrl.split('&c1_label')[0]
                            seriesMixdropUrl = seriesMixdropUrl.split('?sub=htt')[0]
                            seriesMixdropUrl = seriesMixdropUrl + "***" + subUrl + "***" + "24"

                        seriesIframeList.append(str(seriesMixdropUrl))
                    episodeTimer = episodeTimer + 1
                print("imdbId:", imdbId)
                print("src:", url)
                print("name:", name)
                print("picture:", picture)
                print("year:", year)
                print("genreList:", genreList)
                print("description:", description)
                print("season:", season)
                print("episode:", episode)
                print("iframeList:", seriesIframeList)
                imdbUrl="https://www.imdb.com/title/"+imdbId+"/"
                print("imdbUrl:",imdbUrl)
                print("+++++++++++++++++++++++++++++++++")



        except Exception as e:
            print("Json patladi", e)



if __name__ == '__main__':
     # VizerTvSeries().getSeries(url="https://vizer.tv/serie/online/normal-people")
     VizerTvSeries().seriePages(
          baseUrl="https://vizer.tv/includes/ajax/ajaxPagination.php?categoriesListSeries=all&anime=0&search=&page=")
