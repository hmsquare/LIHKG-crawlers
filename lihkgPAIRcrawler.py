""" LIHKG CRAWL """
#!pip install selenium
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

##################### CRAWL FORUMS #####################
driver = webdriver.Chrome('whereever webdriver is in your PC')

# reference: https://towardsdatascience.com/scraping-multiple-urls-with-python-tutorial-2b74432d085f
""" function to get list of replies """
def crawler(link):
    pairs = []
    l = link[:-1]
    #scrape the first n pages of the topic (11,16,21,26,31,36,41)
    for i in range(1,41):
        wp = l + str(i)
        driver.implicitly_wait(10)
        driver.get(wp)
        sleep(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        comments = soup.find_all('div', class_="GAagiRXJU88Nul1M7Ai0H")
        
        quoted, reply = "", ""       
        
        for comment in comments:
            reply = comment.find('div', class_="_2cNsJna0_hV8tdMj3X6_gJ").text
            
            #print(comment)
            quotedContent = comment.find('blockquote', class_="_31B9lsqlMMdzv-FSYUkXeV")
            if quotedContent != None:
                allquotes = quotedContent.findChildren('div')
                if len(allquotes) >1:
                    quoted = allquotes[-1].text
                else:
                    quoted = quotedContent.text
            else:
                quoted = "--"
            
            if "顯示更多" in quoted:
                quoted = quoted.replace("顯示更多", '')
            if "顯示 #1" in quoted:
                quoted = quoted.replace("顯示 #1", '')
                
            pairs.append((quoted,reply))
        #print(pairs)
    return pairs # a list of quote-reply pairs

#""" CHANGE FN FOR LINKS """
urlist = ["list of lihkg links as seen in example in line 55"]
comments = [c for line in urlist for c in crawler(line.strip()) if c != '']
#comments = crawler('https://lihkg.com/thread/2282219/page/1')
driver.quit()
#print(comments)

##################### STORE TO DATAFRAME #####################
df = pd.DataFrame(comments, columns=["Quote", "Reply"])

#CHANGE FN FOR OUTPUT CSV
df.to_csv('fn', index = False) 


