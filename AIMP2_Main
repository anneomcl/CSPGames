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


def graphColor(adjMatrix, colorNum, colorList, vertNum, vert, total):
    if vert == vertNum:
        return True

    for c in range(1, colorNum+1):
        if checkColor(vert, adjMatrix, colorList, c, vertNum)== True:
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


def graphColor2(adjMatrix, colorNum, colorList, vertNum, vert, sortedVertList, total):
    if vert == vertNum:
        return True

    for c in range(1, colorNum+1):
        if checkColor(sortedVertList[vert][0], adjMatrix, colorList, c, vertNum)== True:
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


    with PdfPages('multipage_pdf2'+str(num)+'.pdf') as pdf:
        for elem in graph[1]:
            listX.append(elem[0])
            listY.append(elem[1])
        lines = graph[0]
            #[[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
        lc = mc.LineCollection(lines, linewidths=.2)
        fig, ax = pl.subplots()
        ax.add_collection(lc)
        #pl.plot(listX, listY, [1, 0])
        pl.scatter(listX, listY, s=100, c=colormap[categories])
        #pl.axis([-1, 4, -1, 4])
        pl.axis([-.1, 1.1, -.1, 1.1])
        #pl.show()
        pl.title('Page One')
        pdf.savefig()
        pl.close()

        d = pdf.infodict()
        d['Title'] = 'Multipage PDF Example'
        d['Author'] = u'Jouni K. Sepp\xe4nen'
        d['Subject'] = 'How to create a multipage pdf file and set its metadata'
        d['Keywords'] = 'PdfPages multipage keywords author title subject'


    return

def reportGenerator(N, num):
    graph=list(graphGenerator(N))
    adjMatrix=list(AdjMatrixBuilder(graph))
    sortedVertList=list(reversed(sorted(MRVHeursitc(adjMatrix), key=operator.itemgetter(1))))

    colorList=[]
    start = timeit.default_timer()
    #colorList=mainSolutionA(adjMatrix, N, 4)
    #colorList=mainSolutionB(adjMatrix, N, 4, sortedVertList)

    mainSolutionA(adjMatrix, N, 4)
    stop = timeit.default_timer()
    A=stop - start

    start = timeit.default_timer()
    #colorList=mainSolutionA(adjMatrix, N, 4)
    #colorList=mainSolutionB(adjMatrix, N, 4, sortedVertList)

    colorList=mainSolutionB(adjMatrix, N, 4, sortedVertList)
    stop = timeit.default_timer()
    B=stop - start
    #plotter(colorList, graph, num)
    return (A,B)
    # vert=0
    # for elem in colorList:
    #
    #     if checkColor(vert, adjMatrix, colorList, elem, N)== False:
    #         print("FAILED")
    #         break
    #     vert=vert+1


def reportRunner(R, N):
    A=0
    B=0
    for x in range(1, R):
        #print(x)
        A=A+reportGenerator(N, x)[0]
        B=B+reportGenerator(N, x)[1]

    print(A/R)
    print(B/R)


for x in range(3, 25):
    string="------- the average runtimes for "+str(x)
    print(string)
    reportRunner(70, x)


