import cv2
import numpy as np
import opFlowOfBlocks as roi
import math

def getThresholdDistance(mag,blockSize):
    return mag*blockSize

def getThresholdAngle(ang):
    tAngle = float(math.pi)/2
    return ang+tAngle,ang-tAngle

def getCentreOfBlock(blck1Indx,blck2Indx,centreOfBlocks):
    x1 = centreOfBlocks[blck1Indx[0]][blck1Indx[1]][0]
    y1 = centreOfBlocks[blck1Indx[0]][blck1Indx[1]][1]
    x2 = centreOfBlocks[blck2Indx[0]][blck2Indx[1]][0]
    y2 = centreOfBlocks[blck2Indx[0]][blck2Indx[1]][1]
    slope = float(y2-y1)/(x2-x1) if (x1 != x2) else float("inf")
    return (x1,y1),(x2,y2),slope


def calcEuclideanDist((x1,y1),(x2,y2)):
    dist = float(((x2-x1)**2 + (y2-y1)**2)**0.5)
    return dist
    
def angleBtw2Blocks(ang1,ang2):
    if(ang1-ang2 < 0):
        ang1InDeg = math.degrees(ang1)
        ang2InDeg = math.degrees(ang2)
        return math.radians(360 - (ang1InDeg-ang2InDeg))
    return ang1 - ang2

def motionInMapGenerator(opFlowOfBlocks,blockSize,centreOfBlocks,xBlockSize,yBlockSize):
    global frameNo
    motionInfVal = np.zeros((xBlockSize,yBlockSize,8))
    for index,value in np.ndenumerate(opFlowOfBlocks[...,0]):
        Td = getThresholdDistance(opFlowOfBlocks[index[0]][index[1]][0],blockSize)
        k = opFlowOfBlocks[index[0]][index[1]][1]
        posFi, negFi =  getThresholdAngle(math.radians(45*(k)))
        
        for ind,val in np.ndenumerate(opFlowOfBlocks[...,0]):
            if(index != ind):
                (x1,y1),(x2,y2), slope = getCentreOfBlock(index,ind,centreOfBlocks)
                euclideanDist = calcEuclideanDist((x1,y1),(x2,y2))
        
                if(euclideanDist < Td):
                    angWithXAxis = math.atan(slope)
                    angBtwTwoBlocks = angleBtw2Blocks(math.radians(45*(k)),angWithXAxis)
        
                    if(negFi < angBtwTwoBlocks and angBtwTwoBlocks < posFi):
                        motionInfVal[ind[0]][ind[1]][int(opFlowOfBlocks[index[0]][index[1]][1])] += math.exp(-1*(float(euclideanDist)/opFlowOfBlocks[index[0]][index[1]][0]))
    #print("Frame number ", frameNo)
    frameNo += 1
    return motionInfVal


def getMotionInfuenceMap(vid):
    global frameNo
    
    frameNo = 0
    cap = cv2.VideoCapture(vid)
    ret, frame1 = cap.read()
    rows, cols = frame1.shape[0], frame1.shape[1]
    print(rows,cols)
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    motionInfOfFrames = []
    count = 0
    while 1:
        '''
        #if(count <= 475 or (count > 623 and count <= 1300)):
        if(count < 475):
            ret, frame2 = cap.read()
            prvs = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
            count += 1
            continue
        '''
        
        #if((count < 1451 and count <= 623)):
        '''
        if(count < 475):    
            ret, frame2 = cap.read()
            prvs = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
            count += 1
            continue
        '''
        print(count)
        ret, frame2 = cap.read()
        if (ret == False):
            break
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
       
        
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        
        
        prvs = next
        opFlowOfBlocks,noOfRowInBlock,noOfColInBlock,blockSize,centreOfBlocks,xBlockSize,yBlockSize = roi.calcOptFlowOfBlocks(mag,ang,next)
        motionInfVal = motionInMapGenerator(opFlowOfBlocks,blockSize,centreOfBlocks,xBlockSize,yBlockSize)
        motionInfOfFrames.append(motionInfVal)
        
        #if(count == 622):
        #    break
        count += 1
    return motionInfOfFrames, xBlockSize,yBlockSize
