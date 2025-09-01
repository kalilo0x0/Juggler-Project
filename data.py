from sys import platform
from colorama import Fore, Back, init

init()


tag_names_list   = ["form","input","script","style","a","abbr","address","area","article","aside","audio","b","base","bdi","bdo","blockquote","br","button","canvas","caption","cite","code","col","colgroup","data","datalist","dd","del","details","dfn","dialog","div","dl","dt","em","embed","fieldset","figcaption","figure","footer","h1","h2","h3","h4","h5","h6","header","hgroup","hr""i","iframe","img","ins","kbd","label","legend","li","link","main","map","mark","math","menu","menuitem","meta","meter","nav","noscript","object","ol","optgroup","option","output","p","param","picture","pre","progress","q","rb","rp","rt","rtc","ruby","s","samp","search","section","select","slot","small","source","span","strong","sub","summary","sup","svg","table","tbody","td","template","textarea","tfoot","th","thead","time","title","tr","track","u","ul","var","video","wbr"]
image_ext   = ["ase", "art", "bmp", "blp", "cd5", "cit", "cpt", "cr2", "cut", "dds", "dib", "djvu", "egt", "exif", "gif", "gpl", "grf", "icns", "ico", "iff", "jng", "jpeg", "jpg", "jfif", "jp2", "jps", "lbm", "max", "miff", "mng", "msp", "nef", "nitf", "ota", "pbm", "pc1", "pc2", "pc3", "pcf", "pcx", "pdn", "pgm", "PI1", "PI2", "PI3", "pict", "pct", "pnm", "pns", "ppm", "psb", "psd", "pdd", "psp", "px", "pxm", "pxr", "qfx", "raw", "rle", "sct", "sgi", "rgb", "int", "bw", "tga", "tiff", "tif", "vtf", "xbm", "xcf", "xpm", "3dv", "amf", "ai", "awg", "cgm", "cdr", "cmx", "dxf", "e2d", "egt", "eps", "fs", "gbr", "odg", "svg", "stl", "vrml", "x3d", "sxd", "v2d", "vnd", "wmf", "emf", "art", "xar", "png", "webp", "jxr", "hdp", "wdp", "cur", "ecw", "iff", "lbm", "liff", "nrrd", "pam", "pcx", "pgf", "sgi", "rgb", "rgba", "bw", "int", "inta", "sid", "ras", "sun", "tga", "heic", "heif"]
video_ext   = ["3g2", "3gp", "aaf", "asf", "avchd", "avi", "drc", "flv", "m2v", "m3u8", "m4p", "m4v", "mkv", "mng", "mov", "mp2", "mp4", "mpe", "mpeg", "mpg", "mpv", "mxf", "nsv", "ogg", "ogv", "qt", "rm", "rmvb", "roq", "svi", "vob", "webm", "wmv", "yuv"]
method_list = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE", "CONNECT", "MOVE", "BIND", "BMOVE", "BDELETE", "LABEL", "PROPFIND", "PROPPATCH", "ACL", "CHECKIN", "CHECKOUT", "MERGE", "POLL", "NOTIFY", "REBIND", "REPORT", "SEARCH", "SUBSCRIBE", "LOCK", "LINK", "HTTP-BUG"]
ports_list  = [ 1,7,11,13,15,20,21,22,23,25,37,42,43,53,67,68,69,80,81,87,88,90,91,98,101,106,107,109,110,111,113,115,119,123,135,137,138,139,143,161,162,164,174,194,220,345,389,443,445,464,465,500,512,513,514,515,532,543,544,546,547,548,554,587,636,646,749,750,751,754,760,775,777,853,871,873,902,989,990,992,993,995,999,1000,1024,1080,1094,1194,1433,1434,1521,1529,1646,1701,1720,1723,1812,1813,1957,1958,2000,2002,2003,2010,2030,2049,2086,2105,2121,2181,2222,2323,2375,2401,2432,2483,2484,2628,2792,2988,2989,2999,3000,3050,3074,3128,3130,3306,3307,3389,3600,4145,4353,4440,4444,4500,4505,4506,4557,4559,4600,4664,4899,5000,5060,5061,5222,5223,5269,5353,5432,5433,5555,5601,5722,5800,5900,5901,5984,6000,6379,6446,6514,6566,6667,6970,6999,7000,7001,7002,7003,7004,7005,7006,7007,7008,7009,7070,7080,7100,7600,7700,8002,8006,8008,8021,8069,8080,8081,8085,8086,8087,8089,8090,8091,8118,8123,8140,8180,8181,8222,8440,8443,8800,8880,8881,8888,9000,9043,9050,9060,9090,9091,9092,9100,9150,9200,9300,9392,9418,9667,9673,9900, 9960,10000,10809,11201,11211,11371,12345,13724,15672,17500,22125,22128,27017,27374,30303,36268,49152,49153,49200,50000,57000]

static_headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=1000",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:30.0) Gecko/20100101 Firefox/33.0",
    }

cookie_security = ['samesite','SameSite','secure','Secure','Max-Age','max-age','Expires','expires','httponly','HttpOnly','domain','Domain','path','Path']


vuln_headers = {
    'User-Agent': '<img src=x onerror="alert(0)">',
    'Host': '127.0.0.1',
    'Host': 'localhost',
    'Host': '127.1',
    'Host-Name': 'localhost',
    'X-Forwarded-For': '127.0.0.1',
    'Forwarded-For': '127.0.0.1',
    'Forwarded':'127.0.0.1',
    'Origin': 'http://127.0.0.1',
    'Reffered': 'http://127.0.0.1',
    'Refered': 'http://127.0.0.1',
    'Accept-Encoding': 'br',
    'Admin': 'true',
    'Client-Address': '127.0.0.1',
    'Client-Ip': '127.0.0.1',
    'Cookie': 'cookie=abcdef0123456789',
    'Javascript': 'false',
    'Local-Addr': '127.0.0.1',
    'Proxy-Host': '127.0.0.1',
    'Proxy-User': 'admin',
    'Remote-Addr': '127.0.0.1',
    'Remote-Host': 'localhost',
    'Remote-User': 'admin',
    'Request-Method': 'CONNECT',
    'Root': 'true',
    'True-Client-Ip': '127.0.0.1',
    'Token': 'abcdef0123456789',
    'User': 'admin',
    'User-Name': 'admin',
    'Work-Directory': 'admin',
    # X-Authorization
    'X-Auth-Password': 'password',
    # X-Auth-Service-Provider
    'X-Auth-Token': 'abcdef0123456789',
    'X-Auth-User': 'admin',
    'X-Auth-Userid':'0',
    'X-Auth-Username': 'admin',
    'X-Client-Ip': '127.0.0.1',
    'X-Client-Host': 'localhost',
    'X-Client-Os': 'windows',
    'X-Client-Os': 'android',
    'X-Client-Os': 'linux',
    'X-Csrf-Token': 'abcdef0123456789',
    'X-Forwarded-By': 'localhost',
    'X-Forwarded-For-Original': '127.0.0.1',
    'X-Forwarded-Host': 'localhost',
    'X-Forwarded-Port': '80',
    'X-Forwarded-Proto': 'tcp/http',
    # X-Forwarded-Protocol
    # X-Forwarded-Scheme
    # X-Forwarded-Server
    # X-Forwarded-Ssl
    # X-Forwarded-Ssl 
    'X-Forwarder-For': '127.0.0.1',
    'X-Forward-For': '127.0.0.1',
    # X-Forward-Proto
    'X-Host': 'localhost',
    'X-Http-Method': 'JUGGLER',
    'X-Http-Method-Override': 'JUGGLER',
    'X-Http-Path-Override': 'JUGGLER',
    'X-Ip': '127.0.0.1',
    'X-Ip-Trail': '127.0.0.1',
    # X-Orig-Client
    # X-Original-Host
    # X-Original-Http-Command
    # X-Originally-Forwarded-For
    # X-Originally-Forwarded-Proto
    # X-Original-Remote-Addr
    # X-Original-Url
    # X-Original-User-Agent
    'X-Originating-Ip': '127.0.0.1',
    'X-Real-Ip': '127.0.0.1',
    'X-Remote-Addr': '127.0.0.1',
    'X-Server-Port': '2027',
    'X-User': 'admin',
    'X-User-Agent': '<img src=x onerror="alert(0)">',
    'X-Username': 'admin',
    'X-Username': 'root',
}


status_codes = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Unused",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    407: "Proxy Authentication Required",
    406: "Not Acceptable",
    408: "Request Timeout",
    409: "Conflict",
    414: "Request-url Too Long",
    419: "Page Expired 'Laravel Framework'",
    421: "Misdirected Request",
    429: "Too Many Requests",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported"
}






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

error_wordlist = [
    "Failed","failed", "FAILED"
    "Invalid","invalid","INVALID"
    "Wrong","WRONG","wrong",
    "Error","ERROR","error",
    "False","false","FALSE", 
    "failure","Failure", "FAILURE"
    "not true", "Not True", "Not true", "NOT TRUE"
    "incorrect","Incorrect","INCORRECT" 
    "sorry","Sorry","SORRY"
    "Unknown","unknown","UNKNOWN",
    
    "خطأ","خطا",
    "لا توجد", "لا يوجد", "غير موجود"
    "غير صحيح",
    
    "hata",
    "başarısız",
    "bilinmeyen",
    "yanlış",
    
    "desconocido", "Desconocido",
    "incorrecto", "Incorrecto"
                 ] 