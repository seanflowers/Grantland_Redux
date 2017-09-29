from bs4 import BeautifulSoup
import re
import urllib2
import praw
import csv
import time

while True:

#Open website and find newest article

    html_Barnwell = urllib2.urlopen('http://search.espn.com/bill-barnwell/')
    soup_Barnwell = BeautifulSoup(html_Barnwell, 'html.parser')
    for link in soup_Barnwell.find_all('a', string="Story" , limit=1):
        kurl = (link.get('href'))

    html_Barnwell2 = urllib2.urlopen(kurl)
    soup_Barnwell2 = BeautifulSoup(html_Barnwell2, "html.parser")   
    headlines = soup_Barnwell2.find_all('header',{"class" : "article-header"},limit=1)
    for ia in headlines :
        ktitle = ia.text

#Open CSV File and check database

    newArt = True
    with open('BarnwellBot.csv','r+ab') as f:
        reader = csv.reader(f)
        for row in reader:
            if [kurl] == row : newArt = False
        if newArt : 
            writer = csv.writer(f)
            writer.writerows([[kurl]])
            print 'BillBarnwellBot: New article! Posting to reddit!'
        
            r = praw.Reddit(user_agent='TestScript')
            r.login('BillBarnwellBot','**********',disable_warning=True)
            r.submit('GrantlandRedux', ktitle, url=kurl)
        else :
            print 'BillBarnwellBot: No new article. Going back to sleep.'
            
    time.sleep(14400) #8 hours = 28800 seconds
