__author__ = 'huangb3'
"""
                       ....?$8Z:....... ..+$I .
                     .,.I7II7III777$$O...8O...:I.
                .. ..M$$$$$$$$$$$$$$$$$$O$7.:~~:...
                .. .7ZZ$ZOO8=???+IO$$$$OOO=8~O8887.
             I ,~,.,,I.,,,.,,,..,?~~~+OI,,,,.,~IO?.
          . ,,::=~..,,,,,,,,,,:,,,..:~:,::,,,,::DOO
          .I+,:~:..,,..,,,,,,,.:.,,,,::.....:=:::7,
          $..==...,,,.:,,,,,,.,,,.,,...=:,,,.,,,?:.
        .7,.~?......,.:,,,,,,,,,=,,,,,,.?:~,,,,,::.
        +.,=?,......,I...,,,,,,,,,,,.,,,.::::,,.,:, .
       ..,=I,,... ..?...........,+....,,.,,,~.,,,,:..
       ..~?..,.,,,..,...........:=.,..,,..=.:~,,,,::.
       $,~,:,,,,,~.I,.............,,..,,,,,:,:,,,,,~:
      .7,?~.,,.,,+,:.,,:.,,,,,,,:.=.,,,,,,..,,,:,,,,Z
       :..?.,,,,:+.:.:.~,,,,,,,,+:=+,,.,,,.I,,,:,,,.Z
      . .:+.,,,.:?+,.=,=,,,,,,,,.~I~=,,,,,,I,,,:,,,,?
      . I:?.,,,.?=+:..+~~,,,,..:...O??++...:,,.,.,,,.
        .:=...?~M~:ON.?,~,,,..=MNNNNM,,+,,:,,,,+,,,.
        .=I+,.,,M,DDMNN....:.D88OM.MNN,=.,,,.,?:.....
        ..?~,,..~.M+:.M.....,.:M?I.??+,,,.,,,:,,,~N..
      ..Z.,.:=,....::,=........~=,.,I:,,+,,~:,.,~~:
        ..,.,.~.,~=,..,..........,.,?.,:,.::,.===:I~.
         .,,,,.?:?,,,,..........,:::+::,,,::,:~~~=+=~
        ..,,,,.,?,,,,,.......~..,+=.::==:,:::I~7::$..
            ..,,.+++?~......,.,8=+.::I=+~.::::::::.
            ~..:,++=7~=$~8+?8?7$=D8=+++==.,:~:=.
          .......==+I??II$ZO8O:Z=$I+=++==.,::M
               .,$+~?...ZOO.,..,:~=~==~7..   .
                 ,7.O...,I:~::..8=.+~=.7..
                   .  ..8OD:,:..7..7=+=...
                    ...,.OMZ,~..,.87~+878
                     ...?8O+N,:DOI$8OII$?I .
                      8?D8=+?,+,~II7$7?I$~8.
                     ..7+?MZ.,.,OI,7.,,.$O
                     ...?M+O.$~..,.=,,~:..   .
                       . ?+?=O...,,,.OOODZ....
                         .,7I$,,,.,~$D8OZ?,...
                         ..     ..   .. ..   .

                         Your waifu is shit
"""


import cv2
import math
import numpy

infl = 0
lag = 10
#setting up everything
scanImg = cv2.imread("TestImages/scan.jpg")
greyImg = cv2.cvtColor(scanImg, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(greyImg, [0], None, [256], [0, 256])
print len(hist)
#Display base image
cv2.imshow("Original", greyImg)
signal = numpy.zeros(256)
#Read in Histogram array outputs peak Array, 1

def calcMean(arr):
    mean = 0
    for x in arr:
        x = int(x)
        mean += x
    mean = mean/256
    return mean

def calcSD(arr,mean):
    sd = 0
    for x in arr:
        sd += (x - mean)**2
    sd /= 255
    sd = math.sqrt(sd)
    return sd

# is POI
#poi means poi and i aint going to explain shit to you poi
def poi(hist, mean, Stdev, lag):
    global signal
    for i in range(len(hist)):
        if i > lag:
            oldmean = mean
            if hist[i] > ((mean + infl * Stdev)/(1+infl)):
                mean = (oldmean + infl * hist[i]) / (1+infl)
                Stdev = (Stdev + infl * math.sqrt((hist[i] - oldmean)**2)) / (1+infl)
                signal[i] = 1
                if hist[i] > 1.2 * ((mean + infl * Stdev)/(1+infl)):
                    signal[i] = 2
            else:
                mean = (oldmean + hist[i]) / 2
                Stdev = (Stdev + math.sqrt((hist[i] - oldmean) ** 2)) / 2
                signal[i] = 0
        if i < lag:
            print "wee."

def humpScan(signal):
    scnVal = 0
    bflag = 0
    wflag = 0
    for p in range(len(signal)):
        if signal[p] == 0:
            scnVal += 1
        else:
            bflag = int(scnVal)
    scnVal = 255
    for p in range(len(signal)):
        if signal[255-p] == 0:
            scnVal -= 1
        else:
            wflag = int(scnVal)
    print bflag
    print wflag
    return bflag, wflag
#get fuked boy 2  2
#THIS IS TESTING GAMMA CORRECTION BS W/ A LOOKUP TABLE
"""
def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = numpy.array([((i / 255.0) ** invGamma) * 255
                         for i in numpy.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

gamma = gamma if gamma > 0 else 0.1
adjusted = adjust_gamma(original, gamma=gamma)
cv2.putText(adjusted, "g={}".format(gamma), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
cv2.imshow("Images", numpy.hstack([original, adjusted]))
cv2.waitKey(0)
"""
#END OF TEST CODE DO NOT RUN THIS SHIT

dankmemes = cv2.equalizeHist( greyImg)
cv2.imshow("image", dankmemes)

#def eq(signal, )



print hist
tempMean = calcMean(hist[0:lag])
tempSd = calcSD(hist[0:lag], tempMean)
print "mean",tempMean
print "standard dev", tempSd
poi(hist, tempMean, tempSd, lag)


bcutoff = int(0)
wcutoff = int(0)
bcutoff, wcutoff = humpScan(signal)

#Errors: it's cutting off grey areas, I need to preserve the gray and instead do it for whites.
res, testimg = cv2.threshold(greyImg, (bcutoff/1.5), 255, cv2.THRESH_TOZERO)
res, ndstep = cv2.threshold(testimg, (255-(wcutoff/4)), 255, cv2.THRESH_BINARY)
ndstep = cv2.bitwise_or(ndstep, testimg)

dunzo = cv2.calcHist(ndstep, [0], None, [256], [0, 256])
print dunzo

cv2.imshow("testing2222", testimg)
cv2.imshow("whiteimg", ndstep)
cv2.waitKey(0)

"""for x in range(len(signal)):
    hist[x] = signal[x]
print hist"""
print signal