import cv2
import numpy as np
import math

def calcOptFlowOfBlocks(mag,angle,grayImg):
    '''Takes an image (gray scale) and a flow matrix as input. Divides image into blocks and calculates Optical Flow of each block '''
    '''calculate number of rows and columns in the matrix of the image'''
    rows = grayImg.shape[0]
    cols = grayImg.shape[1]
    noOfRowInBlock = 20
    noOfColInBlock = 20
    ''' calculate the number of rows of blocks and columns of blocks in the frame '''
    xBlockSize = rows / noOfRowInBlock
    yBlockSize = cols / noOfColInBlock
    '''To calculate the optical flow of each block'''

    '''declare an array initialized to 0 of the size of the number of blocks'''
    
    opFlowOfBlocks = np.zeros((xBlockSize,yBlockSize,2))
    
    for index,value in np.ndenumerate(mag):
        opFlowOfBlocks[index[0]/noOfRowInBlock][index[1]/noOfColInBlock][0] += mag[index[0]][index[1]]
        opFlowOfBlocks[index[0]/noOfRowInBlock][index[1]/noOfColInBlock][1] += angle[index[0]][index[1]]

    centreOfBlocks = np.zeros((xBlockSize,yBlockSize,2))
    for index,value in np.ndenumerate(opFlowOfBlocks):
        opFlowOfBlocks[index[0]][index[1]][index[2]] = float(value)/(noOfRowInBlock*noOfColInBlock)
        val = opFlowOfBlocks[index[0]][index[1]][index[2]]

        if(index[2] == 1):
            angInDeg = math.degrees(val)
            if(angInDeg > 337.5):
                k = 0
            else:
                q = angInDeg//22.5
                a1 = q*22.5
                q1 = angInDeg - a1
                a2 = (q+2)*22.5
                q2 =  a2 - angInDeg
                if(q1 < q2):
                    k = int(round(a1/45))
                else:
                    k = int(round(a2/45))        
            opFlowOfBlocks[index[0]][index[1]][index[2]] = k
            theta = val
            
        
        
        
        if(index[2] == 0):
            r = val
            x = ((index[0] + 1)*noOfRowInBlock)-(noOfRowInBlock/2)
            y = ((index[1] + 1)*noOfColInBlock)-(noOfColInBlock/2)
            centreOfBlocks[index[0]][index[1]][0] = x
            centreOfBlocks[index[0]][index[1]][1] = y
    return opFlowOfBlocks,noOfRowInBlock,noOfColInBlock,noOfRowInBlock*noOfColInBlock,centreOfBlocks,xBlockSize,yBlockSize
