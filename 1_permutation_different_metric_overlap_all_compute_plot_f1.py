# -*- coding: utf-8 -*-
"""1-permutation_different_metric_overlap_all_compute_plot_F1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nWG2i6RuspeEdGNPUix5J3wn1JlA34oQ
"""

import scipy.io.arff
import pandas as pd
import numpy as np
from sklearn.utils import resample # for Bootstrap sampling
import shutil
import os

from numpy import array

#Import resampling and modeling algorithms

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import matthews_corrcoef

import warnings

warnings.filterwarnings("ignore")

# click load google drive
# 置换特征重要性在测试集上不同的指标得到的特征排名的一致性 Overlap 这个文件是计算 F1

rootpath = "/content/drive/MyDrive/Colab Notebooks/1/"

datasets_original = "datasets-original/"
datasets_discretize = "datasets-discretize/"
datasets_log = "datasets-log/"
datasets_minmax = "datasets-min-max/"
datasets_standardize = "datasets-standardize/"

AEEEM = ["EQ"]
ReLink = ["Zxing", "Apache", "Safe"]
Promise = [ "camel-1.2", "ivy-1.1", "jedit-3.2", "log4j-1.1", "lucene-2.0", "lucene-2.2", "lucene-2.4",
        "poi-1.5", "poi-2.5", "poi-3.0", "xalan-2.5", "xalan-2.6"]

ARFF = "ARFF/"
CSV = "CSV/"

BOOTSTRAP = "BOOTSTRAP/"


# some data sets imbanlance so we exclude it because these classifier have precision recall and f1 = 0  so we select 30-70% percent of defective

data_o_Promise = pd.DataFrame(pd.read_csv(rootpath + datasets_original + "Promise-permutation-test-f1-rank.csv"))

data_o_ReLink = pd.DataFrame(pd.read_csv(rootpath + datasets_original + "ReLink-permutation-test-f1-rank.csv"))

data_o_AEEEM = pd.DataFrame(pd.read_csv(rootpath + datasets_original + "AEEEM-permutation-test-f1-rank.csv"))

data_log_Promise = pd.DataFrame(pd.read_csv(rootpath + datasets_log + "Promise-permutation-test-f1-rank.csv"))

data_log_ReLink = pd.DataFrame(pd.read_csv(rootpath + datasets_log + "ReLink-permutation-test-f1-rank.csv"))

data_log_AEEEM = pd.DataFrame(pd.read_csv(rootpath + datasets_log + "AEEEM-permutation-test-f1-rank.csv"))


data_min_Promise = pd.DataFrame(pd.read_csv(rootpath + datasets_minmax + "Promise-permutation-test-f1-rank.csv"))

data_min_ReLink = pd.DataFrame(pd.read_csv(rootpath + datasets_minmax + "ReLink-permutation-test-f1-rank.csv"))

data_min_AEEEM = pd.DataFrame(pd.read_csv(rootpath + datasets_minmax + "AEEEM-permutation-test-f1-rank.csv"))

data_sta_Promise = pd.DataFrame(pd.read_csv(rootpath + datasets_standardize + "Promise-permutation-test-f1-rank.csv"))

data_sta_ReLink = pd.DataFrame(pd.read_csv(rootpath + datasets_standardize + "ReLink-permutation-test-f1-rank.csv"))

data_sta_AEEEM = pd.DataFrame(pd.read_csv(rootpath + datasets_standardize + "AEEEM-permutation-test-f1-rank.csv"))


print(data_o_Promise.shape)
print(data_log_Promise.shape)
print(data_o_Promise.shape[0])
print(data_log_Promise.shape[1])
print(data_o_Promise.index)

print(data_o_Promise.shape)
print(data_o_ReLink.shape)
print(data_o_AEEEM.shape)
print(data_log_Promise.shape)
print(data_log_ReLink.shape)
print(data_log_AEEEM.shape)

O = [data_o_Promise, data_o_ReLink, data_o_AEEEM]
L = [data_log_Promise, data_log_ReLink, data_log_AEEEM]
M = [data_min_Promise, data_min_ReLink, data_min_AEEEM]
S = [data_sta_Promise, data_sta_ReLink, data_sta_AEEEM]

overlap_L_O_1_list = []
overlap_L_O_3_list = []
overlap_L_O_5_list = []

overlap_M_O_1_list = []
overlap_M_O_3_list = []
overlap_M_O_5_list = []

overlap_S_O_1_list = []
overlap_S_O_3_list = []
overlap_S_O_5_list = []


for k in range(len(O)):

  for i in range(O[k].shape[0]):

    old_O_1_attrlist = []
    new_L_1_attrlist = []

    old_O_3_attrlist = []
    new_L_3_attrlist = []

    old_O_5_attrlist = []
    new_L_5_attrlist = []

    new_M_1_attrlist = []
    new_M_3_attrlist = []
    new_M_5_attrlist = []

    new_S_1_attrlist = []
    new_S_3_attrlist = []
    new_S_5_attrlist = []


    for j in range(O[k].shape[1]):

      if(O[k].loc[i].values[j] == 1):
        old_O_1_attrlist.append(list(O[k])[j])

      if(L[k].loc[i].values[j] == 1):
        new_L_1_attrlist.append(list(L[k])[j])
      if(M[k].loc[i].values[j] == 1):
        new_M_1_attrlist.append(list(M[k])[j])
      if(S[k].loc[i].values[j] == 1):
        new_S_1_attrlist.append(list(S[k])[j])

      if(O[k].loc[i].values[j] == 1 or O[k].loc[i].values[j] == 2 or O[k].loc[i].values[j] == 3):  # =1 overlap-1 =3 overlap-3
        old_O_3_attrlist.append(list(O[k])[j])
      if(L[k].loc[i].values[j] == 1 or L[k].loc[i].values[j] == 2 or L[k].loc[i].values[j] == 3):
        new_L_3_attrlist.append(list(L[k])[j])
      if(M[k].loc[i].values[j] == 1 or M[k].loc[i].values[j] == 2 or M[k].loc[i].values[j] == 3):
        new_M_3_attrlist.append(list(M[k])[j])
      if(S[k].loc[i].values[j] == 1 or S[k].loc[i].values[j] == 2 or S[k].loc[i].values[j] == 3):
        new_S_3_attrlist.append(list(S[k])[j])

      if(O[k].loc[i].values[j] == 1 or O[k].loc[i].values[j] == 2 or O[k].loc[i].values[j] == 3 or O[k].loc[i].values[j] == 4 or O[k].loc[i].values[j] == 5):
        old_O_5_attrlist.append(list(O[k])[j])
      if(L[k].loc[i].values[j] == 1 or L[k].loc[i].values[j] == 2 or L[k].loc[i].values[j] == 3 or L[k].loc[i].values[j] == 4 or L[k].loc[i].values[j] == 5):
        new_L_5_attrlist.append(list(L[k])[j])
      if(M[k].loc[i].values[j] == 1 or M[k].loc[i].values[j] == 2 or M[k].loc[i].values[j] == 3 or M[k].loc[i].values[j] == 4 or M[k].loc[i].values[j] == 5):
        new_M_5_attrlist.append(list(M[k])[j])
      if(S[k].loc[i].values[j] == 1 or S[k].loc[i].values[j] == 2 or S[k].loc[i].values[j] == 3 or S[k].loc[i].values[j] == 4 or S[k].loc[i].values[j] == 5):
        new_S_5_attrlist.append(list(S[k])[j])

    """
    # 需要检查交集和并集是否与看到的一致，多检查几个验证代码正确性 11-24号下午验证 正确
    print("LO 1交集")
    print(list(set(old_O_1_attrlist).intersection(set(new_L_1_attrlist))))
    print("LO 1并集")
    print(list(set(old_O_1_attrlist).union(set(new_L_1_attrlist))))

    print("MO 1交集")
    print(list(set(old_O_1_attrlist).intersection(set(new_M_1_attrlist))))
    print("MO 1并集")
    print(list(set(old_O_1_attrlist).union(set(new_M_1_attrlist))))

    print("SO 1交集")
    print(list(set(old_O_1_attrlist).intersection(set(new_S_1_attrlist))))
    print("SO 1并集")
    print(list(set(old_O_1_attrlist).union(set(new_S_1_attrlist))))
    """


    #print(old_attrlist) #输出证明有的的确是多个属性同时为1 rank diff 没算错
    #print(new_attrlist)



    # 交集/并集
    overlap_L_O_1 = len(list(set(old_O_1_attrlist).intersection(set(new_L_1_attrlist)))) / len(list(set(old_O_1_attrlist).union(set(new_L_1_attrlist))))
    overlap_L_O_3 = len(list(set(old_O_3_attrlist).intersection(set(new_L_3_attrlist)))) / len(list(set(old_O_3_attrlist).union(set(new_L_3_attrlist))))
    overlap_L_O_5 = len(list(set(old_O_5_attrlist).intersection(set(new_L_5_attrlist)))) / len(list(set(old_O_5_attrlist).union(set(new_L_5_attrlist))))

    overlap_M_O_1 = len(list(set(old_O_1_attrlist).intersection(set(new_M_1_attrlist)))) / len(list(set(old_O_1_attrlist).union(set(new_M_1_attrlist))))
    overlap_M_O_3 = len(list(set(old_O_3_attrlist).intersection(set(new_M_3_attrlist)))) / len(list(set(old_O_3_attrlist).union(set(new_M_3_attrlist))))
    overlap_M_O_5 = len(list(set(old_O_5_attrlist).intersection(set(new_M_5_attrlist)))) / len(list(set(old_O_5_attrlist).union(set(new_M_5_attrlist))))

    overlap_S_O_1 = len(list(set(old_O_1_attrlist).intersection(set(new_S_1_attrlist)))) / len(list(set(old_O_1_attrlist).union(set(new_S_1_attrlist))))
    overlap_S_O_3 = len(list(set(old_O_3_attrlist).intersection(set(new_S_3_attrlist)))) / len(list(set(old_O_3_attrlist).union(set(new_S_3_attrlist))))
    overlap_S_O_5 = len(list(set(old_O_5_attrlist).intersection(set(new_S_5_attrlist)))) / len(list(set(old_O_5_attrlist).union(set(new_S_5_attrlist))))


    # L_O 表示 Log 和 原始 的重叠
    overlap_L_O_1_list.append(overlap_L_O_1)
    overlap_L_O_3_list.append(overlap_L_O_3)
    overlap_L_O_5_list.append(overlap_L_O_5)

    overlap_M_O_1_list.append(overlap_M_O_1)
    overlap_M_O_3_list.append(overlap_M_O_3)
    overlap_M_O_5_list.append(overlap_M_O_5)

    overlap_S_O_1_list.append(overlap_S_O_1)
    overlap_S_O_3_list.append(overlap_S_O_3)
    overlap_S_O_5_list.append(overlap_S_O_5)



print("overlap_L_O_1_list")
print(overlap_L_O_1_list)
print(len(overlap_L_O_1_list))  # 为什么不是1800？因为有某个行存在两个1

print("overlap_L_O_3_list")
print(overlap_L_O_3_list)
print(len(overlap_L_O_3_list))

print("overlap_L_O_5_list")
print(overlap_L_O_5_list)
print(len(overlap_L_O_5_list))

print("overlap_M_O_1_list")
print(overlap_M_O_1_list)
print(len(overlap_M_O_1_list))  # 为什么不是1800？因为有某个行存在两个1

print("overlap_M_O_3_list")
print(overlap_M_O_3_list)
print(len(overlap_M_O_3_list))

print("overlap_M_O_5_list")
print(overlap_M_O_5_list)
print(len(overlap_M_O_5_list))

print("overlap_S_O_1_list")
print(overlap_S_O_1_list)
print(len(overlap_S_O_1_list))  # 为什么不是1800？因为有某个行存在两个1

print("overlap_S_O_3_list")
print(overlap_S_O_3_list)
print(len(overlap_S_O_3_list))

print("overlap_S_O_5_list")
print(overlap_S_O_5_list)
print(len(overlap_S_O_5_list))




print("计算结束")


# AEEEM 150行63列 1个数据集 6个分类器 25次采样 150次实验 61列属性 2列自己加的标记 63列属性
# Promise 1800行22列 12个数据集 6个分类器 25次采样 1800次实验
# ReLink 450行28列 3个数据集 6个分类器 25次采样 450次实验
#print(df.shape)


#print(list(df_rank))

#  计算结束

# 计算概率分布的数量 简单看一下统计数据

from collections import Counter

print(len(overlap_L_O_1_list))
print(len(overlap_L_O_3_list))
print(len(overlap_L_O_5_list))
print("---------------------")
print(len(overlap_M_O_1_list))
print(len(overlap_M_O_3_list))
print(len(overlap_M_O_5_list))
print("---------------------")
print(len(overlap_S_O_1_list))
print(len(overlap_S_O_3_list))
print(len(overlap_S_O_5_list))
print("---------------------")

count_L_O_1 = Counter(overlap_L_O_1_list)
print(count_L_O_1)
count_L_O_3 = Counter(overlap_L_O_3_list)
print(count_L_O_3)
count_L_O_5 = Counter(overlap_L_O_5_list)
print(count_L_O_5)
print("---------------------")
count_S_O_1 = Counter(overlap_S_O_1_list)
print(count_S_O_1)
count_S_O_3 = Counter(overlap_S_O_3_list)
print(count_S_O_3)
count_S_O_5 = Counter(overlap_S_O_5_list)
print(count_S_O_5)
print("---------------------")
count_M_O_1 = Counter(overlap_M_O_1_list)
print(count_M_O_1)
count_M_O_3 = Counter(overlap_M_O_3_list)
print(count_M_O_3)
count_M_O_5 = Counter(overlap_M_O_5_list)
print(count_M_O_5)
print("L-O ---------------------")
count_L_O_1_pd = pd.DataFrame(count_L_O_1.items(),columns=['label', 'counts'])
count_L_O_1_pd['probability']=count_L_O_1_pd['counts']/2400

count_L_O_3_pd = pd.DataFrame(count_L_O_3.items(),columns=['label', 'counts'])
count_L_O_3_pd['probability']=count_L_O_3_pd['counts']/2400
count_L_O_5_pd = pd.DataFrame(count_L_O_5.items(),columns=['label', 'counts'])
count_L_O_5_pd['probability']=count_L_O_5_pd['counts']/2400
print(count_L_O_1_pd)
print(count_L_O_3_pd)
print(count_L_O_5_pd)

print("M-O ---------------------")
count_M_O_1_pd = pd.DataFrame(count_M_O_1.items(),columns=['label', 'counts'])
count_M_O_1_pd['probability']=count_M_O_1_pd['counts']/2400
count_M_O_3_pd = pd.DataFrame(count_M_O_3.items(),columns=['label', 'counts'])
count_M_O_3_pd['probability']=count_M_O_3_pd['counts']/2400
count_M_O_5_pd = pd.DataFrame(count_M_O_5.items(),columns=['label', 'counts'])
count_M_O_5_pd['probability']=count_M_O_5_pd['counts']/2400
print(count_M_O_1_pd)
print(count_M_O_3_pd)
print(count_M_O_5_pd)

print("S-O ---------------------")
count_S_O_1_pd = pd.DataFrame(count_S_O_1.items(),columns=['label', 'counts'])
count_S_O_1_pd['probability']=count_S_O_1_pd['counts']/2400
count_S_O_3_pd = pd.DataFrame(count_S_O_3.items(),columns=['label', 'counts'])
count_S_O_3_pd['probability']=count_S_O_3_pd['counts']/2400
count_S_O_5_pd = pd.DataFrame(count_S_O_5.items(),columns=['label', 'counts'])
count_S_O_5_pd['probability']=count_S_O_5_pd['counts']/2400
print(count_S_O_1_pd)
print(count_S_O_3_pd)
print(count_S_O_5_pd)

"""
count_L_O_1_pd.to_csv(rootpath+"results/overlap/count_L_O_1_pd.csv",index=False)
count_L_O_3_pd.to_csv(rootpath+"results/overlap/count_L_O_3_pd.csv",index=False)
count_L_O_5_pd.to_csv(rootpath+"results/overlap/count_L_O_5_pd.csv",index=False)
count_M_O_1_pd.to_csv(rootpath+"results/overlap/count_M_O_1_pd.csv",index=False)
count_M_O_3_pd.to_csv(rootpath+"results/overlap/count_M_O_3_pd.csv",index=False)
count_M_O_5_pd.to_csv(rootpath+"results/overlap/count_M_O_5_pd.csv",index=False)
count_S_O_1_pd.to_csv(rootpath+"results/overlap/count_S_O_1_pd.csv",index=False)
count_S_O_3_pd.to_csv(rootpath+"results/overlap/count_S_O_3_pd.csv",index=False)
count_S_O_5_pd.to_csv(rootpath+"results/overlap/count_S_O_5_pd.csv",index=False)

"""

#作图统计 作图用原始的数据列表  用的是这个！！！

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

with sns.axes_style('darkgrid'):
  fig, axes = plt.subplots(3, 3, figsize=(12, 6), sharey=True, sharex=True,  dpi=350) # sharey=True ,sharex=True, dpi=350
  fig.subplots_adjust(wspace=0.010,hspace=0.050)

  #fig,axes=plt.subplots(1,3, figsize=(15, 4))

  axes[0][0].set_title( "F1 Top-1 Overlap",loc='center'  )
  axes[0][0].axvline(0, color='black', linestyle=':')
  axes[0][0].axvline(0.25, color='black', linestyle=':')
  axes[0][0].axvline(0.5, color='black', linestyle=':')
  axes[0][0].axvline(0.75, color='black', linestyle=':')
  axes[0][0].axvline(1, color='black', linestyle=':')
  axes[0][0].set_xticks([0.0,0.5,1.0])
  axes[0][0].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_L_O_1_list, shade=True, color='darkblue', linewidth=2, ax=axes[0][0])

  xmedian1 = np.median(overlap_L_O_1_list)
  print(xmedian1)
  axes[0][0].axvline(xmedian1, color='red')

  #axes[0].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  axes[0][0].set_ylabel( "L vs O")

  axes[0][1].set_title( "F1 Top-3 Overlap",loc='center'  )
  axes[0][1].axvline(0, color='black', linestyle=':')
  axes[0][1].axvline(0.25, color='black', linestyle=':')
  axes[0][1].axvline(0.5, color='black', linestyle=':')
  axes[0][1].axvline(0.75, color='black', linestyle=':')
  axes[0][1].axvline(1, color='black', linestyle=':')

  axes[0][1].set_xticks([0.0,0.25,0.5,0.75,1.0])
  axes[0][1].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_L_O_3_list, shade=True, color='darkblue', linewidth=2, ax=axes[0][1])
  #axes[0].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[0].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

  xmedian2 = np.median(overlap_L_O_3_list)
  print(xmedian2)
  axes[0][1].axvline(xmedian2, color='red')

  axes[0][2].set_title( "F1 Top-5 Overlap",loc='center'  )
  axes[0][2].axvline(0, color='black', linestyle=':')
  axes[0][2].axvline(0.25, color='black', linestyle=':')
  axes[0][2].axvline(0.5, color='black', linestyle=':')
  axes[0][2].axvline(0.75, color='black', linestyle=':')
  axes[0][2].axvline(1, color='black', linestyle=':')
  axes[0][2].set_xticks([0.0,0.25,0.5,0.75,1.0])
  axes[0][2].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_L_O_5_list, shade=True, color='darkblue', linewidth=2, ax=axes[0][2])
  #axes[0].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[0].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

  xmedian3 = np.median(overlap_L_O_5_list)
  print(xmedian3)
  axes[0][2].axvline(xmedian3, color='red')


  axes[1][0].set_ylabel( "M vs O")
  axes[1][0].axvline(0, color='black', linestyle=':')
  axes[1][0].axvline(0.25, color='black', linestyle=':')
  axes[1][0].axvline(0.5, color='black', linestyle=':')
  axes[1][0].axvline(0.75, color='black', linestyle=':')
  axes[1][0].axvline(1, color='black', linestyle=':')
  axes[1][0].set_xticks([0.0,0.5,1.0])
  axes[1][0].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_M_O_1_list, shade=True, color='darkorange', linewidth=2, ax=axes[1][0])
  #axes[1].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[1].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

  xmedian4 = np.median(overlap_M_O_1_list)
  print(xmedian4)
  axes[1][0].axvline(xmedian4, color='red')

  axes[1][1].axvline(0, color='black', linestyle=':')
  axes[1][1].axvline(0.25, color='black', linestyle=':')
  axes[1][1].axvline(0.5, color='black', linestyle=':')
  axes[1][1].axvline(0.75, color='black', linestyle=':')
  axes[1][1].axvline(1, color='black', linestyle=':')

  axes[1][1].set_xticks([0.0,0.25,0.5,0.75,1.0])
  axes[1][1].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_M_O_3_list, shade=True, color='darkorange', linewidth=2, ax=axes[1][1])
  #axes[4].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[4].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

  xmedian5 = np.median(overlap_M_O_3_list)
  print(xmedian5)
  axes[1][1].axvline(xmedian5, color='red')

  axes[1][2].axvline(0, color='black', linestyle=':')
  axes[1][2].axvline(0.25, color='black', linestyle=':')
  axes[1][2].axvline(0.5, color='black', linestyle=':')
  axes[1][2].axvline(0.75, color='black', linestyle=':')
  axes[1][2].axvline(1, color='black', linestyle=':')
  axes[1][2].set_xticks([0.0,0.25,0.5,0.75,1.0])
  axes[1][2].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_M_O_5_list, shade=True, color='darkorange', linewidth=2, ax=axes[1][2])
  #axes[0].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[0].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

  xmedian6 = np.median(overlap_M_O_5_list)
  print(xmedian6)
  axes[1][2].axvline(xmedian6, color='red')


  axes[2][0].set_ylabel( "Z vs O")
  axes[2][0].axvline(0, color='black', linestyle=':')
  axes[2][0].axvline(0.25, color='black', linestyle=':')
  axes[2][0].axvline(0.5, color='black', linestyle=':')
  axes[2][0].axvline(0.75, color='black', linestyle=':')
  axes[2][0].axvline(1, color='black', linestyle=':')
  axes[2][0].set_xticks([0.0,0.5,1.0])
  axes[2][0].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_S_O_1_list, shade=True, color='darkgreen', linewidth=2, ax=axes[2][0])
  #axes[2].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[2].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

  xmedian7 = np.median(overlap_S_O_1_list)
  print(xmedian7)
  axes[2][0].axvline(xmedian7, color='red')

  axes[2][1].axvline(0, color='black', linestyle=':')
  axes[2][1].axvline(0.25, color='black', linestyle=':')
  axes[2][1].axvline(0.5, color='black', linestyle=':')
  axes[2][1].axvline(0.75, color='black', linestyle=':')
  axes[2][1].axvline(1, color='black', linestyle=':')

  axes[2][1].set_xticks([0.0,0.25,0.5,0.75,1.0])
  axes[2][1].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_S_O_3_list, shade=True, color='darkgreen', linewidth=2, ax=axes[2][1])
  #axes[4].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[4].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)
  xmedian8 = np.median(overlap_S_O_3_list)
  print(xmedian8)
  axes[2][1].axvline(xmedian8, color='red')

  axes[2][2].axvline(0, color='black', linestyle=':')
  axes[2][2].axvline(0.25, color='black', linestyle=':')
  axes[2][2].axvline(0.5, color='black', linestyle=':')
  axes[2][2].axvline(0.75, color='black', linestyle=':')
  axes[2][2].axvline(1, color='black', linestyle=':')
  axes[2][2].set_xticks([0.0,0.25,0.5,0.75,1.0])
  axes[2][2].set_yticks([0.0,0.5,1.0,1.5,2.0])
  sns.kdeplot(overlap_S_O_5_list, shade=True, color='darkgreen', linewidth=2, ax=axes[2][2])
  xmedian9 = np.median(overlap_S_O_5_list)
  print(xmedian9)
  axes[2][2].axvline(xmedian9, color='red')



  #axes[0].set_ylabel( "Probability density", fontsize=20, labelpad=10 )
  #axes[0].set_xlabel( "Temperature:K",fontsize=20 ,labelpad=10)

#作图统计 作图用原始的数据列表 论文里用分布图 数据分析时结合 概率分布图和概率值统计 分析 这个作为参考

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt



with sns.axes_style('darkgrid'):
  fig, axes = plt.subplots(3, 3, figsize=(12, 6),sharey=True,sharex=True, dpi=350) # sharey=True ,sharex=True, dpi=350
  fig.subplots_adjust(wspace=0.010,hspace=0.050)



  axes[0][0].set_title( "Top-1 Overlap",loc='center'  )

  sns.histplot(data=overlap_L_O_1_list, kde=True, stat='probability',ax=axes[0][0])

  axes[0][1].set_title( "Top-3 Overlap",loc='center'  )

  sns.histplot(data=overlap_L_O_3_list, kde=True, stat='probability',ax=axes[0][1])

  axes[0][2].set_title( "Top-5 Overlap",loc='center'  )
  sns.histplot(data=overlap_L_O_5_list, kde=True, stat='probability',ax=axes[0][2])



  sns.histplot(data=overlap_M_O_1_list, kde=True, stat='probability',ax=axes[1][0])

  sns.histplot(data=overlap_M_O_3_list, kde=True, stat='probability',ax=axes[1][1])

  sns.histplot(data=overlap_M_O_5_list, kde=True, stat='probability',ax=axes[1][2])



  sns.histplot(data=overlap_S_O_1_list, kde=True, stat='probability',ax=axes[2][0])

  sns.histplot(data=overlap_S_O_3_list, kde=True, stat='probability',ax=axes[2][1])

  sns.histplot(data=overlap_S_O_5_list, kde=True, stat='probability',ax=axes[2][2])


"""
sns.histplot(data=overlap_L_O_1_list, kde=True, stat='probability')
plt.xticks([0.0,0.5,1.0])
plt.show()

sns.histplot(data=overlap_L_O_3_list, kde=True, stat='probability')
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_L_O_5_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_M_O_1_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_M_O_3_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_M_O_5_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_S_O_1_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_S_O_3_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

sns.histplot(data=overlap_S_O_5_list, kde=True, stat='probability')
#plt.ylabel("纵坐标")
plt.xticks([0.0,0.25,0.5,0.75,1.0])
plt.show()

"""