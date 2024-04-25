"""
parse_web
=====
Using this module
you can get important information from a URL
It is enough to provide a url as the input of this class.✨
>>> import parse_web as pw

Using  package:
---------------------
>>> url = set_url("https://example.com")
>>> p = url.method()
>>> print(p)


This module can:
---------------------
1. Returns the IP address of the website
2. return website information
3. return the used technologies
4. Ping returned the site
5. Return all links
6. Returns the address of the used images
7. Returns the address of the used videos
8. Return the link of the social networks of the site
9. You can search for a word in the website
10. Returns the body code
11. Returns the CSS code
12. It returns textual content
13. Find the target tag
14. You can see if the site is developed with WordPress or not
15. and other works...
"""



""""
                                          _     
 _ __   __ _ _ __ ___  ___  __      _____| |__  
| '_ \ / _` | '__/ __|/ _ \ \ \ /\ / / _ \ '_ \ 
| |_) | (_| | |  \__ \  __/  \ V  V /  __/ |_) |
| .__/ \__,_|_|  |___/\___|   \_/\_/ \___|_.__/ 
|_|                                             


"""

# thelegram  : https://t.me/the_developerman 



import os 

# installing packages : 
try:
    import pythonping as p
    from  string import ascii_uppercase
    from bs4 import BeautifulSoup as bs
    import requests
    import socket
except:
    os.system("pip install pythonping")
    os.system("pip install beautifulsoup4")
    os.system("pip install requests")

# ERR Handeling : 
class NetworkError(Exception):
    pass

class NoneUrlError(Exception):
    pass

class ModeError(Exception):
    pass



# Encryption of domains : 
tkn = {
".com" : 'registrarData' , 
'.net' : "registrarData" ,
'.ir' : 'registryData' , 
'.org'  : 'registryData' , 

}

class set_url:
    '''By using the set_url class, you can retrieve important information from a URL.
    Just provide a URL starting with http or https as the input to this class.✨'''


    def __init__(self , url:str):  
        # url_type_1 >> Along with the protocol . 
        # url_type_2 >> No protocol .  
        
        if url[-1]=='/': 
            self.url = url[:-1]
        else:
            self.url = url


        if 'https:' in self.url:
            self.url_type_1 = self.url 
            self.url_type_2 = self.url[8:]
        elif "http:" in self.url:
            self.url_type_1 = self.url
            self.url_type_2 = self.url[7:]
        else:
            self.url_type_1=f'https://{self.url}'
            self.url_type_2=url

    def __str__(self):
        return f'This is an object with input {self.url} of class set_url'
    
    def __eq__(self , other):
        return self.ping() == other.ping()
    
    def __gt__(self , other):
        return self.ping() > other.ping()
    
    def __lt__(self , other):
        return self.ping() < other.ping()

    def __add__(self , other):
        return int(self.ping()[:3]) + int(other.ping()[:3])
    
    def __sub__(self , other):
        return int(self.ping()[:3]) - int(other.ping()[:3])


    def robots(self):
        """Returns the accesses of bots
            In other words, it returns the robots.txt file."""
        if '/' in self.url_type_2: # google.com\home
            domain = f"https://{self.url_type_2.split('/')[0]}"
        else:
            domain = f'https://{self.url_type_2}'

        news_url =  "{0}/{1}".format(domain , "robots.txt")
        try:
            request = requests.get(news_url)
        except Exception as e:
            raise e
        try:
            text = request.text
            if 'html' not in text:
                return text
            return False
        except  Exception as e :
            return e         

    def get_ip(self):
        '''Return IP address from  Entered url'''
        if '/' in self.url_type_2:
            self.domain  = self.url_type_2.split("/")[0]
        else:
            self.domain = self.url_type_2
        try:
            ip = socket.gethostbyname(self.domain)
            return ip
        except NetworkError as e : 
            return '{type_error} : {message}'.format(type_error = 'NetworkError' , message=e )
        
    def html_code(self):
        '''Returns body code'''
        try:
            request = requests.get(self.url_type_1)
            html = request.text
            bot = bs(html , 'html.parser')
            return bot.prettify
        except NetworkError as e :
            return '{type_error} : {message}'.format(type_error = 'NetworkError' , message=e )
        
    def css_code(self , link_or_code='link'):
        """Returns CSS code"""
        list_of_css_link = []
        request = requests.get(self.url_type_1)
        body = request.text
        bot = bs(body , 'html.parser')
        for  css_link in bot.find_all("link"):
            link  = css_link.get("href")
            if '.css' in link:
                if 'http' not in link:
                    link_2 = f"{self.url_type_1}/{link}"
                    list_of_css_link.append(link_2)
                else:
                    list_of_css_link.append(link)
        if link_or_code == 'link':
            return list_of_css_link
        elif link_or_code =='code':
            list_of_css_code = {}
            try:
                for link in list_of_css_link:
                    req = requests.get(link)
                    list_of_css_code[link]=req.text
                return list_of_css_code
            
            except Exception as e:
                return e 
        else:
            raise ModeError('ModeError: The link_or_code argument can be code or link ')
        
    def title(self):
        """Returns the entered url title."""

        request = requests.get(self.url_type_1)
        body = request.text
        bot = bs(body , 'html.parser')
        x=bot.find("title")
        return x.string 
    
        # or 

        # try:
        #     request = requests.get(self.url_type_1)
        #     body = request.text
        #     bot = bs(body , 'html.parser')
        #     return bot.title.name
        # except NetworkError as e :
        #     return '{type_error} : {message}'.format(type_error = 'NetworkError' , message=e )
        
    def text(self ):
        '''Returns the text content of the page . '''
        try:
            req = requests.get(self.url_type_1)
            body = req.text
            bot = bs(body , 'html.parser')
            return bot.get_text()
        except Exception as en :
            raise NetworkError(en)
        
    def get_links(self):
        """Puts all the links in a list and returns the list"""
        list_of_links = list()
        try:
            request = requests.get(self.url_type_1)
            body = request.text
            bot = bs(body , 'html.parser')
            
            for l in  bot.find_all('a'):
                if l.get("href") !=None:
                    if 'http' in l.get("href"):
                        list_of_links.append(l.get("href"))
                    else:
                        l_2 = f'{self.url_type_1}{l.get("href")}'
                        list_of_links.append(l_2)
            return list_of_links
        
        except Exception as e :
            raise NetworkError(e)
            # or 
            # return '{type_error} : {message}'.format(type_error = 'NetworkError' , message=e )

    def information(self):
        """Returns whois information . """
        try:
            if '.ir' in self.url :
                domain_to_ip = socket.gethostbyname(self.url_type_2)
                self.finall_url = f"https://www.whois.com/whois/{domain_to_ip}"
                request=requests.get(self.finall_url)
                data = request.text
                bot = bs(data,"html.parser")
                information = bot.find("pre",id=tkn['.ir']).text
            elif ".com" in self.url  or '.net' in self.url :
                self.finall_url = f"https://www.whois.com/whois/{self.url_type_1}"
                request = requests.get(self.finall_url)
                data = request.text 
                bot = bs(data , 'html.parser')
                information = bot.find('pre' , id=tkn['.com']).text
            elif '.org' in self.url :
                self.finall_url = f"https://www.whois.com/whois/{self.url_type_1}"
                request=requests.get(self.finall_url)
                data = request.text
                bot = bs(data,"html.parser")
                information = bot.find("pre",id=tkn['.org']).text
            else:
                enc_0_1 = ascii_uppercase[3].lower()
                enc_0_2 = ascii_uppercase[5].lower() 
                enc_0_3  = ascii_uppercase[4].lower() 
                enc_0_4 = 180 
                enc_0_5 = 429
                enc_0_6  = 1 
                enc_0_7  = ascii_uppercase[2].lower() 
                sever = f"https://api.whoisfreaks.com/v1.0/whois?apiKey=42{enc_0_1}{enc_0_5}48{enc_0_6}3{enc_0_3}44836894{enc_0_7}6574{enc_0_2}{enc_0_2}41805{enc_0_3}&whois=live&domainName={self.url_type_1}"
                a=requests.get(sever)
                data=a.json()

                information = data

            return information
        except:
                enc_0_1 = ascii_uppercase[3].lower()
                enc_0_2 = ascii_uppercase[5].lower() 
                enc_0_3  = ascii_uppercase[4].lower() 
                enc_0_4 = 180 
                enc_0_5 = 429
                enc_0_6  = 1 
                enc_0_7  = ascii_uppercase[2].lower() 
                sever = f"https://api.whoisfreaks.com/v1.0/whois?apiKey=42{enc_0_1}{enc_0_5}48{enc_0_6}3{enc_0_3}44836894{enc_0_7}6574{enc_0_2}{enc_0_2}41805{enc_0_3}&whois=live&domainName={self.url_type_1}"
                a=requests.get(sever)
                data=a.json()
                information = data
                return information
    def technology(self):
        '''returns the technologies used,'''
        try:
            url="https://whatcms.org/API/Tech?key=wkfidt4wvwn2tklorxmqxxwsfvetiox51gw7ipu7xww8nl2g3a4r4mxjnin6cnoo1jarne&url="+self.url_type_1
            request = requests.get(url)
            return request.json()['results']
        except NetworkError as e :
            return '{type_error} : {message}'.format(type_error = 'NetworkError' , message=e )
        
    def ping(self , mode='mid' , number=4 ):
        """
        types of modes:
        min : Returns the lowest ping
        mid : Returns the average ping
        max : Returns the maximum ping.

        number parameter:
        The number of times to ping the entered address, 
        the higher this value is, the more accurate the obtained ping is, but it takes more time.
        Also, if this value is low (less than 4), the ping it returns may not be accurate.
        
        """ 
        per_pocess = p.ping(self.url_type_2 , count=number)
        pings = str(per_pocess).split("Round Trip Times min/avg/max is ")[1]
        min_ping = pings.split('/')[0]
        average_ping = pings.split('/')[1]
        max_ping = pings.split('/')[2]

        if mode=='min':
            return min_ping
        elif mode =='mid':
            return average_ping
        elif mode== 'max':
            return max_ping
        else:
            raise ModeError("mode can be equal to average or min or max")
        
    def iswordpress(self):
        """Returns true if developed with WordPress; otherwise false"""
        request = requests.get(self.url_type_1)
        body = request.text
        bot = bs(body , 'html.parser')
        html = bot.prettify()
        return 'wp-content'in html
    
    def get_images(self):
        """Returns all image links."""
        list_of_image = list()
        try:
            request = requests.get(self.url_type_1)
            html = request.text
            bot = bs(html , 'html.parser')
            for img in bot.find_all('img'):
                if 'http' in img.get("src"):
                    list_of_image.append(img.get("src"))
                else:
                    img_2 = f'{self.url_type_1}{img.get("src")}'
                    list_of_image.append(img_2)
            return list_of_image
        
        except Exception as en:
            raise NetworkError('\n{message}'.format( message=en ))
        
    def get_videos(self):
        '''Returns all video links.'''
        list_of_videos = list()
        request = requests.get(self.url_type_1)
        body = request.text
        bot = bs(body , 'html.parser')
        for vid in bot.find_all("video"):
            if 'http' in vid:
                list_of_videos.append(vid.get("src"))
            else:
                vid_2 = f'{self.url_type_1}{vid.get("src")}'
                list_of_videos.append(vid_2)
        return list_of_videos
    
    def tag(self, tag:str , attribute:str=None):
        """
        Returns the content inside the desired tag; You can filter the content with attribute.
        Inputs:
        Tag: It is equal to the desired tag name
        attribute: It is equal to the attribute in question
        """
        list_of_contents = list()
        try:
            request = requests.get(self.url_type_1)
            html_code = request.text
            bot = bs(html_code , 'html.parser')
            
            for content in bot.find_all(tag):
                if attribute==None:
                    list_of_contents.append(content)
                else:
                    list_of_contents.append(content.get(attribute))
            return list_of_contents

        except Exception as e :
            raise NetworkError(e)
        
    def isit(self , word:str):
        '''If the given word is inside the url, it will return true, otherwise it will return false.'''
        try:
            request =  requests.get(self.url_type_1)
            content = request.text
            return word in content
        except Exception as e:
            raise NetworkError(e)
        
    def find_file(self , *suffix:str):
        """Returns all desired files."""
        list_of_file = []
        request = requests.get(self.url_type_1)
        body = request.text
        bot = bs(body , 'html.parser')
        for suf in suffix:
            for  file_link in bot.find_all("a"):
                link  = file_link.get("href")
                if link !=None : 
                    if suf in link:
                        if 'http' not in link:
                            link_2 = f"{self.url_type_1}/{link}"
                            list_of_file.append(link_2)
                        else:
                            list_of_file.append(link)

        return list_of_file


    def social(self ):
        """Returns the address of social networks"""
        social_network = {
            "mailto" :    None , 
            "tel" :       None , 
            "instagram" : None ,  
            'linkedin' :  None , 
            "tg":         None , 
            "telegram":   None , 
            "twitter" :   None , 
            "youtube" :   None ,  
            "facebook":   None , 
            "rubika" :    None , 
            "aparat" :    None ,  
            'Pinterest' : None , 
            "WhatsApp" :  None , 
            "Discord" :   None ,  
            "github" :    None ,  
        }
        start =set_url(self.url)
        try:
            links=start.get_links()
        except Exception as e:
            raise NetworkError(e)

        for link in links:
            for network in social_network:
                if network in link:
                    social_network[network]=link

        social_network_with_link = {}
        for l,s in social_network.items():
            if s!=None:
                social_network_with_link[l]=s
        
        # return social_network_with_link
        if social_network_with_link == {}:
            if '/' in self.url_type_2:
                domain  = self.url_type_2.split("/")[0]
            domain = self.url_type_2
            start =set_url(domain)
            links=start.get_links()

            for link in links:
                for network in social_network:
                    if network in link:
                        social_network[network]=link

            social_network_with_link = {}
            for l,s in social_network.items():
                if s!=None:
                    social_network_with_link[l]=s
        
        return social_network_with_link

    


"""
             _   _                     
 _ __  _   _| |_| |__   ___  _ __      
| '_ \| | | | __| '_ \ / _ \| '_ \     
| |_) | |_| | |_| | | | (_) | | | |    
| .__/ \__, |\__|_| |_|\___/|_| |_|    
|_|__  |___/  ___| | ____ _  __ _  ___ 
| '_ \ / _` |/ __| |/ / _` |/ _` |/ _ \
| |_) | (_| | (__|   < (_| | (_| |  __/
| .__/ \__,_|\___|_|\_\__,_|\__, |\___|
|_|                         |___/
"""
#the end .
