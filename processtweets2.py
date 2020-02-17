#! /usr/bin/python3
from wordcloud import WordCloud,STOPWORDS
##import matplotlib.pyplot as plt
import sys
import requests
from bs4 import BeautifulSoup


print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of an html file to extract the text from!")
    sys.exit()
else:
    text = open(sys.argv[1],"r")

print("Reading in %s " % str(sys.argv[1]))

#vvv  This is the code to load tweets from a website
#url="https://twitter.com/sometwiiterhandle"
#r=requests.get(url)
#soup=BeautifulSoup(r.text, 'html.parser')
#^^^^ This would be used on a network where you could access Twitter

soup=BeautifulSoup(text, 'html.parser')

#tweets = [p.text for p in soup.findAll('p',class_='tweet-text')]
#print(type(tweets))
## ^^^^ it's a list
#print(tweets)

tweets = [p.text for p in soup.findAll('p')]
txt = ' '.join(tweets)
stop_words = ["https", "co", "RT"] + list(STOPWORDS)

wordcloud = WordCloud(stopwords=stop_words, width=480, height=480, margin=0).generate(txt)

pngname = "CT_tweets.png"
print("Creating file " + pngname)
wordcloud.to_file(pngname)

with open('bestfilename.txt','w') as f:
    for t in tweets:
        f.write(t+"\n")
"""
for t in tweets:
    print t
"""

"""
# this code is purposefully left here commented out
# use to test your images
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()
"""
