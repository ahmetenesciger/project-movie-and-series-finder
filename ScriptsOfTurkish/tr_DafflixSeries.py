import requests
from scrapy import Selector

class Dafflix:

    def start(self, baseUrl):
        urlTimer = 1
        while urlTimer < 194:
            self.pageLoop(url=baseUrl + str(urlTimer))
            urlTimer = urlTimer + 1

    def pageLoop(self, url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)
        serieList = []
        serie = selector.xpath(
            "//ul[@class='flex flex-wrap row']//li[@class='w-full']//div[@class='filter-result-box']//div[@class='filter-result-box-top flex items-start']//div[@class='filter-result-box-image flex-shrink-0']//a//@href").getall()
        for ser in serie:
            if ser is not None:
                if "https" not in ser:
                    ser = "https://www.dafflix.com/" + ser
                    serieList.append(ser)
                else:
                    serieList.append(ser)

        for serie in serieList:
            self.seriesDetails(url=serie)

    def seriesDetails(self, url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        name = selector.xpath("//div[@class='page-title w-full']//p[@itemprop='name']//@content").get()
        if ' (Türkçe Dublaj)' in name:
            name=name.replace(' (Türkçe Dublaj)','')
        if name is not None:
            if "'" in name:
                name = name.replace("'", "")
        seriesImage = selector.xpath("//div[@class='series-profile-image']//a//img//@src").get()
        seriesImage = "https://www.dafflix.com/" + str(seriesImage)

        year = selector.xpath("//span[@class='inline-block']//text()").get()
        if year is not None:
            year = year.replace(" ", "").replace("(", "").replace(")", "")
        if year is None:
            year = "2018"

        actorList = []
        actor = selector.xpath(
            "//li[@itemtype='http://schema.org/Person']//a//div[@class='series-profile-cast-info text-center sm:text-left']//h5[@itemprop='name']//text()").getall()
        if actor is not []:
            for ac in actor:
                if ac is not None:
                    actorList.append(ac)

        genreList = []

        genre = selector.xpath("//div[@class='series-profile-type tv-show-profile-type']//span//a//@title").getall()

        for gen in genre:
            genreList.append(gen)
        if len(genreList) == 0:
            genreList.append("Action")
        description = selector.xpath(
            "//div[@class='series-profile-summary article mb-5']/p[@itemprop='description']//text()").get()
        if description is not None:
            if " izle :" in description:
                description = description.split(" izle :")[1]

        seriesSeasonList = []
        seasonList = selector.xpath(
            "//div[@class='series-profile-episodes-nav relative']//ul[@class='flex md:block']//li[@itemprop='season']//a//@href").getall()
        for season in seasonList:
            if season is not None:
                if "https" not in season:
                    season = "https://www.dafflix.com/" + season
                    seriesSeasonList.append(season)
                else:
                    seriesSeasonList.append(season)

        seasonTimer = 0
        while seasonTimer < len(seriesSeasonList):
            Dafflix().getEpisode(seasonUrl=seriesSeasonList[seasonTimer], name=name, image=seriesImage, year=year,
                                 genreList=genreList,
                                 description=description, seasonNumber=seasonTimer + 1, actorList=actorList)
            seasonTimer = seasonTimer + 1

    def getEpisode(self, seasonUrl, name, image, year, genreList, description, seasonNumber, actorList):
        response = requests.get(url=seasonUrl)
        selector = Selector(text=response.content)
        episodeList = []

        episode = selector.xpath(
            "//div[@class='series-profile-episodes-area series-tab-content-active']//div[@class='series-profile-episode-list']//ul//li//div[@itemprop='episode']//a[@class='truncate']//@href").getall()
        for ep in episode:
            if ep is not None:
                if "https" not in ep:
                    ep = "https://www.dafflix.com/" + ep
                    episodeList.append(ep)
                else:
                    episodeList.append(ep)

        episodeTimer = 0
        while episodeTimer < len(episode):
            Dafflix().getIframe(episodeUrl=episodeList[episodeTimer], name=name, image=image, year=year,
                                genreList=genreList, description=description, seasonNumber=seasonNumber,
                                episodeNumber=episodeTimer + 1, actorList=actorList)
            episodeTimer = episodeTimer + 1

    def getIframe(self, episodeUrl, name, image, year, genreList, description, seasonNumber, episodeNumber, actorList):
        iframeList = []
        response = requests.get(url=episodeUrl)
        selector = Selector(text=response.content)

        iframe = selector.xpath("//button[@title='vidmoly']//@data-hhs").get()
        if iframe is not None:
            if "https:" not in iframe:
                iframe = "https:" + iframe
                iframeList.append(iframe)
            else:
                iframeList.append(iframe)

        if len(iframeList) != 0:
            print("src:", episodeUrl)
            print("name:", name)
            print("image:", image)
            print("actorList:", actorList)
            print("year:", year)
            print("genreList:", genreList)
            print("description:", description)
            print("season:", seasonNumber)
            print("episode:", episodeNumber)
            print("episode Iframe:", iframeList)
            print("**************************************************")
            print("")
            if "Sezon" not in name:
                if name is not None:
                    if "izle" in name:
                        name=name.replace("izle","")
if __name__ == '__main__':
    Dafflix().start(baseUrl="https://www.dafflix.com/kesfet/eyJ0eXBlIjoic2VyaWVzIn0=/")
