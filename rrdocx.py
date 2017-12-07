# -*- coding: utf-8 -*-
"""
Created on Wed Nov 39 23:30:34 3027

@author: xuzhi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
from docx.shared import Inches,Pt
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from tools import xz_graph
from docx.enum.text import WD_ALIGN_PARAGRAPH

import os,sys


class rrdocx:
    str_tzjy=''
    str_gsjs=''
    str_hyfx=''
    str_gjzb=''
    str_cwzk=''
    str_zjlfx=''
    str_qxmfx=''
    str_xwsjfx=''
    
    
    def __init__(self,filename,server):

        self.filename = filename
        self.server = server
        self.document=Document()
        
        if os.path.exists(filename):
            print("deleting...")
            os.remove(filename)
            
        #修改原有heading格式，很麻烦，常规方式不行
        styles = self.document.styles
        new_heading_style = styles.add_style('New Heading 2', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Heading 2']
        font = new_heading_style.font
        font.name = '宋体'
        font._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        new_heading_style = styles.add_style('New Heading 3', WD_STYLE_TYPE.PARAGRAPH)
        new_heading_style.base_style = styles['Heading 2']
        font = new_heading_style.font
        font.name = '宋体'
        font._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        
        
        new_normal_style = styles.add_style('New Normal', WD_STYLE_TYPE.PARAGRAPH)
        new_normal_style.base_style = styles['Normal']
    
        font = new_normal_style.font
        font.name = '宋体'
        font._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        para_format = new_normal_style.paragraph_format
        para_format.first_line_indent = Pt(20)

            
    def get_var(self):
        pass
    
    
    from datasource import estools
    
    def get_esdata(self):
        es = estools(self.server)
        data = es.getkv("airr_2017.12.7","airr_mapping","603727.SH")
        return data
        
    def makeparagraph(self):
 
        
        self.str_tzjy = "本报告对该股票长期建议：0001，预测目标价为0000。根据各方面综合测算，短期操作建议观望。"
        self.str_gsjs='公司是国内白酒行业的标志性企业，主要生产销售世界三大名酒之一的茅台酒，同时进行饮料、食品、包装材料的生产和销售，防伪技术开发，信息产业相关产品的研制开发。茅台酒历史悠久，源远流长，是酱香型白酒的典型代表，享有“国酒”的美称。公司产品形成了低度、高中低档、极品三大系列70多个规格品种，全方位跻身市场，从而占据了白酒市场制高点，称雄于中国极品酒市场。'
        self.str_hyfx='根据万德行业分类，该股票属于0007，该行业近期研究报告平均打分为0003_0，建议0003_1。该行业处于上升周期，且行业集中度较高，该公司**产品在行业占有量为*，属于寡头地位，且产品供不求。'
        self.str_gjzb='如下图，该股票近5年ROE\FCF\PE\PB变化情况。根据中证行业分类，该股票属于**，该行业于**，加权平均PE（TTM）为0005，PB为0006'
        self.str_cwzk='如下图，可以看出，该股票**能力较强，**能力稍显不足，且较去年同期有所**。'
        self.str_zjlfx='如下图，近日主力资金持续净流*，大户持续**，散户持续**。'
        self.str_qxmfx='该股票雪球热度当日排名**，新增热度**，近期热度持续**。实时舆情为**，近期舆情呈**。'
        self.str_xwsjfx='近期存在异常事件，南方水灾导致部分原材料工厂停工，可能对**价格造成影响，预计对该股票作用**。'        
        
        
    def makegraph(self):
        
        x=np.array([np.linspace(0.3*x,1,5) for x in range(4)])      #生成二维数据 4行K列
        y=np.abs(np.sin(x*1010))
        
        gp = xz_graph()
        gp.radar(title="财务能力",labels= ['营运','偿债','成长','盈利','现金流'],data =[1,3,6,4,8],filepath='./pic/radar.png')
        gp.plot4z(x*10,y,filepath='./pic/plot4z.png')
        gp.bar([x for x in range(10)],[x for x in range(10)],title="资金净流入",filepath='./pic/bar.png')
        

    def makedocx(self):
 
        
        
        
        #行文        
        self.document.add_paragraph('一、投资意见', style='New Heading 2')
            
        paragraph=self.document.add_paragraph(self.str_tzjy, style = 'New Normal')   
        
        self.document.add_paragraph('二、基本信息分析',"New Heading 2")
        
        self.document.add_paragraph('2.1.公司介绍',"New Heading 3")
        paragraph=self.document.add_paragraph(self.str_gsjs, style = 'New Normal') 
        
        self.document.add_paragraph('2.2.行业分析',"New Heading 3")
        paragraph=self.document.add_paragraph(self.str_hyfx, style = 'New Normal') 
        
        self.document.add_paragraph('2.3.关键指标',"New Heading 3")
        paragraph=self.document.add_paragraph(self.str_gjzb, style = 'New Normal') 
        self.document.add_picture(r'./pic/plot4z.png',width=Inches(2.5))
        last_paragraph = self.document.paragraphs[-1] 
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER        
        
        self.document.add_paragraph('2.4.财务状况',"New Heading 3")
        paragraph=self.document.add_paragraph(self.str_cwzk, style = 'New Normal')
        self.document.add_picture(r'./pic/radar.png',width=Inches(2.5))
        last_paragraph = self.document.paragraphs[-1] 
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  
        
        self.document.add_paragraph('三、资金流分析',"New Heading 2")
        paragraph=self.document.add_paragraph(self.str_zjlfx, style = 'New Normal') 
        self.document.add_picture(r'./pic/bar.png',width=Inches(2.5))
        last_paragraph = self.document.paragraphs[-1] 
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        self.document.add_paragraph('四、情绪面分析',"New Heading 2")
        paragraph=self.document.add_paragraph(self.str_qxmfx, style = 'New Normal') 
        
        self.document.add_paragraph('五、行为事件分析',"New Heading 2")
        paragraph=self.document.add_paragraph(self.str_xwsjfx, style = 'New Normal') 
        
        
        self.document.save(filename)           


    def autorr(self):
        self.makeparagraph()
        self.makegraph()
        self.makedocx()

if __name__ == '__main__':
    
    filename ="./研究报告.docx"
    rd = rrdocx(filename,"10.237.2.132")
    data = rd.get_esdata()
    #rd.autorr()


#import win32api
#win32api.ShellExecute(0, 'open', filename, '','',1)