import multiprocessing
import threading
from bs4 import BeautifulSoup
import urllib.request

class GenericPage(multiprocessing.Process):

    def __init__(self, objConfigFile):
        super().__init__()
        self.objConfigFile  = objConfigFile
        self.strHeader      = "[%s][%s]" %(objConfigFile['Page']['type'],objConfigFile['Page']['category'])
        self.dictNew        = {}

        self.start()

    def fnGetPage(self,strUrl):
        req = urllib.request.Request(
                strUrl,
                data=None,
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
        )
        result  = urllib.request.urlopen(req)
        page    = result.read().decode('utf-8')
        return page

    def fnProcessPage(self,page):
        soup = BeautifulSoup(page,'lxml')

    def fnProcessUrl(self, strUrl):
        page    = self.fnGetPage(strUrl)
        self.fnProcessPage(page)
        return None

    def fnPostProcess(self):
        fDataFile = ""

    def run(self):
        strUrl      = self.objConfigFile['Page']['url']
        intNumPages = int(self.objConfigFile['Page']['pages'])

        arrUrls     = []

        for intPageNum in range(1,intNumPages+1):
            arrUrls.append( strUrl.replace("$_PAGE_$",str(intPageNum)))

        arrThreads  = []
        for strUrl in arrUrls:
            thrObj = threading.Thread(target=self.fnProcessUrl, args=(strUrl,))
            thrObj.setDaemon(True)
            arrThreads.append(thrObj)
            thrObj.start()
        for thrObj in arrThreads:
            if thrObj.is_alive():
                thrObj.join()

        self.fnPostProcess()

        self.Email()

        return None

    def Email(self):
        print("Sending email")
