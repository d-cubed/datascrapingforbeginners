#! /usr/bin/python3
##import matplotlib.pyplot as plt
import sys
import requests
from bs4 import BeautifulSoup
import ssl
from requests.utils import DEFAULT_CA_BUNDLE_PATH;
#openssl x509 -in cert.crt -out cert.pem

#print(DEFAULT_CA_BUNDLE_PATH)

# This restores the same behavior as before.
context = ssl._create_unverified_context()
requests.packages.urllib3.disable_warnings()

print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of an website to extract the text from!")
    sys.exit()
else:
    url= sys.argv[1]

print("Reading in %s " % str(sys.argv[1]))

#vvv  This is the code to load tweets from a website
#url="https://twitter.com/sometwitterhandle"
#^^^^ This would be used on a network where you could access Twitter


r=requests.get(url,verify=False)
soup=BeautifulSoup(r.text, 'html.parser')

#soup=BeautifulSoup(text, 'html.parser')
#tweets = [p.text for p in soup.findAll('p',class_='tweet-text')]

## ^^^^ it's a list
#print(tweets)

tweets = [p.text for p in soup.findAll('p')]
txt = ' '.join(tweets)

"""
for t in tweets:
    print t
"""

filename = str(sys.argv[1]).split(':')[1]
filename = filename.split('/')[2]
filename = filename.replace('.','_')

with open(filename, "w") as f:
    for t in tweets:
        f.write(t+'\n')

"""
# this code is purposefully left here commented out
# use to test your images
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()
"""

print ("Finished writing %s" % (filename))
sys.exit()
