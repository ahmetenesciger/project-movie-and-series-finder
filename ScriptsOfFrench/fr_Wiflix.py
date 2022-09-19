import requests
from scrapy import Selector
import re


class Wiflix:

    def start(self, url):
        i = 1

        while i <= 3:
            baseUrl = url + "page/" + str(i) + "/"
            response = requests.get(url=baseUrl)
            # print(response.status_code)
            if response.ok is True:
                selector = Selector(text=response.content)

                for movie in selector.xpath("//div[@class='mov clearfix']//a[@class='mov-t nowrap']"):

                    movieUrl = (movie.xpath(".//@href").getall())
                    movieName=(movie.xpath(".//text()").getall())
                    timer=0
                    while timer < len(movieUrl):

                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        if movieUrl is not None and movieName is not None:
                            self.details(url=movieUrl[timer],name=movieName[timer])
                        timer=timer+1
            print("KAÇINCI SAYFA: ", i)
            i += 1


    def parseYear(self, selector):
        try:
            year=""
            yearList = selector.xpath("//div[@class='mov-desc']//text()").getall()
            for y in yearList:
                year=year+y
            realYear = re.findall("\d\d\d\d", year)[0]
            return realYear
        except:
            return "2018"

    def parseImage(self, selector):
        try:
            image = selector.xpath("//img[@id='posterimg']//@src").get()
            image="https://wiflix.city/"+image
            return image


        except:
            return None

    def parseDescription(self, selector):
        try:
            descriptionList = selector.xpath("//div[@class='screenshots-full']//text()").getall()
            description=descriptionList[len(descriptionList)-1]
            if "'" in description or '\t' in description or "\n" in description:
                description=description.replace("'","").replace("\t","").replace("\n","")
            return description
        except:
            return "......."

    def parseGenre(self, selector):
        genreList = []
        try:
            genre=selector.xpath("//span[@itemprop='genre']//a//text()").getall()
            for gen in genre:
                if 'Exclue' not in gen and 'Film' not in gen:
                    genreList.append(gen)
            return genreList
        except:
            genreList.append('Action')
            return genreList

    def parseIframeList(self, selector):
        sourceList = []
        try:
            movieList=selector.xpath("//div[@class='tabs-sel linkstab']//a//@href").getall()
            for movie in movieList:
                if 'uqload' in movie:
                    if 'php?u=' in movie:
                        movie=movie.replace('/vd.php?u=','')
                        sourceList.append(movie)
                    else:
                        sourceList.append(movie)

            return sourceList
        except:
            return sourceList
    def details(self, url , name):
        response = requests.get(url=url)
        selector = Selector(text=response.content)

        print("src:",url)
        if "'" in name:
            name=name.replace("'","")
        print("name:",name)
        image = self.parseImage(selector=selector)
        print("image:",image)
        year = self.parseYear(selector=selector)
        print("year:",year)
        genre = self.parseGenre(selector=selector)
        print("genre:",genre)

        iframeList = self.parseIframeList(selector=selector)

        print("iframeList:",iframeList)

        description = self.parseDescription(selector=selector)
        print("description:", description)

if __name__ == '__main__':
    Wiflix().start(url="https://wiflix.city/film-en-streaming/")
