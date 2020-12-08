""" LIHKG CRAWL """
#!pip install selenium
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

##################### CRAWL FORUMS #####################
driver = webdriver.Chrome('directory of chromedriver in your PC')

# reference: https://towardsdatascience.com/scraping-multiple-urls-with-python-tutorial-2b74432d085f
""" function to get list of replies """
def crawler(link):
    titles = []
    driver.implicitly_wait(10)
    driver.get(link)
    sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    #comments = soup.find_all('div', class_="_2cNsJna0_hV8tdMj3X6_gJ")
    title = soup.find('div', class_="CrheYfsiQFY-vLMnO378W").text
    titles.append((link, title))    
        
    return titles # a list of quote-reply pairs

#""" CHANGE FN FOR LINKS """
urlist = ["list of lihkg links as in the format in line 29"]
ti = [c for line in urlist for c in crawler(line.strip()) if c != '']
#ti = crawler('https://lihkg.com/thread/2282219/page/1')

driver.quit()
#print(ti)

##################### STORE TO DATAFRAME #####################
df = pd.DataFrame(ti, columns=["Link", "Title"])

#CHANGE FN FOR OUTPUT CSV
df.to_csv('fn', index = False) 



