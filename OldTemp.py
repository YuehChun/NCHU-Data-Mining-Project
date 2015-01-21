from scrapy import Spider, Item, Field
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import time
from datetime import datetime
from datetime import timedelta
import MySQLdb
import re



# command #scrapy runspider OldTemp.py
class Post(Item):
    title = Field()

class CWBSpider(Spider):
    name = 'CWBSpider'

    def __init__(self, name=None, **kwargs):
        self.start_urls = []
        #mysql initial
        db = MySQLdb.connect(host="localhost", user="root", passwd="bird", db="project")
        cur = db.cursor()
        #read all city
        cur.execute("select cityNumber from city")
        rows = cur.fetchall()
        # start 20131015
        Today = datetime(2015 ,1 ,6)
        for Cit in rows:
            # CurrData = datetime(2014 ,12 ,26)
            CurrData = datetime(2014 ,10 ,1)
            while (CurrData < Today) :
                self.start_urls.extend(['http://www.cwb.gov.tw/V7/climate/30day/Data/%d_%s.htm' % (Cit[0] , str(CurrData.strftime("%Y%m%d")) )])
                CurrData = CurrData + timedelta(days=1)

        super(CWBSpider, self).__init__(name, **kwargs)
    
    def parse(self, response):
        

        db = MySQLdb.connect(host="localhost", user="root", passwd="bird", db="project")
        cur = db.cursor()
        sel = Selector(response)
        try :
            TRList = sel.xpath("//table[@class='Form00' and position() = 2]/tr[position() > 1]")
            AvgTemp = float(sel.xpath("//table[@class='Form00' and position() = 3]/tr[position()= 2]/td[position() = 3]/text()").extract()[0])
            MaxTemp = float(sel.xpath("//table[@class='Form00' and position() = 3]/tr[position()= 2]/td[position() = 1]/text()").extract()[0])
            MinTemp = float(sel.xpath("//table[@class='Form00' and position() = 3]/tr[position()= 2]/td[position() = 2]/text()").extract()[0])
            hPa = 0
            Wet = 0
            WindVelocity = 0
            Rainfall = 0
            Sunshine = 0
            Ac = 0
            for TR in TRList : 
                Ac += 1
                hPa += float(TR.xpath("string(./td[position() = 2])").extract()[0])
                Wet += int(TR.xpath("string(./td[position() = 4])").extract()[0])
                WindVelocity += float(TR.xpath("string(./td[position() = 5])").extract()[0])
                if re.match("\d+.\d+",TR.xpath("string(./td[position() = 7])").extract()[0]):
                    Rainfall += float(TR.xpath("string(./td[position() = 7])").extract()[0])
                if Ac > 5 and Ac < 20 :
                    # print TR.xpath("string(./td[position() = 8])").extract()[0]
                    Sunshine += float(TR.xpath("string(./td[position() = 8])").extract()[0])

            Avg_hPa = hPa / 24
            Avg_Wet = Wet / 24
            Avg_WindVelocity = WindVelocity / 24

            rowUrl = response.url.split("/")[7].split(".")[0].split("_")
            myInsertString = "INSERT ignore INTO cur_weather (maxT,avgT,minT,pressure,humidity,speed,rainfall,sunshine,cityID,data) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                            (AvgTemp,MaxTemp,MinTemp,Avg_hPa,Avg_Wet,Avg_WindVelocity,Rainfall,Sunshine,rowUrl[0],rowUrl[1])
            cur.execute(myInsertString)
            db.commit()
            db.close()
            # print myInsertString
        except :
            print "ERROR : " +response.url
