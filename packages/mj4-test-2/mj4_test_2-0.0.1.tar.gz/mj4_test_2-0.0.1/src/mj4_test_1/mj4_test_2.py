
# test 


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
 
class pp:
    '''By using the pp class, you can retrieve important information from a URL.
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
        return f'This is an object with input {self.url} of class pp'
    
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
        
    
