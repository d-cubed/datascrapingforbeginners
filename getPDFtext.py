#! /usr/bin/python
import pdfplumber
import sys

print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of a pdf to extract the text from!")
    sys.exit()
else:
    pdf = pdfplumber.open(sys.argv[1])

print(str(sys.argv[1]) + " has %s pages. " % str(len(pdf.pages)))

#we use this to eyeball the boundingbox
for p in range(1,2):
    tp = pdf.pages[p]
    print("The width of page " + str(p) + " is " + str(tp.width))
    print("The height of page " + str(p) + " is " + str(tp.height))

#Note it's expecting a tuple i.e. () in ()
#(x0, top, x1, bottom)
#this range is just to trim off watermark text - ymmv
## wrt .encode() 50K causes and solutions to this problem
filename = str(sys.argv[1]+".txt")

with open(filename, "w") as textdump:
    for p in range (0,len(pdf.pages)):
        tp = pdf.pages[p]
        sys.stdout.write('\r'+"Currently processing page " + str(p))
        sys.stdout.flush()
        if tp.within_bbox((20,20,540,660)).extract_text():
            thetext = tp.within_bbox((20,20,540,660)).extract_text().encode('utf-8')
            textdump.write(thetext)
        else:
            print("\n No text found on page " + str(p) )

print("The text extraction is complete.")
