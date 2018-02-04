from bs4 import BeautifulSoup
import urllib.request
import time
from multiprocessing import Process, Manager

def fnGumtreeAd(i,shared_list):
    url = "https://www.gumtree.com.au/s-laptops/melbourne/page-"+str(i)+"/c18553l3001317"
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    result = urllib.request.urlopen(req)
    page = result.read().decode('utf-8')

    soup = BeautifulSoup(page, "lxml")

    ads = soup.findAll('a', {"class": "user-ad-row link link--base-color-inherit link--hover-color-none link--no-underline"})

    for ad in ads:
        link = "https://www.gumtree.com.au"+ad.attrs['href']
        title = ad.find("p"     , {"class":"user-ad-row__title"}).string
        try:
            price = ad.find("span"  , {"class":"user-ad-price__price"}).string
        except:
            price = 1000.0
        try:
            desc  = ad.find("p"     , {"class":"user-ad-row__description"}).string
        except:
            desc = ""

        title = str(title)
        price = str(price)
        price = price.replace(",","")
        price = float(price[1:])
        desc  = str(desc.lower())

        #if False:
        if price <= 50.0:
            #print(title)
            #print("\tPrice:\t"+str(price))
            #print("\tLink:\t"+str(link))
            #print()
            shared_list.append(title)

        print("Page:\t"+str(i)+" processed")
        return None

if __name__ == '__main__':
    manager = Manager()
    shared_list = manager.list()
    processes = []
    for i in range(1,50):
        p = Process(target=fnGumtreeAd, args=(i,shared_list))
        p.start()
        processes.append(p)

    bExit = False
    while bExit != True:
        termCounter = 0
        for process in processes:
            if process.is_alive() == False:
                termCounter += 1
        if termCounter == len(processes):
            bExit = True
        time.sleep(1)

    print(shared_list)
