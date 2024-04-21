import sys
import time
import requests
import tldextract
from yaspin import Spinner 

VERSION = "1.1.12"
_API_URL = 'https://chiasmodon.com/v2/api/beta'
_API_HEADERS = {'user-agent':'cli/python'}
_VIEW_TYPE = {
    'cred':['domain', 'email', 'cidr', 'app', 'asn', 'username','password',  'endpoint',],
    'url':['domain', 'email', 'cidr', 'asn', 'username','password', 'endpoint',],
    'subdomain':['domain'],
    'email':['domain', 'cidr', 'asn', 'app' ,'endpoint', 'phone', 'password'],
    'password':['domain', 'cidr', 'app', 'asn', 'email' 'username', 'endpoint'],
    'username': ['domain', 'cidr', 'app', 'asn', 'email','password','endpoint',],
    'app':['cidr', 'asn', 'email', 'username','password','phone'],
    #'phone':['domain','cidr', 'asn', 'email', 'username','password', 'endpoint'],
    'endpoint':['domain','cidr', 'asn', 'email', 'username','password',],
    'port':['domain','cidr', 'asn', 'email', 'username','password'],
}

_METHODS = [
    'domain',
    'email',
    'asn',
    'cidr',
    'app',
    'username',
    'password',
    'endpoint',
    #'phone',
]

VIEW_TYPE_LIST = list(_VIEW_TYPE.keys())

class T:
    RED      = '\033[91m'
    GREEN    = '\033[92m'
    YELLOW   = '\033[93m'
    BLUE     = '\033[94m'
    MAGENTA  = '\033[95m'
    CYAN     = '\033[96m'
    RESET    = '\033[0m'


class Chiasmodon:
    def __init__(self, token=None, color=True, debug=True,check_token=True) -> None:

        self.token = token
        self.debug = debug
        self.err :bool   = False 
        self.msg :str    = '' 
        self.__result:list[Result] = []
        self.scan_mode = False
        
        if not color:
            T.RED      = ''
            T.GREEN    = ''
            T.YELLOW   = ''
            T.BLUE     = ''
            T.MAGENTA  = ''
            T.CYAN     = ''
            T.RESET    = ''
        
        if self.token and check_token:
            if self.__check_token():
                self.print(f'{T.GREEN}Set token successfully{T.RESET}')

            else:
                self.print(f'{T.RED}{self.msg}{T.RESET}')
                sys.exit()
    
    def filter_domain(self,d) -> str:
        domain = d.split()[0]
        x = tldextract.extract(domain)
        if x.subdomain:return '{}.{}.{}'.format(x.subdomain,x.domain, x.suffix)
        else:return '{}.{}'.format(x.domain, x.suffix)

    def print(self,text, ys=None, ys_err=False) -> None:
        if text == None:return 
        if self.debug:
            if ys:
                if not ys_err:
                    ys.write(text)
                else:
                    ys.text = text
            else:
                print(text)

    def __check_token(self):
        if self.__request({
            'token':    self.token,
            'method':   'check-token'
        }).get('is_active'):
            return True 

        return False 

    def __request(self, data:dict,timeout=60):

        try:
            resp = requests.post(_API_URL, data=data, headers=_API_HEADERS, timeout=timeout)
            resp.close()
            resp = resp.json()

            try:
                if resp.get('err'):
                    self.err = True 
                    self.msg = resp['msg']
            except:pass

            return resp

        except requests.exceptions.ReadTimeout:
            self.print(f"{T.RED}\nError: timeout !\nPlease try agine later.{T.RESET}")
            sys.exit()

        except requests.exceptions.InvalidJSONError:
            self.print(f"{T.RED}\nError: Server send wrong data.\nPlease try agine later.{T.RESET}")
            sys.exit()

        except Exception as e:
            self.print(f"{T.RED}\nRequest error: {e}\nPlease try agine later.{T.RESET}")
            sys.exit()


    def __proc_query(self, 
                    method:str, 
                    query:str, 
                    view_type:str, 
                    country:str,
                    timeout:int,
                    sort:bool, 
                    only_domain_emails:bool,
                    all:bool,
                    limit:int,
                    related:bool,
                    callback_view_result:None,
                    yaspin:bool,
                    ) -> dict:
        
        Result.VIEW_TYPE = view_type

        result : list[Result] = []

        data = {

            'token':self.token,
            'type-view':view_type,
            'method' : 'search-by-%s' % method,
            'version' : VERSION,
            'query' : query,
            'country' : country.upper(),
            'all':'yes' if all else 'no',
            'related':'yes' if related else 'no',
            'domain-emails':'yes' if only_domain_emails else 'no',
            'get-info':'yes'
        }

        if yaspin:
            with yaspin(Spinner(["🐟","🐠","🐡","🐬","🐋","🐳","🦈","🐙","🐚","🪼","🪸"], 200),text=f"Processing {query} ...") as sp:
                process_info = self.__request(
                    data=data,
                    timeout=timeout,
                )

            if process_info and process_info.get('count') == 0:
                if method == 'domain' and not all and not only_domain_emails and not self.scan_mode:
                    self.print(f"{T.RED}Not found result\nTo view more result try: {T.BLUE}--all{T.RESET}", sp,ys_err=True)

                elif method == 'domain' and all and not only_domain_emails  and not self.scan_mode:
                    self.print(f"{T.RED}Not found result\nTo view more result for this target try: {T.BLUE}--domain-emails{T.RESET}", sp,ys_err=True)
                
                else:
                    self.print(f"{T.RED}Not found result{T.RESET}", sp,ys_err=True)

                sp.fail("💥 ")
                sp.stop()
                return result 

            else:
                sp.ok("⚓ ")

        else:
            process_info = self.__request(
                data=data,
                timeout=timeout,
            )
            if process_info and process_info.get('count') == 0:
                self.print(f"{T.RED}Not found result{T.RESET}")
                return result
            
        
        del data['get-info'] 

        if self.err:
            self.err= False
            raise Exception(f'{T.RED}Error: {self.msg}{T.RESET}') 
            
        self.print(f"{T.YELLOW}Result count{T.YELLOW}: {T.GREEN}{process_info['count'] if process_info['count'] != -1 else 'unknown'}{T.RESET}")

        data['sid'] = process_info['sid']

        if yaspin:
            YS = yaspin(f'Get pages 0/{process_info["pages"]}').green.bold.shark #.on_black
            YS.start()

        else:
            YS = None
        
        for p in range(1, process_info['pages']+0x1):
            if yaspin:YS.text = f'Get pages {p}/{process_info["pages"]}'
            
            data['page'] = p

            beta_result = self.__request(
                data=data,
                timeout=timeout,
            )

            if self.err:
                self.err=False
                if yaspin:self.print(f"{T.RED}{self.msg}{T.RESET}", YS, ys_err=True);YS.fail("💥 ");YS.stop()
                return result
            
            for r in beta_result['data']:
                
                column :Result = Result(**r)

                if sort and column in self.__result:
                    continue
                
                if callback_view_result:
                    callback_view_result(beta=column, ys=YS)

                result.append(column)
                self.__result.append(column)
              
                if len(result) == limit:
                    if yaspin:YS.text='';YS.stop()
                    return result
                
            if beta_result['done']:
                if yaspin:YS.text='';YS.stop()
                return result

            time.sleep(0x1)

        if not result:
            
            if yaspin:self.print(f"{T.RED}Not found result{T.RESET}", YS,ys_err=True);YS.fail("💥 ");YS.stop()
            else:self.print(f"{T.RED}Not found result{T.RESET}")
        else:
            if yaspin:YS.text='';YS.stop()

        return result
    
    def search(self,
               query,
               method='domain',
               country='all',
               view_type='cred',
               limit=10000,
               all=False,
               only_domain_emails=False,
               timeout=60,
               sort=True,
               yaspin=False,
               related=False,
               callback_view_result=None) -> dict:
        
        
        if method not in _METHODS:
            raise Exception(f"{T.RED}not found this method: {method}.{T.RESET}")
        
        if method not in _VIEW_TYPE[view_type]:
            raise Exception(f"{T.RED}{view_type} doesn't support ({method}).{T.RESET}")

        if only_domain_emails and method != 'domain':
            raise Exception(f"{T.RED}domain emails support only (domain) method.{T.RESET}")
        
        if all and method not in ['app', 'domain']:
            raise Exception(f"{T.RED}all support only methods (app, domain).{T.RESET}")
        
        self.err = False
        self.msg = ''

        if method == 'domain':query = self.filter_domain(query)

        result = self.__proc_query(
            method=method,
            query=query,
            country=country,
            view_type=view_type if not related else 'subdomain',
            sort=sort,
            timeout=timeout,
            only_domain_emails=only_domain_emails,
            all=all,
            limit=limit,
            related=related,
            callback_view_result=callback_view_result,
            yaspin=yaspin,
        )

        self.__result:list = []

        return result

class Result(dict):
    VIEW_TYPE = None

    def __init__(self,type,**kwargs) -> None:
        
        self.kwargs         = kwargs
        Type           = type 

        self.url            = None
        self.urlPort        = None
        self.urlEndpoint    = None
        self.email          = None
        self.username       = None
        self.password       = None
        self.country        = None
        self.date           = None 
        self.domain         = None 
        self.phone          = None 
        self.ip             = None 
        self.asn            = None
        self.appID          = None
        self.appName        = None 
        self.appDomain      = None 


        if Type == "login":
            if kwargs.get('url'):
                self.urlEndpoint = kwargs['url']['path']
                self.urlPort = kwargs['url']['port']
                self.url    = self.__convert_url(kwargs['url'])
                
                if kwargs['url']['ip']:
                    self.ip     = kwargs['url']['ip']['ip']
                    self.asn    = kwargs['url']['ip']['asn']

                elif kwargs['url']['domain']:
                    self.domain = self.__convert_domain(kwargs['url']['domain'])    
                

            if kwargs.get('app'):
                self.appID   = kwargs['app']['id']
                self.appName = kwargs['app']['name']
                if kwargs['app']['domain']:
                    self.appDomain = self.__convert_domain(kwargs['app']['domain'])
            
            if kwargs.get('cred'):
                if kwargs['cred']['email']:
                    self.email = self.__convert_email(kwargs['cred']['email'])

                self.username = kwargs['cred']['username']
                self.password = kwargs['cred']['password']

            if kwargs.get('country'):
                self.country = kwargs['country']['f']
            
            self.date = kwargs['date']


        if Type == 'url':
            self.urlEndpoint = kwargs['path']
            self.urlPort = kwargs['port']
            self.url = self.__convert_url(kwargs)

            if kwargs['ip']:
                self.url    = self.__convert_url(kwargs)
                self.ip     = kwargs['ip']['ip']
                self.asn    = kwargs['ip']['asn']

            elif kwargs['domain']:
                self.domain = self.__convert_domain(kwargs['domain'])    

        if Type == "email":
            self.email = self.__convert_email(kwargs)
        
        if Type == "domain":
            self.domain = self.__convert_domain(kwargs)

    def __convert_email(self,email):
        return f"{email['name']}@{self.__convert_domain(email['domain'])}"

    def __convert_url(self,url:dict):
        if url['domain']:
            return f"{url['proto']}://{self.__convert_domain(url['domain'])}:{url['port']}{url['path']}" 
        elif url['ip']:
            return f"{url['proto']}://{url['ip']['ip']}:{url['port']}{url['path']}" 

        
        return None 

    def __convert_domain(self,domain:dict):
        if domain['sub']:
            return f"{domain['sub']}.{domain['name']}.{domain['suffix']}"
        else:
            return  f"{domain['name']}.{domain['suffix']}"


    def __str__(self) -> str:
        return self.save_format()

    def __radd__(self, other):
        if isinstance(other, str):
            return   other + self.save_format() 
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, str):
            return self.save_format() + other
        else:
            return NotImplemented
          
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError(f"'Result' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value
        
    
    def print(self,):
        if self.VIEW_TYPE == "endpoint" and self.urlEndpoint and self.urlEndpoint != '/':
            return f"{T.MAGENTA}[ {T.YELLOW}Endpoint{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.urlEndpoint}{T.RESET}"
        
        if self.VIEW_TYPE == "port" and self.urlPort:
            return f"{T.MAGENTA}[ {T.YELLOW}Port{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.urlPort}{T.RESET}"

        if self.VIEW_TYPE == "email" and self.email:
            return f"{T.MAGENTA}[ {T.YELLOW}Email{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.email}{T.RESET}"
        
        if self.VIEW_TYPE == "app" and self.appID:
            return f"{T.MAGENTA}[ {T.YELLOW}App ID{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.appID}{T.RESET}"
        
        if self.VIEW_TYPE == "url" and self.url:
            return f"{T.MAGENTA}[ {T.YELLOW}Url{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.url}{T.RESET}"
        
        if self.VIEW_TYPE == "subdomain" and self.domain:
            return f"{T.MAGENTA}[ {T.YELLOW}Domain{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.domain}{T.RESET}"

        #if self.VIEW_TYPE == "phone" and self.phone:
        #    return f"{T.MAGENTA}> {T.CYAN}{self.domain}{T.RESET}"
        

        if self.VIEW_TYPE == "cred":
            c= ""
            if self.url:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}>  {T.CYAN}{self.url}{T.RESET}\n"

            if self.urlEndpoint and self.urlEndpoint != '/':c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Path{T.RESET}{' ':10}: {T.CYAN}{self.urlEndpoint}{T.RESET}\n"

            if self.urlPort and self.urlPort not in [80, 443]:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Port{T.RESET}{' ':10}: {T.CYAN}{self.urlPort}{T.RESET}\n"
            if self.asn:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.MAGENTA}> {T.RED} ASN{T.RESET}{' ':11}: {T.CYAN}{self.asn}{T.RESET}\n"
            
            if self.appID:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.RED}{T.MAGENTA}>  {T.CYAN}{self.appID}{T.RESET}\n"
            if self.appName:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.RED}{T.MAGENTA}> {T.RED} Name{T.RESET}{' ':10}: {T.CYAN}{self.appName}{T.RESET}\n"
            if self.appDomain:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Domain{T.RESET}{' ':8}: {T.CYAN}{self.appDomain}{T.RESET}\n"
            
            if self.email:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Email{T.RESET}{' ':9}: {T.GREEN}{self.email}{T.RESET}\n"
            if self.username and not self.email:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Username{T.RESET}{' ':6}: {T.GREEN}{self.username}{T.RESET}\n"
            if self.password:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Password{T.RESET}{' ':6}: {T.GREEN}{self.password}{T.RESET}\n"
            
            if self.country:c+=f"{T.MAGENTA}[ {T.YELLOW}INFO{T.MAGENTA} ]{T.MAGENTA}>{T.RED}  Country{T.RESET}{' ':7}: {T.BLUE}{self.country}{T.RESET}\n"
            #if self.date:c+=f"{T.MAGENTA}[ {T.YELLOW}INFO{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Date{T.RESET}{' ':10}: {T.BLUE}{self.date}{T.RESET}\n"

            #c+=f"{T.MAGENTA}{'+'*30}{T.RESET}"
            return c            

    def save_format(self):
        result = []
        if self.VIEW_TYPE == "cred":
            # 1 
            if self.url:
                result.append(self.url)
            elif self.appID:
                result.append(self.appID)
            else:
                result.append('')

            # 2
            if self.username:
                result.append(self.username)
            elif self.email:
                result.append(self.email)
            else:
                result.append('')
            
            # 3 
            if self.password:
                result.append(self.password)
            else:
                result.append('')
            
            # 4 
            if self.country:
                result.append(self.country)
            else:
                result.append('')
            
            # 5
            #if self.date:
            #    result.append(self.date)
            #else:
            #    result.append('')

            return result

        elif self.VIEW_TYPE == 'subdomain':
            return self.domain
        
        elif self.VIEW_TYPE == 'email':
            return self.email
        
        elif self.VIEW_TYPE == 'endpoint':
            return self.urlEndpoint
        
        elif self.VIEW_TYPE == 'port':
            return f"{self.urlPort}"
        
        elif self.VIEW_TYPE == 'app':
            return self.appID
        
        elif self.VIEW_TYPE == 'url':
            return self.url
        else:
            return 'null'