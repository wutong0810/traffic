# -*- coding: utf-8 -*-
import cPickle as pickle
import numpy as np
def writeObject(path0,data):
    path1 = unicode(path0, "utf8")
    fileOpen=open(path1,'wb')
    pickle.dump(data,fileOpen)
    fileOpen.close()

def listConcat(data):
    medDataFinal=data[0]
    if len(data)>=1:
        for i in range(1,len(data)):
            medDataFinal=np.vstack([medDataFinal,data[i]])
    return medDataFinal




def loadObject(path0):
    path1 = unicode(path0, "utf8")
    fileOpen=open(path1,'rb')
    data=pickle.load(fileOpen)
    fileOpen.close()
    return data



# 获取行程时间特征变量，取历史前3个周期
# 返回的特征向量，0:前4个周期的行程时间，1：前3个周期的行程时间，2：前2个周期的行程时间:3：前1个周期的行程周期:
# 4:t-4到t-3变化值，5：t-3到t-2变化值，6.t-2到t-1
# 7：日期每天所处的时刻，8：星期
def getFeature(data,freeV):
    Vfeature=np.zeros((len(data),9))
    for i in range(len(data)):
        if i<4:
            Vfeature[i,0]=freeV
            Vfeature[i,1] = freeV
            Vfeature[i, 2] = freeV
            Vfeature[i, 3] = freeV
            Vfeature[i, 7] = data[i,0]
            Vfeature[i, 8] = data[i,4]
        else:
            Vfeature[i, 0] = data[i-4, 5]
            Vfeature[i, 1] = data[i-3, 5]
            Vfeature[i, 2] = data[i-2, 5]
            Vfeature[i, 3] = data[i -1, 5]
            Vfeature[i, 4] = data[i-3, 5]-data[i-4,5]
            Vfeature[i, 5] = data[i-2, 5]-data[i-3,5]
            Vfeature[i, 6] = data[i-2, 1]-data[i-2,5]
            Vfeature[i, 7] = data[i, 0]
            Vfeature[i, 8] = data[i, 4]
    return Vfeature



# 输出值为1：前3个周期的流量输入值，2：前2个周期的流量输入值，3：前1个周期的流量输入值
# 4：t-3到t-2的流量变化值，5：t-2到t-1的流量变化值，6：前3个周期的流量输出值，7：前2个周期的流量输出值
# 8：前1个周期的流量输出值，9：t-3到t-2的流量变化值 10:t-2到t-1的驶出量变化值，11：前3个周期的累积驶入驶出值
# 12：前2个周期的累积驶入驶出的值，13：前一个周期的累积驶入驶出的值
def getQ(data):
    Vfeature = np.zeros((len(data),13 ))
    for i in range(len(data)):
        if i>3:
            Vfeature[i, 0] = data[i-3, 1]
            Vfeature[i, 1] = data[i-2, 1]
            Vfeature[i, 2] = data[i-1, 1]
            Vfeature[i, 3] = data[i-2, 1]-data[i-3, 1]
            Vfeature[i, 4] = data[i-1, 1]-data[i-2, 1]
            Vfeature[i, 5] = data[i-3, 2]
            Vfeature[i, 6] = data[i-2, 2]
            Vfeature[i, 7] = data[i-1, 2]
            Vfeature[i, 8] = data[i-2, 2]-data[i-3,2]
            Vfeature[i, 9] = data[i-1, 2]-data[i-2,2]
            Vfeature[i, 10] = data[i-3, 1]-data[i-3,2]
            Vfeature[i, 11] = data[i-2, 1]-data[i-2,2]
            Vfeature[i, 12] = data[i-1, 1]-data[i-1,2]
    return Vfeature















