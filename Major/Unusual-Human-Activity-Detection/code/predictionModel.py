import motionInfuenceGenerator as mig
import createMegaBlocks as cmb
import numpy as np
import cv2
def square(a):
    return (a**2)

def diff(l):
    return (l[0] - l[1])
def showUnusualActivities(unusual, vid, noOfRows, noOfCols, n):
   
    unusualFrames = unusual.keys()
    unusualFrames.sort()
    print(unusualFrames)
    cap = cv2.VideoCapture(vid)
    ret, frame = cap.read()
    rows, cols = frame.shape[0], frame.shape[1]
    rowLength = rows/(noOfRows/n)
    colLength = cols/(noOfCols/n)
    print("Block Size ",(rowLength,colLength))
    count = 0
    screen_res = 980, 520
    scale_width = screen_res[0] / 320
    scale_height = screen_res[1] / 240
    scale = min(scale_width, scale_height)
    window_width = int(320 * scale)
    window_height = int(240 * scale)

    cv2.namedWindow('Unusual Frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Unusual Frame',window_width, window_height)
    while 1:
        print(count)
        ret, uFrame = cap.read()
        '''
        if(count <= 475):
            
            count += 1
            continue
        
        elif((count-475) in unusualFrames):
        '''
        if(count in unusualFrames):
            if (ret == False):
                break
            for blockNum in unusual[count]:
                print(blockNum)
                x1 = blockNum[1] * rowLength
                y1 = blockNum[0] * colLength
                x2 = (blockNum[1]+1) * rowLength
                y2 = (blockNum[0]+1) * colLength
                cv2.rectangle(uFrame,(x1,y1),(x2,y2),(0,0,255),1)
            print("Unusual frame number ",str(count))
        cv2.imshow('Unusual Frame',uFrame)
            
        cv2.waitKey(0)
            #cv2.destroyAllWindows()
        '''
        if(count == 622):
            break
        '''
        count += 1
def constructMinDistMatrix(megaBlockMotInfVal,codewords, noOfRows, noOfCols, vid):
    #threshold = 2.1874939946e-21
    #threshold = 0.00196777849633
    #threshold = 9.3985643749758953e-06
    #threshold = 0.439167467697
    #threshold = 0.021305195096797892
    #threshold = 3.35845489394e-07
    #threshold = 1.6586380629e-08
    #threshold = 0.000212282134156
    #threshold = 4.63266766923e-14
    #threshold = 7.29868038369e-06
    #threshold = 8.82926005091e-05
    #threshold = 7.39718222289e-14
    #threshold = 8.82926005091e-05
    #threshold = 0.0080168593265873295
    #threshold = 0.00511863986892
    #------------------------------------#
    threshold = 5.83682407063e-05
    #threshold = 3.37029584538e-07
    #------------------------------------#
    #threshold = 2.63426664698e-06
    #threshold = 1.91130257263e-08
    
    #threshold = 0.0012675861679
    #threshold = 1.01827939172e-05
    n = 2
    minDistMatrix = np.zeros((len(megaBlockMotInfVal[0][0]),(noOfRows/n),(noOfCols/n)))
    for index,val in np.ndenumerate(megaBlockMotInfVal[...,0]):
        eucledianDist = []
        for codeword in codewords[index[0]][index[1]]:
            #print("haha")
            temp = [list(megaBlockMotInfVal[index[0]][index[1]][index[2]]),list(codeword)]
            #print("Temp",temp)
            dist = np.linalg.norm(megaBlockMotInfVal[index[0]][index[1]][index[2]]-codeword)
            #print("Dist ",dist)
            eucDist = (sum(map(square,map(diff,zip(*temp)))))**0.5
            #eucDist = (sum(map(square,map(diff,zip(*temp)))))
            eucledianDist.append(eucDist)
            #print("My calc ",sum(map(square,map(diff,zip(*temp)))))
        #print(min(eucledianDist))
        minDistMatrix[index[2]][index[0]][index[1]] = min(eucledianDist)
    unusual = {}
    for i in range(len(minDistMatrix)):
        if(np.amax(minDistMatrix[i]) > threshold):
            unusual[i] = []
            for index,val in np.ndenumerate(minDistMatrix[i]):
                #print("MotInfVal_train",val)
                if(val > threshold):
                        unusual[i].append((index[0],index[1]))
    print(unusual)
    showUnusualActivities(unusual, vid, noOfRows, noOfCols, n)
    
def label_video(vid):
    '''
        calls all methods to test the given video
       
    '''
    print "Labelling video ", vid
    MotionInfOfFrames, rows, cols = mig.getMotionInfuenceMap(vid)
    #np.save("videos\scene1\rows_cols_set1_p1_test_20-20_k5.npy",np.array([rows,cols]))
    #######print "Motion Inf Map ", len(MotionInfOfFrames)
    #numpy.save("MotionInfluenceMaps", np.array(MotionInfOfFrames), allow_pickle=True, fix_imports=True)
    megaBlockMotInfVal = cmb.createMegaBlocks(MotionInfOfFrames, rows, cols)
    ######rows, cols = np.load("rows_cols__set3_p2_test_40_k3.npy")
    #print(megaBlockMotInfVal)
    np.save("megaBlockMotInfVal_set1_p1_test_20-20_k5.npy",megaBlockMotInfVal)
    ######megaBlockMotInfVal = np.load("megaBlockMotInfVal_set3_p2_train_40_k7.npy")
    codewords = np.load("codewords_set2_p1_train_20-20_k5.npy")
    print("codewords",codewords)
    listOfUnusualFrames = constructMinDistMatrix(megaBlockMotInfVal,codewords,rows, cols, vid)
    return
    
if __name__ == '__main__':
    inputSet = ["2_test1.avi"]
    for video in inputSet:
        label_video(video)
    print "Done"
