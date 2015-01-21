import scrapy
import json



class LoginSpider(scrapy.Spider):
    name = 'google.com'
    start_urls = ['https://www.google.com.tw/?gws_rd=ssl']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'q': 'python'},
            callback=self.after_login
        )


    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        else:
            print "right"
        # continue scraping with authenticated session...

    # def start_requests(self):
    #         payload = {"a": 1, "b": 2}
    #         yield Request(url, self.parse_data, method="POST", body=urllib.urlencode(payload))

    # def parse_data(self, response):
    #     # do stuff with data...
    #     data = json.loads(response.body)

# help(LoginSpider)
LS = LoginSpider()
LS.parse("http://www.google.com.tw")

