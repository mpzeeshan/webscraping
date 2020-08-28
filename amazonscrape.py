'''
This program exracts data from amazon search result and dumps results into a json file as output The program is written to be executed in python3 enviroment
dependencies/required packages: BeautifulSoup
                                requests
                                re
                                json 
'''

class my_class:
    def __init__(self,url,soup,clean,s_containers,l_containers,userInput):
        self.url = url
        self.soup = soup
        self.clean = clean
        self.s_containers = s_containers
        self.l_containers = l_containers
        self.userInput = userInput
        
        
    # this method grabs the number of pages from the intial search page result
    def get_pageNos(self):
        page_nos = 0
        for line in soup.findAll('li', attrs={'class':'a-disabled'}):
            page_nos = re.sub(clean,'',str(line))
        return page_nos

    # this method stores all the html content by searching specific div elements
    def store_content(self):
        for container in soup.findAll('div', attrs={'class':'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32'}):
            s_containers.append(container)
        for container in soup.findAll('div', attrs={'class':'a-section a-spacing-medium'}):
            l_containers.append(container)

    # this method uses BeautifulSoup's html parser to get content from the provided url    
    def get_content(self,headers, ur):
        getRequest = requests.get( ur, headers = headers)
        content = getRequest.content
        soup1 = bs(content, features = 'html.parser')
        return soup1

    # this method is used to extract required specific data and is stored into fields   
    def scrap_data(self,containers1,containers2): 
        if len(containers1) != 0:
            for item in range(len(containers1)):
                try:
                    s_rating = re.sub(clean,'',str(containers1[item].div.i.span))   
                    s_desc = re.sub(clean,'',str(containers1[item].div.h2.span))    
                    s_brand = re.sub(clean,'',str(containers1[item].div.h5)) 
                    s_brand = ' '.join(s_brand.split())
                    if s_brand == 'None':
                        s_brand = s_desc.split(' ')[0]+s_desc.split(' ')[1]
                    s_price = re.sub(clean,'',str(containers1[item].find('span', attrs={'class':'a-price'}))) 
                    s_price = s_price[:len(s_price)//2]
    
                    jsonObject = {'Brand': s_brand, 'Desc': s_desc , 'Ratings': s_rating , 'Price': s_price}
                    # fileobj.write(json.dumps(jsonObject,ensure_ascii=False))
                    # fileobj.write('\n')
                    print(jsonObject)
                except AttributeError as ae:
                    pass
        elif len(containers2) != 0:
            for item in range(len(containers2)):
                try:
                    l_desc = re.sub(clean,'',str(containers2[item].h2.span))    
                    try:
                        l_brand = l_desc.split(' ')[0]+l_desc.split(' ')[1]  
                    except IndexError as ie:
                        pass
                    l_rating = re.sub(clean,'',str(containers2[item].i.span))    
                    l_price = str(containers2[item].find('span', attrs={'class':'a-offscreen'})) 
                    l_price = re.sub(clean, '',l_price)
                    
                    jsonObject = {'Brand': l_brand, 'Desc': l_desc , 'Ratings': l_rating , 'Price': l_price}
                    # fileobj.write(json.dumps(jsonObject,ensure_ascii=False))
                    # fileobj.write('\n')
                    print(jsonObject)
                except AttributeError as AE:
                    pass

    # this method is used to check if the search result has no items retrieved and if executed fully exits the program
    def result_check(self,soup):
        for result in self.soup.findAll('div',attrs={'class':'sg-col-20-of-24 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-8-of-12 sg-col-12-of-16 sg-col-24-of-28'}):
            if 'No results for' in str(result):
                print('No results for:{}'.format(userInput.replace('+',' ')))
                print('no result')
                exit()
    def functions(page_nos):    
        for i in range(page_nos+1)[2::1]:
            soup = first_obj.get_content(headers,'https://www.amazon.in/s?k={userInput}&page={page_no}'.format(userInput= userInput,page_no=i))
            first_obj.s_containers, first_obj.l_containers= [],[]
            first_obj.store_content()
            first_obj.scrap_data(s_containers,l_containers)

#############################################################################################################################################
##                                      Execution starts here                                                                              ##
#############################################################################################################################################
import requests, re, json, threading
from bs4 import BeautifulSoup as bs

s_containers, l_containers = [],[]
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
clean = re.compile('<.*?>')                
soup = bs(features='html.parser')                       #creating a variable of type BeautifulSoup html parser   

userInput = str(input('Enter Your Search Here:'))
userInput = " ".join(userInput.split())                 #removing whitespaces if any at the beginning or the end of the string and joining substtrings with one whitespace in between
userInput = str(userInput.replace(' ','+'))             #replacing whitespace with '+'

url = 'https://www.amazon.in/s?k={userInput}&ref=nb_sb_noss_2'.format(userInput= userInput)

first_obj = my_class(url,soup,clean,s_containers,l_containers,userInput)

soup = first_obj.get_content(headers, url)
first_obj.result_check(soup)
page_nos=int(first_obj.get_pageNos())
first_obj.store_content()
# # fileob=open('scraped.json','w')                         #opening the file for the intial time in write mode to clear content if any content is present already
# # fileob.close()
# # fileobj=open('scraped.json','a')
first_obj.scrap_data(s_containers,l_containers)  
functions(page_nos)
# fileobj.close()
