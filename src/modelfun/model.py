# -*- coding: utf-8 -*-
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import copy


def getTest(X,Y,trainDay,valDay,testDay):
    trainX=X[:(96*trainDay),:]
    trainY=Y[:(96*trainDay)]
    valX=X[(96*trainDay):(96*valDay),:]
    valY=Y[(96*trainDay):(96*valDay)]
    testX=X[(96*testDay):,:]
    testY=Y[(96*testDay):]
    return trainX,trainY,valX,valY,testX,testY


def foreFeature(trainX,trainY,validX,validY,para):
    gbm0 = RandomForestRegressor(n_estimators=para, min_samples_split=10,\
                                          min_samples_leaf=20,max_depth=11,max_features='sqrt',random_state=0)
    Mape1=np.zeros((1,(trainX.shape[1])))
    Vector=[]
    index=0
    total=range(trainX.shape[1])
    outMape=1
    for i in range(trainX.shape[1]-1):
        minMape=1
        for j in total:
            total1=copy.deepcopy(total)
            total1.remove(j)
            train_x=trainX[:,total1]
            valid_x=validX[:,total1]
            gbm0.fit(train_x,trainY)
            aa1=np.hstack([validY.reshape(-1,1), gbm0.predict(valid_x).reshape(-1,1)])
            aa2=np.abs(aa1[:,0]-aa1[:,1])/aa1[:,0]
            aa3=np.hstack([aa1,aa2.reshape(-1,1)])
            c1=np.sum(aa3[:,2])/len(aa3)
    #        print c1
            if c1<minMape:
    #            mapechange=True
                minMape=c1
                index=j
        Mape1[0,i]=minMape
        total.remove(index)
        if minMape<outMape:
            outMape=minMape
            total3=copy.deepcopy(total)
        total2=copy.deepcopy(total)
        Vector.append(total2)
    return Mape1,Vector,total3,outMape



def chooseFeature(trainX,trainY,para):
    state=range(0,100,10)
    for i in range(10):
        gbm0 = RandomForestRegressor(n_estimators=para, min_samples_split=10,\
                                          min_samples_leaf=20,max_depth=11,max_features='sqrt',random_state=state[i])
      # 这里我们进行十次循环取交集
        tmp = set()
        gbm0.fit(trainX, trainY)
        # print("training finished")
        importances = gbm0.feature_importances_

        indices = np.argsort(importances)[::-1]  # 降序排列
        # print indices
        for f in range(trainX.shape[1]):
            if f < 20:  # 选出前20个重要的特征
                # print indices[f]
                tmp.add(indices[f])
        if  i==0:
            tempList=list(tmp)
        tempList=list(set(tempList).intersection(tmp))
    return tempList





def getMape(oril,predict):
    data1=np.hstack([oril.reshape(-1,1),predict.reshape(-1,1)])
    data2=np.abs(data1[:, 0] - data1[:, 1]) / data1[:, 0]
    data3=np.hstack([data1,data2.reshape(-1,1)])
    result=np.sum(data3[:,2])/len(data3)
    return result





def getResult(trainX,trainY,testX,testY,para):
    gbm0 = RandomForestRegressor(n_estimators=para, min_samples_split=10,\
                                          min_samples_leaf=20,max_depth=11,max_features='sqrt',random_state=0)
    gbm0.fit(trainX,trainY)
    predictResult=gbm0.predict(testX)
    finalResult=[]
    for i in range(7):
        finalMape=getMape(testY[i*96:(i+1)*96],predictResult[i*96:(i+1)*96])
        finalResult.append(finalMape)
    return finalResult













def computeCorrelation(X, Y):
    xBar = np.mean(X)
    yBar = np.mean(Y)
    SSR = 0
    varX = 0
    varY = 0
    for i in range(0, len(X)):
        # 对应分子部分
        diffXXBar = X[i] - xBar
        diffYYBar = Y[i] - yBar
        SSR +=(diffXXBar * diffYYBar)
        # 对应分母求和部分
        varX += diffXXBar ** 2
        varY += diffYYBar ** 2
    SST = math.sqrt(varX * varY)
    return SSR / SST


def gridSearch(trainX,trainY, validX,validY, pamater=range(20, 300, 20)):
    MAPE = np.zeros((1, len(pamater)))
    minMape = 1
    minPam = 0
    for i, j in enumerate(pamater):
        gbm0 = RandomForestRegressor(n_estimators=j, min_samples_split=50, min_samples_leaf=20, max_depth=4,
                                     max_features='sqrt', random_state=0)
        gbm0.fit(trainX, trainY)
        aa1 = np.hstack([validY.reshape(-1, 1), gbm0.predict(validX).reshape(-1, 1)])
        aa2 = np.abs(aa1[:, 0] - aa1[:, 1]) / aa1[:, 0]
        aa3 = np.hstack([aa1, aa2.reshape(-1, 1)])
        c1 = np.sum(aa3[:, 2]) / len(aa3)
        if c1 < minMape:
            minMape = c1
            minPam = i
        MAPE[0, i] = c1
    return minMape, pamater[minPam], MAPE


# 状态评估函数
def stateMap(x, freeV=86.3):
    c = 0
    x = max(1 - freeV / x, 0)
    if (x >= 0) & (x <= 0.2):
        c = 0
    elif (x > 0.2) & (x <= 0.4):
        c = 1
    elif (x > 0.4) & (x <= 0.6):
        c = 2
    elif (x > 0.6) & (x <= 0.8):
        c = 3
    elif (x > 0.8):
        c = 4
    return c
