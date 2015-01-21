# -*- coding: utf8 -*-
#coding=utf-8
from scrapy import Spider, Item, Field, FormRequest
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import time
from datetime import datetime
from datetime import timedelta
import MySQLdb
import re

class Post(Item):
    title = Field()

class MyItem(Item):
    # Items are defined in a declarative style. If you attempt to store a field
    # not defined here, an exception will be raised.
    title = Field()
    content = Field()
    url = Field()

class MySpider(Spider):
    name = 'govVegetable'
    allowed_domains = ['govVegetable']

    def start_requests(self):
        Today = datetime(2015 ,1 ,6)
        requests = []

        db = MySQLdb.connect(host="localhost", user="root", passwd="bird", db="project", charset="utf8")
        cur = db.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute("SET CHARACTER_SET_CLIENT=utf8")
        cur.execute("SET CHARACTER_SET_RESULTS=utf8")

        #read all city
        cur.execute("select * from market")
        rows = cur.fetchall()
        for market in rows : 
            CurrData = datetime(2014 ,10 ,1)
            CurrData2 = datetime(2014 ,10 ,2)
            if market[1] == 'AAA' :
                rb1 = '2'
                mkno = ''
                mknoname = ''            
            else :
                rb1 = '1'
                mkno = market[1]
                mknoname = market[2]

            while ((CurrData < Today) and (CurrData2 < Today) ) :
                myy = "%03d" % int(CurrData2.year-1911)
                mmm = "%02d" % CurrData2.month
                mdd = "%02d" % CurrData2.day
                myy1 = "%03d" % int(CurrData.year-1911)
                mmm1 = "%02d" % CurrData.month
                mdd1 = "%02d" % CurrData.day
                requests += [FormRequest("http://amis.afa.gov.tw/v-asp/v201r.asp?market=%s&%s&%s" % (market[1],CurrData2.strftime("%Y%m%d"),CurrData.strftime("%Y%m%d") ),
                                           formdata={'rb2': '1','tpno' :'S', 
                                                'myy': myy , 'mmm': mmm , 'mdd': mdd,
                                                'myy1': myy1, 'mmm1': mmm1 , 'mdd1': mdd1,
                                                'mselcnt': '0', 'stb1' : '',
                                                'rb1': rb1,'mkno':mkno ,'mknoname':mknoname 
                                           },
                                           method="POST",
                                           callback=self.logged_in)]
                CurrData = CurrData + timedelta(days=2)
                CurrData2 = CurrData2 + timedelta(days=2)

        return requests

    def logged_in(self, response):


        Pere = response.url.split("?")[1]
        CurrData2 = Pere.split("&")[1]  #this
        CurrData = Pere.split("&")[2]   #pre
        marketID = Pere.split("&")[0].split("=")[1]


        sel = Selector(response)
        ListTr = sel.xpath("//table[position()= 2]/tr[position() > 2]")
        db = MySQLdb.connect(host="localhost", user="root", passwd="bird", db="project")


        cur = db.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute("SET CHARACTER_SET_CLIENT=utf8")
        cur.execute("SET CHARACTER_SET_RESULTS=utf8")

        for Tr in ListTr : 
            VegetableName = Tr.xpath("string(.//td[position() = 1])").extract()[0].replace("&nbsp","").strip()
            VegetableSubName = Tr.xpath("string(.//td[position() = 2])").extract()[0].replace("&nbsp","").strip()
            
            if not VegetableName == "" :
                #read all Class
                QueryVID = "select ID from VCategory where name = '%s' and subname = '%s'" % (VegetableName,VegetableSubName)
                cur.execute(QueryVID.encode("utf8"))
                row = cur.fetchall()
                # print len(row)
                if len(row) == 0:
                    insertVC = "insert into VCategory (name,subname) values ('%s','%s')" % \
                                (VegetableName,VegetableSubName)
                    cur.execute(insertVC.encode("utf8"))
                    db.commit()
                    VID = cur.lastrowid
                else :
                    VID = row[0][0]

                priceThis = Tr.xpath("string(.//td[position() = 3])").extract()[0].replace("&nbsp","").strip()
                pricePre = Tr.xpath("string(.//td[position() = 4])").extract()[0].replace("&nbsp","").strip()
                amountThis = Tr.xpath("string(.//td[position() = 7])").extract()[0].replace("&nbsp","").strip()
                amountPre = Tr.xpath("string(.//td[position() = 8])").extract()[0].replace("&nbsp","").strip()



                insertVThis = "insert ignore into Vegetable (VID,date,MID,amount,price) values ('%s','%s','%s','%s','%s')" %\
                            (VID,CurrData2,marketID,amountThis,priceThis)
                insertVPre = "insert ignore into Vegetable (VID,date,MID,amount,price) values ('%s','%s','%s','%s','%s')" %\
                            (VID,CurrData,marketID,amountPre,pricePre)
                # print insertVThis

                try :
                    cur.execute(insertVThis)
                    cur.execute(insertVPre)
                    db.commit()
                except :
                    print "ERROR : " +insertVThis



                # print Tr.xpath("string(./tr/td[1])").extract()
                # print Tr.xpath("string(//td[4])").extract()
                # print Tr.xpath("string(/td[position() = 3])").extract()
                # print ("start : %s " % VegetableSubName )
                # self.log("start : %s " % Tr.xpath("string(.//td[1])").extract() )
