import sys
import os

from data import *
from tools import *

is_windows = sys.platform.startswith('win')
wordlist_path = 'wordlist\passwords.txt'
wordlist_len = open(wordlist_path, 'r').read().splitlines()
http_headers = open('wordlist\http_headers.txt', 'r').read().splitlines()
is_req_sended = False

crawl_mode = 'off'
verbose = 'off'

session = requests.Session()

req_config = {
    "url":      "http://localhost",
    "ip":       "127.0.0.1",
    "host":     "127.0.0.1",
    "method":   "GET",
    "data":     {},
    "params":   {},
    "timeout":  10,
    "redirect": True,
    "verify":   True,
    "stream":   False,
    "auth":     {},
    "proxies":  {},
    
    "headers" : {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",#"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=1000",
        "User-Agent": "Opera/9.21 (Windows NT 5.1; U; en)",
    }
}

info_gathered = {
    'web-server': '',
    'powerd-by': '',    
    'open-ports': [],    
    'use-wordpress': {
        'status': '',
        'version': '', 
        },   
    'robots.txt': {
        'status': '',
        'user-agents': [],
        'disallow': [],
        'site-map': '',
        },    
    'urls': {},  
    'subdomains': [],   
    'tags': {},
    'history': [],
}

def BANNER():
    if is_windows:
        os.system('cls')
    else:
        os.system('clear')
    
    print(f"""{W}.————————————————————————————————————————————————————————————.   
|         {GB}{BLACK} X-Powered-By : Mohamed Elsayed - @kalilo0 {RESETB} {W}       |
|_______________________________________________________{w},{W}____|  
{W}    .__.                     .__.                       {w}|      {W}
{W}    |__| __ __  ____    ____ |  |    ____ _______       {w}|      {W}
{W}    |  ||  |  \/ ___\  / ___\|  |  _/ __ \\\_  __ \    {w}/ | \   {W}
{W}    |  ||  |  / /_/  |/ /_/  |  |__\  ___/ |  | \/  {w}\_\(_)/_/  {W}
{W}/\__|  ||____/\___  / \___  /|____/ \_____\|__|       {w}//"\\\      {W}
{W}\______|     /_____/ /_____/  {Y}CRAWLER MODE: {crawl_mode.upper( )}   {g}    {w}\\\ //     {W}
                                                                {W}  """)   
    print(f' {w}[-] URL :  {R}{req_config["url"]}{RESET} {w}, Method : {GB}{BLACK}{req_config["method"]}{RESETB}')
    print(f' {w}[-] Params : {R}{req_config["params"]}{RESET}')
    print(f' {w}[-] Data : {R}{req_config["data"]}{RESET}')
    # print(f' {w}[-] Verbose : {R}{verbose}{RESET}')
    print(f' {w}[-] Wordlist : {R}{wordlist_path} [{B}{len(wordlist_len)}{R}]\n')
    for key, value in req_config['headers'].items():
        if key == 'Cookie':
            print(f' {w}[-] {key} : {R}' + value.replace(';', ';\n             ') )
        else:
            space = (16-len(key))*' '
            print(f' {w}[-] {key} : {space}{R}{value}{RESET}')
    print()
#------------------------------------
def URL_PARSER(url):
    if '.' not in url and 'localhost' not in url:
        return
    if ':' in url:
        if url.split(':')[1] == '443':
            url = 'https://' + url
    if not url.startswith('http'):
        url = 'http://' + url

    return url
#------------------------------------
def REQUESTER():
    try: response = requests.request( url=req_config['url'],
                                 method=req_config['method'], 
                                 headers=req_config['headers'],
                                 verify=req_config['verify'], 
                                 stream=req_config['stream'], 
                                 data=req_config['data'], 
                                 params=req_config['params'], 
                                 allow_redirects=req_config['redirect'], 
                                 proxies=req_config['proxies'],
                                 auth=req_config['auth'],
                                 timeout=req_config['timeout'] )
    
    except KeyboardInterrupt:
        print(f'{r}       |__ ERROR: Request Interrupted')
        return
    except Exception as error:
        print(f'{r}       |__ ERROR:', error)
        return
    
    history = response.history
    history.append(response)
        
    info_gathered['history'] = history
    
    for res in history:
        HOST = urlparse(res.url).netloc.split(':')[0]
        IP = socket.gethostbyname(HOST)
        STATUS = f'{res.status_code} {status_codes[res.status_code]}'
        CONTENT = res.content
        SOUP = BeautifulSoup(CONTENT, 'html.parser')
        HEADERS = res.headers
        CONTENT_TYPE = HEADERS.get('Content-Type', '')
        ELAPSED = res.elapsed
        ENCODING = res.encoding
        APPARENT_ENCODING = res.apparent_encoding

        def GET_DATA_SIZE(content):
            size_byte = sys.getsizeof(content)
            if size_byte > 1024 and size_byte < (1024*1024):
                size = f'{round(size_byte/1024, 2)} Kb'
            elif size_byte > (1024*1024) and size_byte < (1024*1024*1024):
                size = f'{round(size_byte/ (1024*1024), 2)} Mb'
            else:
                size = f'{size_byte} byte'
            return size
        
        DATA_SIZE = GET_DATA_SIZE(CONTENT)
        
        try: TITLE = SOUP.find('title').text
        except: TITLE = ''
 
        try: TEXT = SOUP.find('body').text
        except: TEXT = ''
        
        print(f'{W}  General')
        print(f'     {y}|_ URL :               {g}{res.url}')
        print(f'     {y}|_ Status :            {g}{STATUS}')
        print(f'     {y}|_ Title :             {g}{TITLE}')
        print(f'     {y}|_ Size :              {g}{DATA_SIZE}')
        print(f'     {y}|_ Time :              {g}{ELAPSED}')
        print(f'     {y}|_ Encoding :          {g}{ENCODING}')
        print(f'     {y}|_ Apparent-Encoding : {g}{APPARENT_ENCODING}')
        print(f'     {y}|_ IP-Address :        {g}{IP}')
        
        print(f'{W}  Headers')
        for key, value in HEADERS.items():
            SPACE = (18-len(key))*' '
            if key.lower() in ['server','x-powered-by','proxy-status','vary','via','set-cookie','x-frame-options','country','access-control-allow-headers','access-control-allow-methods','server-timing']:
                print(f'     {y}|_ {W}{key} :{SPACE}{B}{value}{RESET}')
            else:
                print(f'     {y}|_ {y}{key} :{SPACE}{g}{value}{RESET}')
        
        print(f'{y}     |' + '_'*45)

        if res.status_code != 200:
            COLORED_HTML = highlight(SOUP.prettify(), HtmlLexer(), TerminalFormatter())
            print(COLORED_HTML)

    
         
if __name__ == '__main__':
    BANNER()
    while True :
      
        # try: 
        cmd = input(f' {GB}{BLACK}$_ {RESETB}{W} ')
        # except KeyboardInterrupt: break
        
        if cmd in ['data','params']:
            while True:
                try:
                    name = input("     |______ Enter the name: ")
                except KeyboardInterrupt:
                    break
    
                if name.lower() == 'clear':
                    req_config[cmd].clear()
                    break
                elif name.lower() == 'exit':
                    break
                    
                try:
                    value = input("     |______ Enter the value: ")
                except KeyboardInterrupt:
                    break
                
                
                req_config[cmd][name] = value
    
                
            BANNER()
        
        elif cmd == 'info -s':
            with open(f"{req_config['host']}_info.json", 'w') as file:
                file.write(str(info_gathered))
                file.close()
                print(f'{g} [i] File Saved Successfully.')
        elif cmd == 'xss':
            xss_scanner(req_config['url'], req_config['headers'])
        elif cmd == 'error':
            GET_ERROR_RESPONSE(req_config['url'])
        elif cmd == 'pscan':
            PORT_SCANNER(req_config['host'], ports_list)
            from tools import open_ports
            info_gathered['open-ports'] = open_ports
        elif cmd == 'robot':
            parse_robots_txt(req_config['url'])
        elif cmd == 'info':
            pprint(info_gathered)
        elif cmd == 'sshbrute':
            ssh_brute(req_config['host'])
        elif cmd == 'netscan':
            net_scan(req_config['host'])
        elif cmd == 'ip':
            print('      |_______' , socket.gethostbyname(req_config['host']))
        elif cmd == '6':
            brute_force_login(req_config['url'])
        elif cmd == 'whois':
            WHOIS_LOOKUP(req_config['host'])
            DNS_LOOKUP(req_config['host'])
            GEO_LOOKUP(req_config['host'])
        elif cmd =='urls':
            URLS_EXTRACTOR(BeautifulSoup(info_gathered['history'][-1].content, 'html.parser'), req_config['url'], req_config['host'])
            from tools import urls
            info_gathered['urls'] = urls
            info_gathered['subdomains'] = subdomains
        elif cmd == 'wordlist':
            value = input('       |_____________ ')
            wordlist_path = value
            wordlist_len = open(wordlist_path, 'r').read().splitlines()
            BANNER()
        elif cmd == 'hscan':
            header_scanner(req_config['url'])
        elif cmd == 'html':
            HTML_ANALYZER(BeautifulSoup(info_gathered['history'][-1].content, 'html.parser'))
        elif cmd == 'config':
            pprint(dict(req_config))
        elif cmd == 'default':
           # req_config['headers'] = dict()
            req_config['headers'] = static_headers
            req_config['data'] = {}
            req_config['params'] = {}
            req_config['method'] = 'GET'
            BANNER()
        elif cmd.lower() in ['tools', 'help']:
            print(tools)
        elif cmd == 'send':
            REQUESTER()
            is_req_send = True
        elif cmd == 'url':
            value = input('      |_____________ ')
            url = URL_PARSER(value)
            if url:
                host = urlparse(url).netloc
                req_config['host'] = host.split(':')[0]
                req_config['url'] = url
                req_config['headers']['Host'] = host
                BANNER()
            else:
                print(f'{r}       |_ ERROR: Invalid URL')
        elif cmd == 'method':
            value = input('       |_____________ ')
            req_config[ cmd ] = value
            BANNER()
        
        
        elif cmd in ['timeout']:
            try:
                req_config['timeout'] = float(input('       |_____________ '))
            except Exception as error:
                print(f'{r} [!] ERROR:', error)
        elif cmd in ['clear', 'cls']:
            BANNER()
        elif cmd == 'verify':
            req_config['verify'] = False
            print('Verify is False')
        elif cmd == 'exit':
            sys.exit()
        elif cmd == 'restart':
            os.system(f'python {os.getcwd()}/juggler.py')
        elif len(cmd.split(' ')) > 1 and cmd.split(' ')[0] == 'cd':
            try:
                os.chdir(cmd.split(' ')[1])
            except Exception as error:
                print(f'{r} [!] ERROR:', error)
        elif cmd.startswith('H '):
            value = input('       |_____________ ')
            req_config['headers'][cmd.replace('H ', '')] = value
            BANNER()
        # else:
        #     for header in http_headers:
        #         if header.lower() == cmd or header == cmd:
        #             value = input('       |_____________ ')
        #             req_config['headers'][cmd] = value
        #             BANNER()