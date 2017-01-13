import urllib.request
import re
import django.http
import matplotlib.dates as dat
import matplotlib.pyplot as plt
import datetime as dt

monthDict = dict()
monthDict['Jan']=1
monthDict['Feb']=2
monthDict['Mar']=3
monthDict['Apr']=4
monthDict['May']=5
monthDict['Jun']=6
monthDict['Jul']=7
monthDict['Aug']=8
monthDict['Sep']=9
monthDict['Oct']=10
monthDict['Nov']=11
monthDict['Dec']=12

bigDic = dict()
dryDic = dict()
ascDic = dict()
seisDic = dict()
noxDic = dict()
bigDic[0]=dryDic
bigDic[1]=ascDic
bigDic[2]=seisDic
bigDic[3]=noxDic
dryDic[0]="Main-hand Drygore Longsword"
dryDic[1]="Main-hand Drygore Mace"
dryDic[2]="Main-hand Drygore Rapier"
dryDic[3]="Off-hand Drygore Longsword"
dryDic[4]="Off-hand Drygore Mace"
dryDic[5]="Off-hand Drygore Rapier"
ascDic[0]="Main-hand Ascension Crossbow"
ascDic[1]="Off-hand Ascension Crossbow"
seisDic[0]="Seismic Wand"
seisDic[1]="Seismic Singularity"
noxDic[0]="Noxious Scythe"
noxDic[1]="Noxious Staff"
noxDic[2]="Noxious Longbow"
# pages = 1
## Here, enter the most recent forum page. If you want to read a whole thread,
## iterate through the pages of the thread and store price data.

# url = "http://secure.runescape.com/m=forum/forums.ws?17,18,853,65786728,goto,"+str(pages)
# file = urllib.request.urlopen(target_url)

#   gather(url : str,pages : int,file : str): writes the strings written as
#       "int/.../int" into the given file from all of the pages in pages,
#       using the url provided as input

def gather(url, pages):
    lst = [[[],[],[],[],[],[]],[[],[]],[[],[]],[[],[],[]]]
    dateTimeLst = []
    for page in range(pages-1):#i=0,1,2,3,...,pages
        (priceLst,timeLst) = scanPage(url+str(page+1))
        sortLines(priceLst,lst)
        for item in timeLst:
            dateTimeLst.append(item)
    return (lst,dateTimeLst)

'''
scanPage(url) = (priceLst, timeLst), where priceLst consists of nested lists containing
    the price updates from the given url, and
    timeLst consists of the date and time of the prices in priceLst
'''

def scanPage(url):
    file = urllib.request.urlopen(url)
    django.http.HttpResponse.flush(file)
    priceLst = []
    timeLst = []
    flag = -1
    for line in file.readlines():   #read the lines of the given page of the thread
        flag += -1
        if line[0:31] == b"<span class=\"forum-post__body\">":
            m = re.findall('[0-9]+[\.,0-9]*[bsBS/\*]+[0-9]+[\.,0-9\*]*[bsBS\*]*/*[0-9]+[\.,0-9bsBS\*]*/*',str(line))
            #19-Aug-2016 09:15:57
            if len(m)>4:
                for item in m:
                    priceLst.append(item.replace(',','.'))   #converts EU decimal values to US
                if len(m)>0:
                    flag = 2
        if flag == 0:
            if line[0:11] != b'<p class="f':
                flag = 1
                continue
            m = re.findall('[0-9]+[\-A-z]+[0-9]+ [0-9][0-9]:[0-9][0-9]',str(line))
            time = m[0]
            day = int(time[:2])
            year = int(time[7:11])
            month = int(monthDict[time[3:6]])
            hour = int(time[12:14])
            minute = int(time[15:17])
            date = dat.date2num(dt.datetime(year,month,day,hour,minute))
            timeLst.append(date)
        #Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    file.close()
    return (priceLst, timeLst)


    
""" sortLines(lst1, lst2) = lst', where lst' is a list of lists containing prices for each item.
    lst'[0][x]: = drygores, where x represents different drygores.
    lst'[1][x]: = ascension x=0=mh;x=1=oh
    lst'[2][x]: = seismic x=0=mh;x=1=oh
    lst'[3][x]: = noxious

    lst' contains 4 lists, one for lists of drygore prices, one for lists of asc, etc.
"""
def sortLines(lst1,lst2):
    for item in lst1:
        m = re.findall('[0-9\.]+',item)
        if float(m[0])<40.0:
            continue
        elif float(m[0])<100.0:       #ascensions
            lst2[1][0].append(float(m[0]))
            lst2[1][1].append(float(m[1]))
        elif float(m[0])<235.0 and len(m)==2:       #seismic
            lst2[2][0].append(float(m[0]))
            lst2[2][1].append(float(m[1]))
        elif len(m)==3 and float(m[0])<700:       #noxious
            lst2[3][0].append(float(m[0]))
            lst2[3][1].append(float(m[1]))
            lst2[3][2].append(float(m[2]))
    return lst2

''' plotItem(num1 : int, num2 : int, lst : Lines list) plots the prices for an item on a graph

    key:
    0,0 - dry mh long
    0,1 - dry mh mace
    0,2 - dry mh rapier
    0,3 - dry oh long
    0,4 - dry oh mace
    0,5 - dry oh rapier
    1,0 - mh asc
    1,1 - oh asc
    2,0 - mh seis
    2,1 - oh seis
    3,0 - nox scythe
    3,1 - nox staff
    3,2 - nox longbow
'''
def plotItem(num1, num2, priceLst, timeLst):
    plt.figure(figsize=(25,5))
    if len(priceLst[num1][num2]) < len(timeLst):    
        plot = plt.plot_date(timeLst[:len(priceLst[num1][num2])],priceLst[num1][num2],'r-',xdate=True,ydate=False,aa=False)
    else:
        plot = plt.plot_date(timeLst,priceLst[num1][num2][:len(timeLst)],'r-',xdate=True,ydate=False,aa=False)
    plt.title(bigDic[num1][num2])
    plt.ylabel("Item Value (In Millions)")
    plt.xlabel("Date of Update")
    plt.savefig(bigDic[num1][num2])
    plt.close()

''' saves all of the graphs for seismics, ascensions, and noxious items
    with the filename of the item itself. (NO DRYGORES ATM)
'''
def makeGraphs(baseUrl, pages):
    (priceLst,timeLst) = gather(baseUrl,pages)
    plotItem(1,0,priceLst,timeLst)
    plotItem(1,1,priceLst,timeLst)
    plotItem(2,0,priceLst,timeLst)
    plotItem(2,1,priceLst,timeLst)
    plotItem(3,0,priceLst,timeLst)
    plotItem(3,1,priceLst,timeLst)
    plotItem(3,2,priceLst,timeLst)
    print("Graphs have been saved to the current working directory.\n")
    
    
