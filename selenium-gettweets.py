#! /usr/bin/python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()


print ("You are currently running Selenium to scrape a webpage")



#vvv  This is the code to load tweets from a website
url = "https://twitter.com/CASTtechSchool"
print("Reading in %s" % url)

#r=requests.get(url)
#soup=BeautifulSoup(r.text, 'html.parser')
#^^^^ This would be used on a network where you could access Twitter
browser.get(url)
time.sleep(2)

body = browser.find_element_by_tag_name('body')

body.send_keys(Keys.ESCAPE)

for _ in range(100):
    body.send_keys(Keys.PAGE_DOWN)
    print("just paged down")
    time.sleep(1)


with open("selct.html", "w") as f:
    f.write(browser.page_source)
