# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:52:19 2017

@author: xuzhi
"""

import numpy as np
import matplotlib.pyplot as plt

class xz_graph():
    
    def radar(self,title="matplotlib雷达图",labels= ['艺术A','调研I','实际R','常规C','企业E','社会S'],data =[1,4,3,6,4,8],filepath=None):
        dataLenth = len(labels)
        angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False)
        data = np.concatenate((data, [data[0]])) # 闭合
        angles = np.concatenate((angles, [angles[0]])) # 闭合
        
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)# polar参数！！
        ax.plot(angles, data, 'bo-', linewidth=2)# 画线
        ax.fill(angles, data, facecolor='r', alpha=0.25)# 填充
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

    def plot4z(self,x,y,str_title=['ROE','FCF','$PE^{TTM}$','PB'],filepath=None):
        plt.figure(1,figsize=(10,10),dpi=72)#创建图表1  ,figsize指定尺寸，dip指定清晰度
        plt.subplots_adjust(wspace=0.3, hspace=0.4)                #调整子图之间距
        
        font = {'family' : 'serif',  
        'color'  : 'darkred',  
        'weight' : 'normal',  
        'size'   : 10,  
        }  
        
        for i in range(1,5):
            plt.sca(plt.subplot(2,2,i))
            plt.xticks(fontsize=10)      #指定坐标尺寸
            plt.yticks(fontsize=10)
            plt.plot(x[i-1],y[i-1])
            plt.title(str_title[i-1],fontdict=font)              #设置如上定义的字体 
        
        if filepath==None:
            plt.show()
        else:
            plt.savefig(filepath)
        plt.clf()
        plt.cla()

    def bar(self,x,y,title="bar图",filepath=None):      
        plt.bar(range(len(y)), y, tick_label=x)
        plt.title(title)
        
        if filepath==None:
            plt.show()
        else:
            plt.savefig(filepath)
        plt.clf()
        plt.cla()
        
if __name__ == '__main__':
    
    x=np.array([np.linspace(0.3*x,1,5) for x in range(4)])      #生成二维数据 4行K列
    y=np.abs(np.sin(x*1010))
    gp = xz_graph()
    gp.radar(title="财务能力",labels= ['营运','偿债','成长','盈利','现金流'],data =[1,3,6,4,8],filepath='./pic/radar.png')
    gp.plot4z(x*10,y,filepath='./pic/plot4z.png')
    gp.bar([x for x in range(10)],[x for x in range(10)],title="资金净流入",filepath='./pic/bar.png')