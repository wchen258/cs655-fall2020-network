import random
import string
import time

import scrapy

class geni(scrapy.Spider):
    name = 'geni'

    def start_requests(self):
        self.ip = getattr(self, 'ip', 'localhost')
        self.n = int(getattr(self, 'n', '10'))
        self.reponse_time = []
        with open('../dog.jpg', 'rb') as f:
            img = f.read()
        url = f'http://{self.ip}/Servlet/servlet'
        boundary = '1359649442142754333936781725'
        self.body = b'--' + boundary.encode('ascii') + b'\r\n' +\
            b'Content-Disposition: form-data; name="image"; filename="dog.jpg"\r\n' +\
            b'Content-Type: image/jpeg\r\n\r\n' +\
            img +\
            b'\r\n--' + boundary.encode('ascii') + b'--\r\n'
        self.headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}'}
        for i in range(self.n):
            yield scrapy.Request(url=url, callback=self.parse, method='POST', body=self.body, headers=self.headers, dont_filter=True, meta={'start': time.time()})

    def parse(self, response: scrapy.http.Response):
        self.reponse_time.append(time.time()-response.meta['start'])
        self.logger.debug(response.text)

    def closed(self, reason):
        with open(f'result_{self.ip}_{self.settings.get("CONCURRENT_REQUESTS")}', 'w') as f:
            for t in self.reponse_time:
                f.write(str(t) + '\n')
