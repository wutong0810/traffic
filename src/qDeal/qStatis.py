# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


# 驶入驶出流量统计函数，参数1为上游交叉口，参数2为下游交叉口，参数3为上游交叉口驶入方向1，参数4为上游交叉口驶入方向1的驶入车道
# 参数5为上游交叉口驶入方向2，参数6为上游交叉口驶入方向2的驶入车道
# 参数7为下游驶出方向1，参数8为下游交叉口的驶出方向1的驶出车道,参数9为下游交叉口的驶出方向1的驶出车道匹配统计的车道
# 返回数组是第1列是时间，第2列为驶入量，第3列为驶出量，第4列为匹配车道的过车流量
def inOut(days,upInsec, downInsec, upDire1, upClane1, upDire2, upClane2, downDire, downClane1,downClane2):
    upInsec.iloc[:, 1] = pd.to_datetime(upInsec.iloc[:, 1])
    downInsec.iloc[:, 1] = pd.to_datetime(downInsec.iloc[:, 1])
    upInsec['day'] = upInsec.iloc[:, 1].apply(lambda x: 100 * x.month + x.day)
    upInsec['sj'] = upInsec.iloc[:, 1].apply(lambda x: 3600 * x.hour + 60 * x.minute + x.second)
    downInsec['day'] = downInsec.iloc[:, 1].apply(lambda x: 100 * x.month + x.day)
    downInsec['sj'] = downInsec.iloc[:, 1].apply(lambda x: 3600 * x.hour + 60 * x.minute + x.second)
    q_total = []
    for i in days:
        print i
        med_data = np.zeros((96, 5))
        med_data[:, 0] = range(96)
        #   取出每天的驶入量
        in_q = upInsec[upInsec.iloc[:, 5] == i]
        in_q=in_q.assign(repair=0)
        #        进口道1
        cache_total1 = []
        cache1 = in_q[in_q.iloc[:, 3] == upDire1]
        for g in upClane1:
            in_Q = cache1[cache1.iloc[:, 2] == g]
            cache_total1.append(in_Q)
        in_q1 = pd.concat(cache_total1, ignore_index=True)
        #        进口道2
        cache_total2 = []
        cache1 = in_q[in_q.iloc[:, 3] == upDire2]
        for g in upClane2:
            in_Q = cache1[cache1.iloc[:, 2] == g]
            cache_total2.append(in_Q)
        in_q2 = pd.concat(cache_total2, ignore_index=True)
        #       排序,按车道再按时间
        in_q1 = in_q1.sort_values(by=[in_q1.columns[2], in_q1.columns[6]])
        in_q2 = in_q2.sort_values(by=[in_q2.columns[2], in_q2.columns[6]])
        in_q1Final = removeFun(in_q1)
        in_q2Final = removeFun(in_q2)
        #        驶出车道流量
        out_q = downInsec[downInsec.iloc[:, 5] == i]
        out_q=out_q.assign(repair=0)
        cache_total3 = []
        cache1 = out_q[out_q.iloc[:, 3] == downDire]
        for g in downClane1:
            in_Q = cache1[cache1.iloc[:, 2] == g]
            cache_total3.append(in_Q)
        out_q1 = pd.concat(cache_total3, ignore_index=True)
        # 按照车道、时间排序
        out_q1 = out_q1.sort_values(by=[out_q1.columns[2], out_q1.columns[6]])
        # 剔除掉重复匹配的车辆，防止一辆车被多次检测到
        out_q1Final = removeFun(out_q1)
        for j in range(96):
            med_data[j, 1] = len(in_q1Final[(in_q1Final.iloc[:, -2] > j * 15 * 60) & (
            in_q1Final.iloc[:, -2] < (j + 1) * 15 * 60)]) + len(
                in_q2Final[(in_q2Final.iloc[:, -2] > j * 15 * 60) & (in_q2Final.iloc[:, -2] < (j + 1) * 15 * 60)])
            med_data[j, 2] = len(
                out_q1Final[(out_q1Final.iloc[:, -2] > j * 15 * 60) & (out_q1Final.iloc[:, -2] < (j + 1) * 15 * 60)])
            med = out_q1Final[(out_q1Final.iloc[:, -2] > j * 15 * 60) & (out_q1Final.iloc[:, -2] < (j + 1) * 15 * 60)]
            med_final1 = []
            for y in downClane2:
                cach = med[(med.iloc[:, 2] == y)]
                med_final1.append(cach)
            medFinal = pd.concat(med_final1, ignore_index=True)
            med_data[j, 3] = len(medFinal)
        q_total.append(med_data)
    return q_total



#剔除掉重复匹配的车辆，防止一辆车被多次检测到函数
def removeFun(data):
    data1=np.array(data)
    dataFinal=[]
    for i in data.iloc[:,2].unique():
        data2=data1[data1[:,2]==i]
        indice=[]
        for j in range(1,len(data2)):
            if (cmp(data2[j,0],data2[j-1,0])==0)& (data2[j,6]-data2[j-1,6]<100&len(data2[j,0])>5):
                indice.append(j-1)
    #给行程时间付上-1来标示行程时间
        for h in indice:
            data2[h,7]=-1
        dataFinal.append(pd.DataFrame(data2[data2[:,7]>-1]))
    dataFinal_1=pd.concat(dataFinal, ignore_index=True)
    return dataFinal_1




