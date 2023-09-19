# -*- coding: utf-8 -*-
"""1-permutation_feature_importance_rank

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15YswSyE53H5d666_eOaJ0n2rTsiqhak8
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
rootpath = "/content/drive/MyDrive/Colab Notebooks/1/"

datasets_original = "datasets-original/"
#datasets_discretize = "datasets-discretize/"
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

def setDir(filepath):
    #if filepath not exist then create  ！

    if not os.path.exists(filepath):
        pass
    else:
        shutil.rmtree(filepath,ignore_errors=True)

# Lets configure Bootstrap
sample_times = 25  #No. of bootstrap samples to be repeated (created) seed is 0-24
# Lets run Bootstrap
# change the datasets name in turn

readfilepath = rootpath + datasets_standardize

outfilepath = rootpath + datasets_standardize

readfile = readfilepath + "Promise-permutation-train-f1.csv"  # accuracy precision recall f1 auc 先算 test 再算 train

data = pd.read_csv(readfile)

df = pd.DataFrame(data)

#df_features = list(df)

#print(df_features)

#print(df_features[2:])

# AEEEM 150行63列 1个数据集 6个分类器 25次采样 150次实验 61列属性 2列自己加的标记 63列属性
# Promise 1800行22列 12个数据集 6个分类器 25次采样 1800次实验
# ReLink 450行28列 3个数据集 6个分类器 25次采样 450次实验
print(df.shape)
print(df)
# print(df.index)
df_rank = df.rank(axis=1,numeric_only=True,method="dense",ascending=False) #沿着列排名 只排数值 dense 二者相同取小值的排序 下一次增加1

#print(list(df_rank))

print(df_rank.shape)
print(df_rank)

# rank 行列交换 再排序 再交换回来？ 排序里面写上序号
#df_T = pd.DataFrame(df.values.T, columns=df.index, index=df_features)
#print(df_T)


# save as csv files
out_file_path = outfilepath + "Promise-permutation-train-f1-rank.csv"

setDir(out_file_path)

df_rank.to_csv(out_file_path,index=False)  #不加行名



#out_file_train = pd.DataFrame(permutation_train_list,columns=out_columns)
#out_file_test = pd.DataFrame(permutation_test_list,columns=out_columns)

#out_file_train.to_csv(out_file_train_path,index=False,columns=out_columns)
#out_file_test.to_csv(out_file_test_path,index=False,columns=out_columns)

# rank 计算结束