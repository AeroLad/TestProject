import os
import configparser
from multiprocessing import Process, Pool, Manager
from functools import partial
from bs4 import BeautifulSoup
import urllib.request
import time

class GenericPage(object):
    def __init__(self):
        self.type           = "Generic"
        self.category       = "Generic"
        self.updates        = None
        self.header         = None
        self.DataFile       = None
        self.ConfigFile     = None
        self.header         = None
        self.WebPages       = None
        self.strINIFile     = None
        self.Manager        = Manager()
        self.SharedDict     = self.Manager.dict()
        self.Process        = None

    def LoadConfigFile(self):
        try:
            if(  self.strINIFile == None or
                self.strINIFile == "" or
                os.path.isfile(self.strINIFile) == False ):
                self.ConfigFile = None
                return "Invalid file"
            self.ConfigFile = configparser.ConfigParser()
            self.ConfigFile.read(self.strINIFile)
            self.type       = self.ConfigFile['Page']['type']
            self.category   = self.ConfigFile['Page']['category']
            self.url        = self.ConfigFile['Page']['url']
            self.pages      = self.ConfigFile['Page']['pages']
            self.header     = "[%s][%s]" %(self.type,self.category)
        except Exception as error:
            self.ConfigFile = None
            return "Key error: "+str(error)
        return self.ConfigFile

    def AnalysePage(self, LocalDict):
        SharedDict = LocalDict['SharedDict']
        url = LocalDict['url']
        try:
            req = urllib.request.Request(
                    url,
                    data=None,
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
            )
            result  = urllib.request.urlopen(req)
            page    = result.read().decode('utf-8')
            soup    = BeautifulSoup(page, 'lxml')
        except:
            print("Error getting page %s" %(url))
            return


    def AsyncProcess(self,SharedDict):
        ConfigFile      = SharedDict['ConfigFile']

        url         = ConfigFile['Page']['url']
        num_pages   = int(ConfigFile['Page']['pages'])
        local_processes = []
        url_list = []
        for page_num in range(1,num_pages+1):
            url_list.append( url.replace("$_PAGE_$",str(page_num)) )

        for url in url_list:
            LocalDict = {'url' : url, 'SharedDict': SharedDict}
            p = Process(target=self.AnalysePage,args=(LocalDict,))
            p.start()
            local_processes.append(p)

        for index,p in enumerate(local_processes):
            if p.is_alive():
                #print("Joining: %i" %(index))
                p.join()

        self.Email()

        return None

    def StartProcess(self):
        self.LoadConfigFile()
        if not isinstance(self.ConfigFile,configparser.ConfigParser):
            return None
        try:
            self.SharedDict['ConfigFile']       = self.ConfigFile
            p = Process(target=self.AsyncProcess, args=(self.SharedDict,))
            p.start()
            self.Process = p
            return None
        except:
            print("Error occured executing: %" %(self.strINIFile))
            return None
        return None

    def Email(self):
        print("Hello")
