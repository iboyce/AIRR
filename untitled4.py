# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:48:40 2017

@author: xuzhi
"""

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl 

def radar2d(title="matplotlib雷达图",labels=['营运','偿债','成长','盈利'],ndata =[[1,3,6,4],[2,6,4,9]],filepath=None):
    data=ndata[0]
    data2=ndata[1]
    dataLenth = len(labels)
    angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False)
    data = np.concatenate((data, [data[0]])) # 闭合
    data2 = np.concatenate((data2, [data2[0]]))
    
    angles = np.concatenate((angles, [angles[0]])) # 闭合
    
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)    # polar参数！！
    ax.plot(angles, data, 'mo-', linewidth=2)    # 画线
    ax.plot(angles, data2, 'ro-', linewidth=2)   # 画线
    print(data,data2)
    ax.fill(angles, data, facecolor='r', alpha=0.25)   # 填充
    ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei")
    ax.set_title(title, va='bottom', fontproperties="SimHei")
    ax.set_rlim(0,10)
    ax.grid(True)

    
    if filepath==None:
        plt.show()
    else:
        plt.savefig(filepath)
    plt.clf()
    plt.cla()
    

radar2d(title="财务能力",labels= ['营运','偿债','成长','盈利'],ndata =[[1,3,6,4],[2,6,4,9]])