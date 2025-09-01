import requests
from bs4 import BeautifulSoup
import subprocess
from random import choice
from os import path
import sys
from colorama import Fore, Back, init
from urllib.parse import urljoin, urlparse

all_reqs_history = {
    # ID : Request
}

req_id = 1

def random_useragent():
    file_path = './wordlist/user-agents.txt'
    if path.exists(file_path):
        useragent_list = open(file_path, "r").read().splitlines()
        useragent_list.close()
        return choice( useragent_list )
    else:
        print(f"ERROR: '{file_path}' path not found")

req_headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=1000",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:30.0) Gecko/20100101 Firefox/33.0",
    }

try:
    url = sys.argv[1] 
except:
    print('Usage: python crawl00.py <HOST>')
    exit(0)
 
banner = f"""
   .————————————————————————————————————————————————————.
   |      X-Powered-By : Mohamed Elsayed - @kalilo0     |
   |_______________________________________________,____| 
     ___            __      __ _   __    __        |
    / __| _ _  __ _ \ \    / // | /  \  /  \       |
   | (__ | '_|/ _` | \ \/\/ / | || () || () |    / | \ 
    \___||_|  \__,_|  \_/\_/  |_| \__/  \__/   \_\(_)/_/
                                                 //"\\\ 
    [-] User-Agent: Random()                     \\\ //
    [-] URL: {url}
    [-] Your IP: 114.30.0.200   VPN: True
"""

R,r = Fore.RED,Fore.RED
G,g = Fore.GREEN, Fore.GREEN
Y,y,YB = Fore.YELLOW,Fore.YELLOW,Fore.YELLOW
M = Fore.MAGENTA
W,w = Fore.WHITE,Fore.WHITE
B = Fore.BLUE
# GB = Fore.GREEN
RESET = Fore.RESET

G = Fore.LIGHTGREEN_EX
W = Fore.LIGHTWHITE_EX
M = Fore.LIGHTMAGENTA_EX
B = Fore.LIGHTBLUE_EX
C = Fore.LIGHTCYAN_EX
Y = Fore.LIGHTYELLOW_EX
R = Fore.RED
RESET = Fore.RESET
BLACK = Fore.BLACK

GB = Back.GREEN+BLACK
CB = Back.CYAN
RESETB = Back.RESET



def root(url):
    response = requests.get(url=url, headers=req_headers) # proxies => BurpSuite
    history = response.history
    history.append( response )
    soup = BeautifulSoup(response.content, 'html.parser')
    return history, soup

def headers_analyzer(history, req_id):
    info = {}
    for response in history:
        info[req_id] = {}
        headers = response.headers
        for key, value in headers.items():
            if key.lower() in ['server','x-powered-by','proxy-status','vary','via','set-cookie','x-frame-options','country','access-control-allow-headers','access-control-allow-methods','server-timing']:
                info[req_id][key] = value
        
        all_reqs_history[req_id] = response
        req_id += 1

    return info

def urls_extract(soup, url):

    info = {
        'Script URLs': [],
        'Form URLs'  : [],
        'Iframe URLs': [],
        'Link URLs'  : [],
        'Image URLs' : [],
        'Atag URLs'  : [],
        'Media URLs' : [],
    }

    for tag in soup.find_all('form'): 
        if tag.attrs.get('action') : info['Form URLs'].append( urljoin(url, tag.attrs.get('action')) )
     
    for tag in soup.find_all('iframe'):
        if tag.attrs.get('src') : info['Iframe URLs'].append( tag.attrs.get('src') )
    
    for tag in soup.find_all('script'):
        if tag.attrs.get('src') : info['Script URLs'].append( urljoin(url, tag.attrs.get('src')) )
    
    for tag in soup.find_all('link'):
        if tag.attrs.get('href'):
            info['Link URLs'].append( urljoin(url, tag.attrs.get('href')) )
   
    for tag in soup.find_all('img'):
        if tag.attrs.get('src') : info['Image URLs'].append( urljoin(url, tag.attrs.get('src')) )

    for tag in soup.find_all('a'):
        if tag.attrs.get('href') : info['Atag URLs'].append(urljoin(url, tag.attrs.get('href')))

    for tag in (soup.find_all('audio') + soup.find_all('video')):
        source_tags = tag.find_all("source")
        for source_tag in source_tags:
            if source_tag.attrs.get('src') : info['Media URLs'].append( urljoin(url, source_tag.attrs.get('src')))
    
    

    return info


def has_param(url):
    if '?' in url and '=' in url:
        return url

root = root(url)
history = root[0]
soup = root[1]

print(banner)

print('Headers-Analyzer\n————————————————')
for key, value in headers_analyzer(history, req_id).items():
    print('Request-ID: {key}\n—————————————')
    for key, value in value.items():
         print(f'    |__ {key} :{(16-len(key))*" "}{value}')





for key, value in urls_extract(soup, url).items():
    if value:
       print("\n" + key)
       print(len(key)*'—')
       for url in value:
           param_url = has_param(url)
           if param_url:
               print(f'[param] |__ {param_url}')
           else:
               print(f'        |__ {url}')

while 1:
    id = int(input('Request@id ~ # '))
    print(all_reqs_history[id].headers)




"""
System-info
——————.————
      |__ Server: apache/2.0 , php 8.3.0
      |__ Proxy: cloudflare
      |__ Powered-by: php 8.3.0
      |__ Wordpress: version 2.3.4
      |__ IP: 145.12.34.171

   
Auto-Header-Scanner
———————————————————
      ID    Status   Length   HTTP-Header
      ——    ——————   ——————   ———————————
      01    400      112      "Host: 127.0.0.1"



Network-Scanner(cidr=24)
———————————————
ID      IP Address       Ping    Status:URL   
———     ——————————       ————    ——————————
1       127.110.110.111  true    302:https://google.com/admin => 200:https://admin.google.com


Auto-Dork-Scanner
—————————————————
"site:example.com ext:sql" ————> http"//google.com/db.sql
                           ————> http"//google.com/db.sql
        

Open-source-analyzer
————————————————————
JS Functions: []
JS Modules: []






   

      

[4:582/7/2025] Scanning Finished 
Requests Loged : 237 => https://google.com/*
                 123 => https://bing.com?search=*


Request@id ~ # 

"""

