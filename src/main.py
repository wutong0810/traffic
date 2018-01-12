# -*- coding: utf-8 -*-
from src.travelTimeDeal.timeDeal import *
from src.qDeal.qStatis import *
from src.otherFunc.func import *
from src.modelfun.model import *


# 函数参数说明：参数1上游数据路径，参数2下游数据路径，参数3路段长度，参数4上游驶入的方向1，参数5驶入方向1的驶入车道
# 参数6上游驶入方向2，参数7上游驶入方向2的驶入车道，参数8下游驶离方向，下游驶出车道，下游直行的驶出车道
# 函数输出行程时间，自由流行程速度，驶入驶出流量
def GetTravelTime(path1, path2, L,upDirect1,upLane1,upDirect2,upLane2, downDirect,downLane1,downLane2):
    ipath1=unicode(path1,'utf-8')
    ipath2=unicode(path2,'utf-8')
    dataUp=pd.read_csv(ipath1,encoding='gbk')
    dataUpRoad,dataUpDay=dataTran(dataUp)
    dataDown=pd.read_csv(ipath2,encoding='gbk')
    dataDownRoad, dataDownDay = dataTran(dataDown)
    maxtime=(L/1.5*3.6)
    mintime=(L/60.0*3.6)
    day_inter = set(dataUpDay).intersection(set(dataDownDay))
    print day_inter
    match_total_tt, match_total_final, match_total_rate = loopMatch(downData=dataDownRoad, upData=dataUpRoad,
                                                                    dayNum=day_inter, maxtime1=maxtime, mintime1=mintime,
                                                                    down_direction1=downDirect)
    q_total1 = inOut(days=day_inter,upInsec=dataUp.iloc[:,:5], downInsec=dataDown.iloc[:,:5], upDire1=upDirect1, upClane1=upLane1, upDire2=upDirect2, upClane2=upLane2,
                     downDire=downDirect, downClane1=downLane1,downClane2=downLane2)
    # 预处理,分车道,处理直行车道
    dataDeal1 = loopDeal(match_total_final, claneNum=downLane2)
    data_15min1, freeV1 = loop_15min(dataDeal1, q_total1)
    return data_15min1,freeV1,q_total1,match_total_rate






if __name__=='__main__':
    # # 瑞金-遵义路至瑞金-雪涯
    # dataFinal1=GetTravelTime(path1=r'E:\oracle\导出数据\rj_zy_1201-1231.csv', path2=r'E:\oracle\导出数据\rj_xy_1204-1231.csv', L=400,upDirect1=1,upLane1=[3,4,6],upDirect2=3,upLane2=[1,2], downDirect=1,downLane1=[1,2,3],downLane2=[1,2,3])
    # writeObject(path0=r'd:/test.txt',data=dataFinal1)
    # # 瑞金-兴关路至瑞金-遵义路
    # dataFinal2=GetTravelTime(path1=r'E:\oracle\导出数据\rj_xg_1201-1231.csv', path2=r'E:\oracle\导出数据\rj_zy_1201-1231.csv', L=400,upDirect1=1,upLane1=[2,3,4],upDirect2=3,upLane2=[1], downDirect=1,downLane1=[1,2,3,4,5,6],downLane2=[3,4,5,6])
    # writeObject(path0=r'd:/test2.txt',data=dataFinal2)
    # # 瑞金-新华至瑞金-兴关路
    # dataFinal3=GetTravelTime(path1=r'E:\oracle\导出数据\rj_xh_1201-1231.csv', path2=r'E:\oracle\导出数据\rj_xg_1201-1231.csv', L=480,upDirect1=1,upLane1=[3,4,5],upDirect2=3,upLane2=[1,2], downDirect=1,downLane1=[1,2,3,4],downLane2=[2,3,4])
    # writeObject(path0=r'd:/test3.txt',data=dataFinal3)
    ## 青云-兴关至瑞金-兴关路
    # dataFinal4=GetTravelTime(path1=r'E:\oracle\导出数据\qy_xg_1204-1231.csv', path2=r'E:\oracle\导出数据\rj_xg_1201-1231.csv', L=150,upDirect1=3,upLane1=[1,2],upDirect2=2,upLane2=[1], downDirect=3,downLane1=[1,2],downLane2=[1,2])
    # writeObject(path0=r'd:/test4.txt',data=dataFinal4)
    # # 市南-耙耙至瑞金-新华
    # dataFinal5=GetTravelTime(path1=r'E:\oracle\导出数据\sn_pp_1204-1231.csv', path2=r'E:\oracle\导出数据\rj_xh_1201-1231.csv', L=320,upDirect1=1,upLane1=[1,2,3],upDirect2=3,upLane2=[1], downDirect=1,downLane1=[3,4,5],downLane2=[3,4,5])
    # writeObject(path0=r'd:/test5.txt',data=dataFinal5)
    ## # 沙冲-兴关至青云-兴关路
    ## dataFinal6=GetTravelTime(path1=r'E:\oracle\导出数据\sc_xg_1204-1231.csv', path2=r'E:\oracle\导出数据\qy_xg_1204-1231.csv', L=660,upDirect1=3,upLane1=[3,4,5,6,7],upDirect2=2,upLane2=[1], downDirect=3,downLane1=[1,2],downLane2=[1,2])
    # #writeObject(path0=r'd:/test6.txt',data=dataFinal6)
    ## 南厂路-解放至瑞金-新华
    # dataFinal7=GetTravelTime(path1=r'E:\oracle\导出数据\jf_nc_1204-1231.csv', path2=r'E:\oracle\导出数据\rj_xh_1201-1231.csv', L=420,upDirect1=3,upLane1=[2],upDirect2=2,upLane2=[1], downDirect=3,downLane1=[1,2],downLane2=[1,2])
    # writeObject(path0=r'd:/test7.txt',data=dataFinal7)
    # 加载数据
    dataFinal1=  loadObject(path0=r'C:\Users\wutongshu\Desktop\11-20匹配数据\test.txt')
    dataFinal2 = loadObject(path0=r'C:\Users\wutongshu\Desktop\11-20匹配数据\test2.txt')
    dataFinal3 = loadObject(path0=r'C:\Users\wutongshu\Desktop\11-20匹配数据\test3.txt')
    dataFinal4 = loadObject(path0=r'C:\Users\wutongshu\Desktop\11-20匹配数据\test4.txt')
    dataFinal5 = loadObject(path0=r'C:\Users\wutongshu\Desktop\11-20匹配数据\test5.txt')
    dataFinal7 = loadObject(path0=r'C:\Users\wutongshu\Desktop\11-20匹配数据\test7.txt')
    # 合并所有数据
    Traveltime1=listConcat(dataFinal1[0])
    Traveltime2=listConcat(dataFinal2[0])
    Traveltime3=listConcat(dataFinal3[0])
    Traveltime4=listConcat(dataFinal4[0])
    Traveltime5 = listConcat(dataFinal5[0])
    Traveltime7 = listConcat(dataFinal7[0])
    #合并流量数据
    Q2=listConcat(dataFinal2[2])
    #拼接特征
    featureV1 = getFeature(data=Traveltime1,freeV=dataFinal1[1])
    featureV2 = getFeature(data=Traveltime2, freeV=dataFinal2[1])
    featureV3 = getFeature(data=Traveltime3, freeV=dataFinal3[1])
    featureV4 = getFeature(data=Traveltime4, freeV=dataFinal4[1])
    featureV5 = getFeature(data=Traveltime5, freeV=dataFinal5[1])
    featureV7 = getFeature(data=Traveltime7, freeV=dataFinal5[1])
    Qfeature=getQ(data=Q2)
    featureX=np.concatenate((featureV1,featureV2[:,:-2],featureV3[:,:-2],Qfeature,featureV4[:,:-2],featureV5[:,:-2],featureV7[:,:-2]),axis=1)
    featureY = Traveltime2[:,5]
    #调参和预测结果
    trainX, trainY, valX, valY, testX, testY=getTest(X=featureX,Y=featureY,trainDay=18,valDay=21,testDay=21)
    chosed=chooseFeature(trainX, trainY,para=100)
    bestParameter=gridSearch(trainX=trainX[:,chosed], trainY=trainY, validX=valX[:,chosed], validY=valY, pamater=range(20, 300, 20))
    result1=getResult(trainX[:,chosed], trainY,  testX[:,chosed], testY,para=bestParameter[1])
    #使用原来的特征向量
    featureX2=np.concatenate((featureV1,featureV2[:,:-2],featureV3[:,:-2],Qfeature),axis=1)
    trainX2, trainY2, valX2, valY2, testX2, testY2=getTest(X=featureX2,Y=featureY,trainDay=18,valDay=21,testDay=21)
    chosed2=chooseFeature(trainX2, trainY2,para=100)
    bestParameter2=gridSearch(trainX=trainX2[:,chosed2], trainY=trainY2, validX=valX2[:,chosed2], validY=valY2, pamater=range(20, 300, 20))
    result2=getResult(trainX2[:,chosed2], trainY2,  testX2[:,chosed2], testY2,para=bestParameter2[1])






