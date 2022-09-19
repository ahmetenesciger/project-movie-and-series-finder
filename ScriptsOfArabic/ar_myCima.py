import requests
from scrapy import Selector

class MyCima:

    def start(self, url):
        i = 1

        while i <= 290:
            baseUrl = url + "page/" + str(i) + "/"
            response = requests.get(url=baseUrl)
            if response.ok is True:
                selector = Selector(text=response.content)
                for movie in selector.xpath("//div[@class='Grid--MycimaPosts']//div[@class='GridItem']"):
                    movieUrl = (movie.xpath(".//a//@href").get())
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    self.details(url=movieUrl)
                print("SAYFA: ", i)
                i += 1

    def iframe(self, selector):
        sourceList = []
        try:
            iframeList = selector.xpath("//ul[@class='WatchServersList']//btn//@data-url").getall()
            for iframe in iframeList:
                if "ok.ru" in iframe or "uqload" in iframe:
                    iframe = iframe.replace("https://www.ok.ru/", "https://m.ok.ru/").replace("videoembed", "video")
                    if "&Expires" in iframe or "\r" in iframe:
                        iframe=iframe.replace("\r","")
                        iframe=iframe.split("&Expires")[0]
                        if not iframe.endswith(".jpg"):
                            if not iframe.startswith("https:"):
                                sourceList.append("https:" + iframe)
                            else:
                                sourceList.append(iframe)
            return sourceList
        except:
            return sourceList

    def name(self, selector):
        try:
            name = selector.xpath("//div[@class='Title--Content--Single-begin']//h1//text()").get()
            name = name.replace("\n","")
            if name.endswith("("):
                name = name.split("(")[0]

            return name
        except:
            return None

    def year(self, selector):
        try:
            year = selector.xpath("//div[@class='Title--Content--Single-begin']//a//text()").get()
            return year
        except:
            return "2018"

    def picture(self, selector):
        try:
            picture = selector.xpath("//meta[@itemprop='thumbnailUrl']//@content").get()
            return picture
        except:
            return None

    def genre(self, selector):
        genreList = []
        if 0==len(genreList):
            genreList.append("Drama")
            genreList.append("Action")
        return genreList

    def description(self, selector):
        try:
            description = selector.xpath("//div[@class='StoryMovieContent']//text()").get()
            if description is not None:
                if "\n" in description:
                    description.replace("\n","")
            else:
                description=""
            return description
        except:
            return "........"

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def details(self, url):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        print("url :",url)

        name = self.name(selector=selector)
        print("Name: ", name)

        year = self.year(selector=selector)
        print("Year: ", year)

        picture = self.picture(selector=selector)
        print("Picture: ", picture)

        genreList = self.genre(selector=selector)
        print("Genre: ", genreList)

        description = self.description(selector=selector)
        print("Description: ", description)

        iframeList = self.iframe(selector=selector)
        print("Iframe List: ", iframeList)


if __name__ == '__main__':
    MyCima().start(url="https://mycima.world/movies/")
