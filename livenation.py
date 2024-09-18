import requests
import urllib.parse
import json
import time
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime

livenation_link = []
bad_link = []
ticketmaster_link = []
all_url = []

# ticketmaster ca
def filter_url_ticketmaster_ca(target_url):
    retries = 3

    for i in range(retries):
        try:
            targetUrl = urllib.parse.quote(target_url)
            url = f"http://api.scrape.do?token=4452cbd7342d4a36971719b194897d692073b3c06af&url={targetUrl}&super=true&render=true&geoCode=us"

            response = requests.request("GET", url )

            soup = BeautifulSoup(response.text, 'html.parser')

            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if script_tag != None:

                data = json.loads(script_tag.text)
            
                try:
                    if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                        print("ok")
                        try :
                            generalinfo = data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["generalInfo"]["linkText"]
                        except :
                            generalinfo = "key error"

                        current_date = datetime.now().date()
                        target_date = datetime.strptime(data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["epDate"], '%Y-%m-%d').date()

                        if current_date < target_date and generalinfo != "":
                            ticketmaster_link.append(target_url)
                            return "success_value"
                                
                    else:   
                        return "No Value"
                except:
                    return "No link"
            else:
                bad_link.append(target_url)
                return "bad status"
                

        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                time.sleep(10)
            else:
                pass


# ticketmaster
def filter_url_ticketmaster(target_url):
    retries = 3

    for i in range(retries):
        try:
            url = f"http://api.scrape.do/?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&url={target_url}"

            response = requests.request("GET", url )

            soup = BeautifulSoup(response.text, 'html.parser')

            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if script_tag != None:

                data = json.loads(script_tag.text)
            
                try:
                    if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                        print("ok")
                        try :
                            generalinfo = data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["generalInfo"]["linkText"]
                        except :
                            
                            generalinfo = "key error"

                        current_date = datetime.now().date()
                        target_date = datetime.strptime(data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["epDate"], '%Y-%m-%d').date()

                        if current_date < target_date and generalinfo != "":
                            type_event = "coming event"
                            ticketmaster_link.append(target_url)
                                
                    else:
                        return "No Value"
                except:
                    return "No link"
            else:
                bad_link.append(target_url)
                return "bad status"
            
        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                time.sleep(10)
            else:
                pass

#  livenation
def filter_url_livenation(targetUrl, max_retries=5, delay=2):

    for attempt in range(max_retries):
        # target_Url = urllib.parse.quote(targetUrl)
        try:
            url = f"https://api.scrape.do/?token=4452cbd7342d4a36971719b194897d692073b3c06af&url={targetUrl}&super=true&render=true"

            response = requests.request("GET", url )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if script_tag != None:
                    data = json.loads(script_tag.text)
                
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            print("ok")
                            livenation_link.append(targetUrl)
                            return data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"]
                    except:
                        return "No Value"
                              
                else:
                    return "No link"

            else:
                bad_link.append(targetUrl)
                return "bad status"
                
        except requests.exceptions.ConnectionError:
            print(f"server error {attempt + 1}")
            if attempt < 5 :
                time.sleep(delay)
            else:
                pass


def request(livenation_url):
    retries = 3
    for i in range(retries):
        try:
            
            token = "4452cbd7342d4a36971719b194897d692073b3c06af"
            url = "http://api.scrape.do?token={}&url={}".format(token, livenation_url)
            response = requests.request("GET", url)
            print(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return  {"soup":soup,"url":url}
        
        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                time.sleep(10)
            else:
                pass

soup = request("https://www.livenation.com/artist-sitemap")
soup = soup["soup"]
links = soup.select('div.css-p1b7dg > a')
for link in links:

    soup = request("https://www.livenation.com"+link["href"])
    current_url = soup["url"].replace("http://api.scrape.do?token=4452cbd7342d4a36971719b194897d692073b3c06af&url=","")
    soup = soup["soup"]
    try:
        pagination = int(soup.select_one('a[aria-label="Last Page"]').text)
    except:
        pagination = 2


    for page in range(1,pagination+1):
     
        print(page)
        if page == 1:
            soup = request(current_url)
        if page > 1 :
     
            soup = request(current_url+ f"?pg={page}")
       
        soup = soup["soup"]
        
        artist_link = soup.select('.chakra-link.css-1okgivo')
        for link in artist_link:

            soup = request('https://www.livenation.com' + link["href"])
            soup = soup["soup"]
            target_link = soup.select('ul.css-p47pw5 a.chakra-linkbox__overlay.css-1q2nroc')
            
            if target_link:
                for link in target_link:

                    link = link["href"]
                    print(link)
                    
                    if "ticketmaster.com" in link and "ticketmaster.com." not in link:
                        data = filter_url_ticketmaster(link)

                    elif "concerts.livenation.com" in link:
                        data = filter_url_livenation(link)

                    elif "ticketmaster.ca" in link:
                        data = filter_url_ticketmaster_ca(link)

                    else:
                        bad_link.append(link)
                    
                    all_url.append(link)
                    print(data)
                    print(f"bad_url = {len(bad_link)} and livenation_concert  = {len(livenation_link)} and ticketmaster = {len(ticketmaster_link)}")



with open("ticketmaster_link.json", "w") as files:
    json.dump(ticketmaster_link,files)

with open("livenation_link.json", "w") as files:
    json.dump(livenation_link,files)

with open("bad_link.json", "w") as files:
    json.dump(bad_link,files)

with open("livenation_all_link.json", "w") as files:
    json.dump(all_url,files)

        
