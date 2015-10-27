import math
import operator
import random
import numpy as np
import pylab as pl
from matplotlib import collections  as mc
import timeit
from matplotlib.backends.backend_pdf import PdfPages


def pointGenerator(N):
    size = N
    pointsList = []

    for x in range(1, N + 1):
        pointsList.append((random.random(), random.random()))
    return pointsList


def pointDistance(pointA, pointB):
    return math.sqrt(pow(pointA[0] - pointB[0], 2) + pow(pointA[1] - pointB[1], 2))


def getNearestPoints(point, pointsList):
    sortedPointList = []
    retList = []
    for point2 in pointsList:
        sortedPointList.append(point2 + (pointDistance(point, point2),))
    for elem in sorted(sortedPointList, key=operator.itemgetter(2)):
        retList.append((elem[0], elem[1]))
    return retList


def pointCheck(point1, point2, point3):
    if point2[0] <= max(point1[0], point3[0]) and \
                    point2[0] >= min(point1[0], point3[0]) and \
                    point2[1] <= max(point1[1], point3[1]) and \
                    point2[1] >= min(point1[1], point3[1]):
        return True
    else:
        return False


def slope(p1, q1):
    if ((q1[0] - p1[0]) == 0):
        if(q1[1] - p1[1] > 0):
            return 'up'
        else:
            return 'down'
    else:
        return ((q1[1] - p1[1]) / (q1[0] - p1[0]))

def direction(point1, point2, point3):
    dir = (point2[1] - point1[1]) * (point3[0] - point2[0]) - (point2[0] - point1[0]) * (point3[1] - point2[1])

    if dir == 0:
        return 0
    elif dir > 0:
        return 1
    else:
        return 2


def unitVector(p1,p2):
    vector=[p2[0]-p1[0], p2[1]-p1[1]]
    mag=math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
    return [vector[0]/mag, vector[1]/mag]


def intersectionCheck(p1, q1, p2, q2):
    if p1 == p2:
        if unitVector(p1, q1) == unitVector(p2, q2):
            return True
        else:
            return False

    if p1 == q2:
        if unitVector(p1, q1) == unitVector(q2, p2):
            return True
        else:
            return False

    if q1 == p2:
        if unitVector(q1, p1) == unitVector(p2, q2):
            return True
        else:
            return False

    if q1 == q2:
        if unitVector(q1, p1) == unitVector(q2, p2):
            return True
        else:
            return False

    o1 = direction(p1, q1, p2)
    o2 = direction(p1, q1, q2)
    o3 = direction(p2, q2, p1)
    o4 = direction(p2, q2, q1)

    if (o1 != o2 and o3 != o4):
        return True

    if (o1 == 0 and pointCheck(p1, p2, q1)):
        return True

    if (o2 == 0 and pointCheck(p1, q2, q1)):
        return True

    if (o3 == 0 and pointCheck(p2, p1, q2)):
        return True

    if (o4 == 0 and pointCheck(p2, q1, q2)):
        return True

    return False


#print(unitVector((3,5),(5,8)))
#print(intersectionCheck((2, 2), (1, 1), (2, 2), (0, 0)))
# print(pointDistance((0,0), (2,2)))
#
# print(getNearestPoints((0,0),
# [(0,0), (5,1), (100,5), (5,10)]
# ))
#
# print(pointGenerator(10))




def graphGenerator(N):
    edgeList = []
    nodeList = []
    pointsList=pointGenerator(N)
    #pointsList = [(0, 0), (1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]


    for elem in pointsList:
        nearestPoints = getNearestPoints(elem, pointsList)
        nearestPoints = nearestPoints[1:]
        nodeList.append((elem, nearestPoints))


    #print(nodeList)

    while(len(nodeList)>0):

        pointX = random.randint(0, len(nodeList) - 1)

        inter = False
        removeList=[]
        for edge in nodeList[pointX][1]:
            inter = False
            if len(edgeList) != 0:
                for elem2 in edgeList:
                    if intersectionCheck(nodeList[pointX][0], edge, elem2[0], elem2[1]) == True:
                        inter=True
                        removeList.append(edge)
                if inter == False:
                    edgeList.append((nodeList[pointX][0],edge))
                    nodeList[pointX][1].remove(edge)
                    break
            else:
                edgeList.append((nodeList[pointX][0], edge))
                nodeList[pointX][1].remove(edge)
                break
            if len(removeList) != 0:
                for rem in removeList:
                    try:
                        nodeList[pointX][1].remove(rem)
                    except ValueError:
                        pass
                        #print(rem)
                        #print(nodeList[pointX][1])
                removeList=[]
        if len(nodeList[pointX][1]) == 0:
            remove=nodeList[pointX]
            nodeList.remove(nodeList[pointX])




    #print(edgeList)
    return (edgeList, pointsList)



def AdjMatrixBuilder(graphInfo):
    pointsList=list(graphInfo[1])
    edgeList=list(graphInfo[0])
    adjMatrix=[]

    dict={}
    x=0
    for elem in pointsList:
        dict[elem] = x
        x=x+1

    for x in range(0, len(pointsList)):
        adjMatrix.append([])
        for y in range(0, len(pointsList)):
            adjMatrix[x].append(0)

    for elem in edgeList:
        adjMatrix[dict[elem[0]]][dict[elem[1]]]=1
        adjMatrix[dict[elem[1]]][dict[elem[0]]]=1

    #print(pointsList)
    #print(edgeList)
    for elem in adjMatrix:
        #print(elem)
        pass
    return adjMatrix

def checkColor(vert, adjMatrix, colorList, color, vertNum):
    for V in range(0, vertNum):
        if adjMatrix[vert][V]==1 and color == colorList[V]:
            return False
    return True

global counter
counter=0
def graphColor(adjMatrix, colorNum, colorList, vertNum, vert, total):
    global counter
    if vert == vertNum:
        return True

    for c in range(1, colorNum+1):
        if checkColor(vert, adjMatrix, colorList, c, vertNum)== True:
            counter=counter+1
            colorList[vert]=c
            #print(total)
            if graphColor(adjMatrix, colorNum, colorList, vertNum, vert+1, total+1) == True:
                return True
            colorList[vert]=0
    return False

def mainSolutionA(adjMatrix, vertNum, colorNum):
    colorList=[]
    for x in range(0, vertNum):
        colorList.append(0)

    if graphColor(adjMatrix, colorNum, colorList, vertNum, 0, 0)==False:
        print(False)
        return False
    #print(colorList)
    return colorList

def mainSolutionB(adjMatrix, vertNum, colorNum, sortedVertList):
    colorList=[]
    for x in range(0, vertNum):
        colorList.append(0)

    if graphColor2(adjMatrix, colorNum, colorList, vertNum, 0, sortedVertList, 0)==False:
        print(False)
        return False
    #print(colorList)
    return colorList

from copy import deepcopy
from collections import Counter
def graphColor2(adjMatrix, colorNum, colorList, vertNum, vert, sortedVertList, total):
    global counter
    if vert == vertNum:
        return True
    colorIteration=[]


    temp=deepcopy(colorList)
    countedDict=Counter(temp)

    sorted_x = sorted(countedDict.items(), key=operator.itemgetter(1), reverse=True)

    for elem in sorted_x:
        colorIteration.append(elem[0])
    for c in range(1, colorNum+1):
        if c in colorIteration:
            pass
        else:
            colorIteration.append(c)
    colorIteration=reversed(colorIteration)

    for c in colorIteration:
        if checkColor(sortedVertList[vert][0], adjMatrix, colorList, c, vertNum)== True:
            counter=counter+1
            colorList[sortedVertList[vert][0]]=c
            #print(total)
            if graphColor2(adjMatrix, colorNum, colorList, vertNum, vert+1, sortedVertList, total+1) == True:
                return True
            colorList[sortedVertList[vert][0]]=0
    return False


#print(len(graphGenerator(5)[0]))

def MRVHeursitc(adjMatrix):

    sum=0
    index=0
    MRVIndex=[]
    for elem in adjMatrix:
        for elem2 in elem:
            sum=sum+elem2
        MRVIndex.append((index, sum))
        index=index+1
        sum=0

    return MRVIndex


def plotter(colorList, graph, num):
    listX=[]
    listY=[]

    listColors=[]
    for elem in colorList:
        listColors.append(elem -1)
    categories = np.array(listColors)
    colormap = np.array(['r', 'g', 'b', 'c'])



    for elem in graph[1]:
        listX.append(elem[0])
        listY.append(elem[1])
    lines = graph[0]
    with PdfPages('Graph_size_withCheck_'+str(len(listX))+'.pdf') as pdf:
            #[[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
        lc = mc.LineCollection(lines, linewidths=.2)
        fig, ax = pl.subplots()
        ax.add_collection(lc)
        #pl.plot(listX, listY, [1, 0])
        pl.scatter(listX, listY, s=100, c=colormap[categories])
        #pl.axis([-1, 4, -1, 4])
        pl.axis([-.1, 1.1, -.1, 1.1])
        #pl.show()
        pl.title('Graph of vertex size: '+str(len(listX)))
        pdf.savefig()
        pl.close()

        d = pdf.infodict()
        d['Title'] = 'Graphs'
        d['Author'] = u'Jouni K. Sepp\xe4nen'
        d['Subject'] = 'How to create a multipage pdf file and set its metadata'
        d['Keywords'] = 'PdfPages multipage keywords author title subject'


    return

global limit
limit=0


def reportGenerator(N, num):
    global counter
    graph=list(graphGenerator(N))
    adjMatrix=list(AdjMatrixBuilder(graph))
    sortedVertList=list(reversed(sorted(MRVHeursitc(adjMatrix), key=operator.itemgetter(1))))

    colorList=[]
    start = timeit.default_timer()
    counter=0
    colorList2=mainSolutionA(adjMatrix, N, 4)
    CA=counter
    counter=0
    stop = timeit.default_timer()
    A=stop - start

    counter=0
    start = timeit.default_timer()
    colorList=mainSolutionB(adjMatrix, N, 4, sortedVertList)
    CB=counter
    counter=0
    stop = timeit.default_timer()
    B=stop - start


    global limit
    if N==limit:
        pass
    else:
        plotter(colorList2, graph, num)
        limit=N

    # vert=0
    # for elem in colorList:
    #
    #     if checkColor(vert, adjMatrix, colorList, elem, N)== False:
    #         print("FAILED")
    #         person = input('you got rekt: ')
    #     vert=vert+1

    return (A,B, len(graph[0]), CA, CB)

global plotData
plotData=[]
def reportRunner(R, N):
    global plotData

    A=0
    B=0
    E=0
    CA=0
    CB=0
    for x in range(1, R):
        #print(x)
        sthex=reportGenerator(N, x)
        A=A+sthex[0]
        B=B+sthex[1]
        E=E+sthex[2]
        CA=CA+sthex[3]
        CB=CB+sthex[4]
    print('Average Time no forward checking :', A/R)
    print('Average Time with forward checking :', B/R)
    print('Average Number Edges :', E/R)
    print('Average Number of Assignments no forward checking :', CA/R)
    print('Average Number of Assignments with forward checking :', CB/R)
    plotData.append((
            N,
            (A/R),
            (B/R),
            (E/R),
            (CA/R),
            (CB/R)

    ))


for x in range(3, 20):
    string="------- the average runtimes for "+str(x)
    print(string)
    reportRunner(70, x)
a=[] #nodes
b=[] #timeA
c=[] #timeB
d=[] #edges
e=[]
f=[]
for elem in plotData:
    a.append(elem[0])
    b.append(elem[1])
    c.append(elem[2])
    d.append(elem[3])
    e.append(elem[4])
    f.append(elem[5])


# pl.plot(a, b, 'r--',a, c, 'g--')
#
# pl.plot(a, c, 'r--',a, d, 'g--')
#
# pl.plot(a, e, 'r--',a, f, 'g--'15
with PdfPages('GraphColoring_with_additional_LCV_3to20.pdf') as pdf:
    pl.figure()
    pl.plot(a, b, 'r--',a, c, 'g--')
    pl.title('Graph of NODES VS TIME')
    pdf.savefig()  # saves the current figure into a pdf page
    pl.close()

    pl.rc('text', usetex=False)


    pl.plot(a, d, 'g--')
    pl.title('Graph of NODES VS EDGES')
    pdf.savefig()
    pl.close()

    pl.rc('text', usetex=False)

    pl.plot(a, e, 'r--',a, f, 'g--')
    pl.title('Graph of NODES VS ASSIGNMENTS')
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    pl.close()

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = u'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'

    print("DONE")


#
# with PdfPages('PLOTS.pdf') as pdf:
#
#     pl.figure(figsize=(3, 3))
#     pl.plot(a, b, 'r--',a, c, 'g--')
#     pl.title('Graph of NODES VS TIME')
#     pl.savefig()
#     pl.close()
#
#     pl.plot(a, c, 'r--',a, d, 'g--')
#     pl.title('Graph of EDGES VS TIME')
#     pl.savefig()
#     pl.close()
#
#     pl.plot(a, e, 'r--',a, f, 'g--')
#     pl.title('Graph of ASSIGNMENTS VS TIME')
#     pl.savefig()
#     pl.close()
#
#     d = pdf.infodict()
#     d['Title'] = 'Graphs'
#     d['Author'] = u'Jouni K. Sepp\xe4nen'
#     d['Subject'] = 'How to create a multipage pdf file and set its metadata'
#     d['Keywords'] = 'PdfPages multipage keywords author title subject'
