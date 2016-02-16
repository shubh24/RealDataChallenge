from __future__ import division
import sys
import numpy as np
import operator
import collections

def skinDetect(red,green,blue,rows,cols):
    selected = [[0 for j in range(0,cols,1)] for i in range(0,rows,1)]
    
    for i in range(0,rows,1):
        for j in range(0,cols,1):
            if red[i][j]+green[i][j]+blue[i][j] != 0:
                r = float(red[i][j]/(red[i][j]+green[i][j]+blue[i][j]))
                g = float(green[i][j]/(red[i][j]+green[i][j]+blue[i][j]))
                b = float(blue[i][j]/(red[i][j]+green[i][j]+blue[i][j]))
            else:
                r = red[i][j]
                g = green[i][j]
                b = blue[i][j]
                
            alpha = (3*b*r*r)
            if r!=0:
                beta = (1/(3*r)) + (r-g)
            else:
                beta = 1
            if b*g != 0:
                gamma = (r*b+g*g)/(b*g)
            else:
                gamma=3
                
            if alpha > 0.1276 and beta <= 0.9498 and gamma <= 2.7775:
                selected[i][j] = 1
    return selected




if __name__ == '__main__':
    red = []
    red.append([])
    blue = []
    blue.append([])
    green = []
    green.append([])

    r = map(int,raw_input().split())
    rows = r[0]
    cols = r[1]

    for i in range(0,rows,1):
        inp = map(list,raw_input().split())
        for j in inp:
            flag = 1
            num1 = ''
            num2 = ''
            num3 = ''
            for k in j:
                if k == ',':
                    flag += 1
                    continue
                if flag == 1:
                    num1 += k
                if flag ==2:
                    num2 += k
                if flag == 3:
                    num3 += k
            blue[i].append(int(num1))
            green[i].append(int(num2))
            red[i].append(int(num3))
        if i!=rows-1:        
            red.append([])
            blue.append([])
            green.append([])
    sel = skinDetect(red,green,blue,rows,cols)
    
    faces = [[0 for j in range(0,cols,1)] for i in range(0,rows,1)]
    regions = [[0 for j in range(0,cols,1)] for i in range(0,rows,1)]
    region = 0
    regionDict = {}
    
    for i in range(0,rows,1):
        for j in range(0,cols,1):
            regionFlag = 0
            faceFlag = 0
            if sel[i][j] == 1:
                if i-1 >= 0 and j-1 >= 0 and sel[i-1][j-1] == 1:
                    faces[i][j]=1
                    faceFlag = 1
                    if regions[i-1][j-1] != 0:
                        regions[i][j] = regions[i-1][j-1]
                        regionFlag = 1
                        regionDict[regions[i][j]] += 1
                elif i-1 >=0 and sel[i-1][j] >= 0:
                    faces[i][j]=1
                    faceFlag = 1
                    if regions[i-1][j] != 0:
                        regions[i][j] = regions[i-1][j]
                        regionFlag = 1
                        regionDict[regions[i][j]] += 1
                elif i-1 >= 0 and j+1 < cols and sel[i-1][j+1] == 1:
                    faces[i][j]=1
                    faceFlag = 1
                    if regions[i-1][j+1] != 0 and regionFlag == 0:
                        regions[i][j] = regions[i][j+1]
                        regionFlag = 1
                        regionDict[regions[i][j]] += 1
                elif j-1 >= 0 and sel[i][j-1] == 0:
                    faces[i][j]=1
                    faceFlag = 1
                    if regions[i][j-1] != 0:
                        regions[i][j] = regions[i][j-1]
                        regionFlag = 1
                        regionDict[regions[i][j]] += 1
                elif j+1 < cols and sel[i][j+1] == 1:
                    faces[i][j]=1
                    faceFlag = 1
                elif i+1 < rows and j-1 >= 0 and sel[i+1][j-1] == 1:
                    faces[i][j]=1
                    faceFlag = 1
                elif i+1 < rows and sel[i+1][j] == 1:
                    faces[i][j]=1
                    faceFlag = 1
                elif i+1 < rows and j+1 < cols and sel[i+1][j+1] == 1:
                    faces[i][j]=1
                    faceFlag = 1
                else:
                    faces[i][j]=0
                if faceFlag == 1 and regionFlag == 0:
                    region += 1
                    regions[i][j] = region
                    regionDict[regions[i][j]] = 1
    
    sorted_x = sorted(regionDict.items(), key=operator.itemgetter(1),reverse = True)[:15]
    countFaces = 0
    
    for x in sorted_x:
        key = x[0]
        posns = []
        for i in range(0,rows,1):
            for j in range(0,cols,1):
                if regions[i][j] == key:
                    posns.append((i,j))  
        
        arr = np.asarray(posns)
        length = arr.shape[0]
        sum_x = np.sum(arr[:, 0])
        sum_y = np.sum(arr[:, 1])
        x_cent = sum_x / length 
        y_cent = sum_y / length
        
        x_res = 0
        y_res = 0
        for i in posns:
            x_res += abs(i[0] - x_cent)
            y_res += abs(i[1] - y_cent)
        x_ave = x_res/length
        y_ave = y_res/length
        
        ratio = y_ave/x_ave
        if ratio >= 0.968 and ratio <= 2.268:
            countFaces += 1
            
    print countFaces
