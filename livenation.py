import requests
import urllib.parse
import json
import time
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
bad_link = []
livenation_link = []
ticketmaster_link = []
all_url = []

def convert_json(fine_name, link):
    try:
        with open(f'{fine_name}', 'r') as file:
            data_list = json.load(file)
        
        data_list.append(link)
        # JSON string se read karna
        with open(f'{fine_name}', 'w') as file:
            json.dump(data_list, file)
    except:
        with open('/home/ubuntu/livenation_ticketmaster/'+f'{fine_name}', 'r') as file:
            data_list = json.load(file)
        data_list.append(link)
        # JSON string se read karna
        with open('/home/ubuntu/livenation_ticketmaster/'+f'{fine_name}', 'w') as file:
            json.dump(data_list, file)

# ticketmaster ca
def filter_url_ticketmaster_ca(target_url):
    retries = 3

    for i in range(retries):
        try:
            targetUrl = urllib.parse.quote(target_url)
            url = f"http://api.scrape.do?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&geoCode=us&url={targetUrl}"
            response = requests.request("GET", url )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if script_tag != None:
                    try:
                        data = json.loads(script_tag.text)
                    except:
                        data = {}
                        
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            try :
                                generalinfo = data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["generalInfo"]["linkText"]
                            except :
                                generalinfo = "key error"

                            current_date = datetime.now().date()
                            target_date = datetime.strptime(data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["epDate"], '%Y-%m-%d').date()

                            if current_date < target_date and generalinfo != "":
                                ticketmaster_link.append(target_url)
                                convert_json('ticketmaster_link.json', target_url)
                                return "success_value"
                                    
                    except:
                        return "No Value"
                else: 
                    return "no link"
            else:       
                if i < retries - 1:  # Don't retry on the last attempt
                    print(f"attempt {i + 1}")
                    time.sleep(10)
                else:
                    pass  
        
        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                print(f"attempt {i + 1}")
                time.sleep(10)
            else:
                pass

# ticketmaster
def filter_url_ticketmaster(target_url):
    retries = 3

    for i in range(retries):
        try:
            url = f"http://api.scrape.do/?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&geoCode=us&url={target_url}"
            response = requests.request("GET", url )
            if response.status_code == 200: 
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            
                if script_tag != None:
                    try:
                        data = json.loads(script_tag.text)
                    except:
                        data = {}
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            try :
                                generalinfo = data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["generalInfo"]["linkText"]
                            except :
                                generalinfo = "key error"

                            current_date = datetime.now().date()
                            target_date = datetime.strptime(data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["epDate"], '%Y-%m-%d').date()

                            if current_date < target_date and generalinfo != "":
                                type_event = "coming event"
                                ticketmaster_link.append(target_url)
                                convert_json('ticketmaster_link.json', target_url)

                    except:
                        return "No link"
                else:
                    return "No link"
            else:
                if i < retries - 1:  # Don't retry on the last attempt
                    print(f"attempt {i + 1}")
                    time.sleep(10)
                else:
                    pass


        except requests.exceptions.ConnectionError:
            if i < retries - 1:  # Don't retry on the last attempt
                print(f"attempt {i + 1}")
                time.sleep(10)
            else:
                pass

#  livenation
def filter_url_livenation(targetUrl, max_retries=5, delay=10):

    for attempt in range(max_retries):
        # target_Url = urllib.parse.quote(targetUrl)
        try:
            url = f"https://api.scrape.do/?token=4452cbd7342d4a36971719b194897d692073b3c06af&super=true&render=true&geoCode=us&url={targetUrl}"
            response = requests.request("GET", url )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if script_tag != None:
                    try:
                        data = json.loads(script_tag.text)
                    except:
                        data = {}
                    try:
                        if data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"] == "Face Value Ticket Exchange":
                            livenation_link.append(target_url)
                            convert_json('livenation_link.json', target_url)
                            return data["props"]["pageProps"]["edpData"]["context"]["discoveryEvent"]["edpPopup"]["linkText"]
                    except:
                        return "No Value"           
                else:
                    return "No link"
            else:
                print(f"attempt {attempt + 1}")
                if attempt < 5 :
                    time.sleep(delay)
                else:
                    pass
                
        except requests.exceptions.ConnectionError:
            print(f"attempt {attempt + 1}")
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
        print(current_url)
        print(f"pagination {page}")
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
                    if "ticketmaster.com" in link and "ticketmaster.com." not in link:
                        data = filter_url_ticketmaster(link)
                    elif "concerts.livenation.com" in link:
                        data = filter_url_livenation(link)
                    elif "ticketmaster.ca" in link:
                        data = filter_url_ticketmaster_ca(link)
                    else:
                        bad_link.append(link)
                        convert_json('bad_link.json', link)
                    all_url.append(link)
                    convert_json('all_link.json', link)
                    print(f"bad_url = {len(bad_link)} and livenation_concert  = {len(livenation_link)} and ticketmaster = {len(ticketmaster_link)} and all_website_link.json ={len(all_url)}")



        
