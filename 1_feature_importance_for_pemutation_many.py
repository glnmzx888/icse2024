# -*- coding: utf-8 -*-
"""1-feature_importance_for_Pemutation_many

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UqLQtBsNx2s30yaFgiyNdlYNIrurp1E2
"""

!pip install eli5
!pip install shap

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


# CLS = [RandomForestClassifier(),LogisticRegression(),GaussianNB(),DecisionTreeClassifier(),KNeighborsClassifier(),MLPClassifier()]
CLS = [RandomForestClassifier(random_state=0),LogisticRegression(random_state=0),GaussianNB(),DecisionTreeClassifier(random_state=0),KNeighborsClassifier(),MLPClassifier(random_state=0)]

# some data sets imbanlance so we exclude it because these classifier have precision recall and f1 = 0  so we select 30-70% percent of defective

def setDir(filepath):
    #if filepath not exist then create  ！

    if not os.path.exists(filepath):
        pass
    else:
        shutil.rmtree(filepath,ignore_errors=True)

# 这是来自eli5包的可解释性方法
import eli5
from eli5.sklearn import PermutationImportance


# Lets configure Bootstrap
sample_times = 25  #No. of bootstrap samples to be repeated (created) seed is 0-24
# Lets run Bootstrap
# change the datasets name in turn

readfilepath = rootpath + datasets_original + ARFF

outfilepath = rootpath + datasets_original

performance_list = list()

permutation_train_accuracy_list = list()
permutation_test_accuracy_list = list()
permutation_train_precision_list = list()
permutation_test_precision_list = list()
permutation_train_recall_list = list()
permutation_test_recall_list = list()
permutation_train_f1_list = list()
permutation_test_f1_list = list()

for i in range(len(ReLink)):

  readfile = readfilepath + "ReLink/" + ReLink[i] + ".arff"
  data,meta = scipy.io.arff.loadarff(readfile) # NOTE: ReLink original has bug{Y,N}->error  correct is bug {Y,N}

  df = pd.DataFrame(data)
  df_features = list(df)
  #print(df_features[:-1]) # delete bug column

  print("performance_list")
  print(performance_list)
  print("permutation_train_accuracy_list")
  print(permutation_train_accuracy_list)
  print("permutation_test_accuracy_list")
  print(permutation_test_accuracy_list)

  print("permutation_train_f1_list")
  print(permutation_train_f1_list)
  print("permutation_test_f1_list")
  print(permutation_test_f1_list)

  print(i)

  # bug has a b'Y' and b'N'
  df["bug"] = (df["bug"]== b"Y").astype(int)  # then bug into N->0 Y->1 !!!

  for j in range(len(CLS)):

    # Bootstrap
    for k in range(sample_times):

      #prepare train & test sets
      #Sampling with replacement..whichever is not used in training data will be used in test data
      train = resample(df, random_state = k)

      #picking rest of the data not considered in training sample test = df - train
      test = pd.concat([df, train, train]).drop_duplicates(keep = False)

      train = np.array(train)
      test = np.array(test)

      #fit model
      model = CLS[j] # can change max_iter=1000
      model.fit(train[:,:-1], train[:,-1]) #model.fit(X_train,y_train) i.e model.fit(train set, train label as it is a classifier)
      #evaluate model
      predictions = model.predict(test[:,:-1]) #model.predict(X_test)

      perm_train_accurucy = PermutationImportance(model, random_state=0, scoring = 'accuracy', n_iter = 25).fit(train[:,:-1], train[:,-1]) #第一次是 roc_auc 导出文件不带标记 其余带标记
      perm_test_accuracy = PermutationImportance(model, random_state=0, scoring = 'accuracy', n_iter = 25).fit(test[:,:-1], test[:,-1])

      perm_train_precision = PermutationImportance(model, random_state=0, scoring = 'precision', n_iter = 25).fit(train[:,:-1], train[:,-1]) #第一次是 roc_auc 导出文件不带标记 其余带标记
      perm_test_precision = PermutationImportance(model, random_state=0, scoring = 'precision', n_iter = 25).fit(test[:,:-1], test[:,-1])

      perm_train_recall = PermutationImportance(model, random_state=0, scoring = 'recall', n_iter = 25).fit(train[:,:-1], train[:,-1]) #第一次是 roc_auc 导出文件不带标记 其余带标记
      perm_test_recall = PermutationImportance(model, random_state=0, scoring = 'recall', n_iter = 25).fit(test[:,:-1], test[:,-1])

      perm_train_f1 = PermutationImportance(model, random_state=0, scoring = 'f1', n_iter = 25).fit(train[:,:-1], train[:,-1]) #第一次是 roc_auc 导出文件不带标记 其余带标记
      perm_test_f1 = PermutationImportance(model, random_state=0, scoring = 'f1', n_iter = 25).fit(test[:,:-1], test[:,-1])



      accuracy = accuracy_score(test[:,-1], predictions) #accuracy_score(y_test, y_pred)
      precision = precision_score(test[:,-1], predictions)
      recall = recall_score(test[:,-1], predictions)
      f1 = f1_score(test[:,-1], predictions)
      auc = roc_auc_score(test[:,-1], predictions)
      mcc = matthews_corrcoef(test[:,-1], predictions)

      out_list_train_accuracy = []
      out_list_test_accuracy = []
      out_list_train_precision = []
      out_list_test_precision = []
      out_list_train_recall = []
      out_list_test_recall = []
      out_list_train_f1 = []
      out_list_test_f1 = []

      out_list_train_accuracy = [ReLink[i],str(CLS[j])+str(k)] + perm_train_accurucy.feature_importances_.tolist()
      out_list_test_accuracy = [ReLink[i],str(CLS[j])+str(k)] + perm_test_accuracy.feature_importances_.tolist()
      out_list_train_precision = [ReLink[i],str(CLS[j])+str(k)] + perm_train_precision.feature_importances_.tolist()
      out_list_test_precision = [ReLink[i],str(CLS[j])+str(k)] + perm_test_precision.feature_importances_.tolist()
      out_list_train_recall = [ReLink[i],str(CLS[j])+str(k)] + perm_train_recall.feature_importances_.tolist()
      out_list_test_recall = [ReLink[i],str(CLS[j])+str(k)] + perm_test_recall.feature_importances_.tolist()
      out_list_train_f1 = [ReLink[i],str(CLS[j])+str(k)] + perm_train_f1.feature_importances_.tolist()
      out_list_test_f1 = [ReLink[i],str(CLS[j])+str(k)] + perm_test_f1.feature_importances_.tolist()

      performance_list.append((ReLink[i],str(CLS[j])+str(k),accuracy,precision,recall,f1,auc,mcc))

      permutation_train_accuracy_list.append(out_list_train_accuracy)
      permutation_test_accuracy_list.append(out_list_test_accuracy)
      permutation_train_precision_list.append(out_list_train_precision)
      permutation_test_precision_list.append(out_list_test_precision)
      permutation_train_recall_list.append(out_list_train_recall)
      permutation_test_recall_list.append(out_list_test_recall)
      permutation_train_f1_list.append(out_list_train_f1)
      permutation_test_f1_list.append(out_list_test_f1)


print("end")
print(performance_list)
print(permutation_train_accuracy_list)
print(permutation_test_accuracy_list)
print(permutation_train_precision_list)
print(permutation_test_precision_list)
print(permutation_train_recall_list)
print(permutation_test_recall_list)

print(permutation_train_f1_list)
print(permutation_test_f1_list)

# save as csv files
out_file_train_accuracy_path = outfilepath + "ReLink-permutation-train-accuracy.csv"
out_file_test_accuracy_path = outfilepath + "ReLink-permutation-test-accuracy.csv"
out_file_train_precision_path = outfilepath + "ReLink-permutation-train-precision.csv"
out_file_test_precision_path = outfilepath + "ReLink-permutation-test-precision.csv"
out_file_train_recall_path = outfilepath + "ReLink-permutation-train-recall.csv"
out_file_test_recall_path = outfilepath + "ReLink-permutation-test-recall.csv"
out_file_train_f1_path = outfilepath + "ReLink-permutation-train-f1.csv"
out_file_test_f1_path = outfilepath + "ReLink-permutation-test-f1.csv"


setDir(out_file_train_accuracy_path)
setDir(out_file_test_accuracy_path)
setDir(out_file_train_precision_path)
setDir(out_file_test_precision_path)
setDir(out_file_train_recall_path)
setDir(out_file_test_recall_path)
setDir(out_file_train_f1_path)
setDir(out_file_test_f1_path)

out_columns = ["project","cls_boot"] + df_features[:-1]

out_file_train_accuracy = pd.DataFrame(permutation_train_accuracy_list,columns=out_columns)
out_file_test_accuracy = pd.DataFrame(permutation_test_accuracy_list,columns=out_columns)
out_file_train_precision = pd.DataFrame(permutation_train_precision_list,columns=out_columns)
out_file_test_precision = pd.DataFrame(permutation_test_precision_list,columns=out_columns)
out_file_train_recall = pd.DataFrame(permutation_train_recall_list,columns=out_columns)
out_file_test_recall = pd.DataFrame(permutation_test_recall_list,columns=out_columns)
out_file_train_f1 = pd.DataFrame(permutation_train_f1_list,columns=out_columns)
out_file_test_f1 = pd.DataFrame(permutation_test_f1_list,columns=out_columns)

out_file_train_accuracy.to_csv(out_file_train_accuracy_path,index=False,columns=out_columns)
out_file_test_accuracy.to_csv(out_file_test_accuracy_path,index=False,columns=out_columns)
out_file_train_precision.to_csv(out_file_train_precision_path,index=False,columns=out_columns)
out_file_test_precision.to_csv(out_file_test_precision_path,index=False,columns=out_columns)
out_file_train_recall.to_csv(out_file_train_recall_path,index=False,columns=out_columns)
out_file_test_recall.to_csv(out_file_test_recall_path,index=False,columns=out_columns)
out_file_train_f1.to_csv(out_file_train_f1_path,index=False,columns=out_columns)
out_file_test_f1.to_csv(out_file_test_f1_path,index=False,columns=out_columns)

#计算结束