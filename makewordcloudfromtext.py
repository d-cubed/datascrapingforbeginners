#! /usr/bin/python
# for more examples of word clouds in Python see:
# https://python-graph-gallery.com/wordcloud/
# https://github.com/amueller/word_cloud
# https://www.datacamp.com/community/tutorials/wordcloud-python


from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys

print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of a textfile to extract the text from!")
    sys.exit()
else:
    text = open(sys.argv[1],"r")

print("Reading in %s " % str(sys.argv[1]))

txt = text.read()

wordcloud = WordCloud(width=480, height=480, margin=0).generate(txt)

pngname = str(sys.argv[1]).split('.')[0] + ".png"
print("Creating file " + pngname)
wordcloud.to_file(pngname)

"""
# this code is purposefully left here commented out
# use to test your images
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()
"""
