# -*- coding: utf-8 -*-
"""CREDIT CARD FRAUD

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zH8CHy7NJIROOKzepMsVEHeaNpkmGJyP
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sklearn
import numpy as np


# %matplotlib inline

df = pd.read_csv("creditcard.csv")

print(df.shape)

"""### null or missing values"""

df.isnull().sum()

df.info()

df.describe().round()

"""### Statistical information in each class"""

print ('Not Fraud % ',round(df['Class'].value_counts()[0]/len(df)*100,2))
print ()
print (round(df.Amount[df.Class == 0].describe(),2))
print ()
print ()
print ('Fraud %    ',round(df['Class'].value_counts()[1]/len(df)*100,2))
print ()
print (round(df.Amount[df.Class == 1].describe(),2))

fig = plt.figure(figsize=(12,5.5))
ax1 = fig.add_subplot(1, 2, 1)
sns.countplot(x=df['Class'],data=df,saturation=1,hue='Class')



ax2 = fig.add_subplot(1, 3, 3)
plt.pie(df['Class'].value_counts(),labels=['Genuine','Fraud'],radius=1.8,colors = ['green','white'],
    autopct='%1.2f%%',pctdistance=1.4 ,labeldistance=1.15,startangle = 20,)

plt.legend(title = 'Transactions',loc='upper right', bbox_to_anchor=(1.7,1.4))
plt.show()

"""*The average value of fraud transactions is greater than normal transactions.

Thus,it is a unbalanced datatset. accuracy isn’t a good measure when working with imbalanced datasets.
Low precision indicates a high number of false positives(non fraudulent classified as fraud).
Low recall indicates a high number of false negatives(fraud classified as non fraudulent).
Thus,1 score is a good metric
"""

df.dropna(axis=0,inplace=True)
df.isnull().sum()

feature_names = df.iloc[:, 1:30].columns
target = df.iloc[:1, 30:].columns

data_features = df[feature_names]
data_target = df[target]



feature_names

target

from sklearn.model_selection import train_test_split
np.random.seed(123)
X_train, X_test, y_train, y_test = train_test_split(data_features, data_target,
                                                    train_size = 0.70, test_size = 0.30, random_state = 1)

X_train.isnull().sum()

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

lr.fit(X_train, y_train)

def PrintStats(cmat, y_test, pred):
    tpos = cmat[0][0]
    fneg = cmat[1][1]
    fpos = cmat[0][1]
    tneg = cmat[1][0]

def RunModel(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train.values.ravel()) ##The numpy.ravel() functions returns contiguous flattened array(1D array with all the input-array elements and with the same type as it). A copy is made only if needed.
    pred = model.predict(X_test)
    matrix = confusion_matrix(y_test, pred)
    return matrix, pred

pip install scikit-plot

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
import scikitplot as skplt

cmat, pred = RunModel(lr, X_train, y_train, X_test, y_test)

import scikitplot as skplt
skplt.metrics.plot_confusion_matrix(y_test, pred)

accuracy_score(y_test, pred)

print (classification_report(y_test, pred))

# The function "len" counts the number of classes = 1 and saves it as an object "fraud_records"
fraud_records = len(df[df.Class == 1])

# Defines the index for fraud and non-fraud in the lines:
fraud_indices = df[df.Class == 1].index   #find index of all frauds
not_fraud_indices = df[df.Class == 0].index

# Randomly collect equal samples of each type:
under_sample_indices = np.random.choice(not_fraud_indices, fraud_records, False) #randomly collect say 100 non frauds
df_undersampled = df.iloc[np.concatenate([fraud_indices, under_sample_indices]),:] #now sample is 100fraud,nonfraud
X_undersampled = df_undersampled.iloc[:,1:30]
Y_undersampled = df_undersampled.Class
X_undersampled_train, X_undersampled_test, Y_undersampled_train, Y_undersampled_test = train_test_split(X_undersampled, Y_undersampled, test_size = 0.30)

lr_undersampled = LogisticRegression()
cmat, pred = RunModel(lr_undersampled, X_undersampled_train, Y_undersampled_train, X_undersampled_test, Y_undersampled_test)
PrintStats(cmat, Y_undersampled_test, pred)

skplt.metrics.plot_confusion_matrix(Y_undersampled_test, pred)

##false positive =7 false neg=12=>>>decerased from 57 ***=>> recall increased(fraud classified as non fraud)

accuracy_score(Y_undersampled_test, pred)

print (classification_report(Y_undersampled_test, pred))

"""Accuracy has decreased, but sensitivity has greatly increased. Looking at the confusion matrix, we can see a much higher percentage of correct classifications of fraudulent data.

Unfortunately, a greater number of fraud classifications almost always means a correspondingly greater number of valid transactions also classified as fraudulent.
"""



# accuracy_score(y_test, pred)

"""The algorithm was much better at capturing fraudulent transactions (61 classification errors at the beginning of the project to 12 current), but much worse at incorrectly labeling valid transactions (15 to 2857)."""

from sklearn import metrics

clf = LogisticRegression(C=1, penalty='l2')
clf.fit(X_undersampled_train, Y_undersampled_train)
y_pred = clf.predict(X_test)

y_pred_probability = clf.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_probability)
auc = metrics.roc_auc_score(y_test, pred)
plt.plot(fpr,tpr,label="LogisticRegression, auc="+str(auc))
plt.legend(loc=4)
plt.show()

#Decision Tree Model

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
classes_names = ['Not Fraud', 'Fraud']

DecisionTreeModel = DecisionTreeClassifier(criterion='gini',max_depth=5,random_state=33) #criterion can be entropy
DecisionTreeModel.fit(X_train, y_train)
DecisionTreeModel_y_pred = DecisionTreeModel.predict(X_test)


#Score
DecisionTreeModel_TrainScore =  round(DecisionTreeModel.score(X_train, y_train) * 100, 2)
DecisionTreeModel_TestScore = round(DecisionTreeModel.score(X_test, y_test) * 100, 2)

print('Decision Tree Train Score: ' , DecisionTreeModel_TrainScore)
print('Decision Tree Test Score: ' , DecisionTreeModel_TestScore)


#Confusion Matrix
DecisionTreeModel_CM = confusion_matrix(y_test, DecisionTreeModel_y_pred)
DecisionTreeModel_ConfusionMatrix = pd.DataFrame(DecisionTreeModel_CM, index=classes_names, columns=classes_names)

sns.heatmap(DecisionTreeModel_ConfusionMatrix, annot=True, cbar=None, cmap="Blues", fmt = 'g')
plt.title("Decision Tree Confusion Matrix"), plt.tight_layout()
plt.ylabel("True Class"), plt.xlabel("Predicted Class")
plt.show()

#Random Forest Model
RandomForestModel = RandomForestClassifier(criterion = 'gini',n_estimators=200,max_depth=5,random_state=33, n_jobs=-1)
RandomForestModel.fit(X_train, y_train)
RandomForestModel_y_pred = RandomForestModel.predict(X_test)


#Score
RandomForestModel_TrainScore =  round(RandomForestModel.score(X_train, y_train) * 100, 2)
RandomForestModel_TestScore = round(RandomForestModel.score(X_test, y_test) * 100, 2)

print('RandomForestModel Train Score: ' , RandomForestModel_TrainScore)
print('RandomForestModel Test Score: ' , RandomForestModel_TestScore)


#Confusion Matrix
RandomForestModel_CM = confusion_matrix(y_test, RandomForestModel_y_pred)
RandomForestModel_ConfusionMatrix = pd.DataFrame(RandomForestModel_CM, index=classes_names, columns=classes_names)

sns.heatmap(RandomForestModel_ConfusionMatrix, annot=True, cbar=None, cmap="Greens", fmt = 'g')
plt.title("Random Forest Confusion Matrix"), plt.tight_layout()
plt.ylabel("True Class"), plt.xlabel("Predicted Class")
plt.show()

from sklearn import ensemble
ada = ensemble.AdaBoostClassifier()
ada.fit(X_train,y_train)

ada_pred = ada.predict(X_test)

print("Traing Score:%f"%ada.score(X_train,y_train))
print("Testing Score:%f"%ada.score(X_test,y_test))


from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
print(accuracy_score(y_test,ada_pred))
print(classification_report(y_test,ada_pred))
print(confusion_matrix(y_test,ada_pred))

Ada_ConfusionMatrix = pd.DataFrame(confusion_matrix(y_test,ada_pred), index=classes_names, columns=classes_names)
sns.heatmap(Ada_ConfusionMatrix, annot=True, cbar=None, cmap="Greens", fmt = 'g')
plt.title("Ada Boost Confusion Matrix"), plt.tight_layout()
plt.ylabel("True Class"), plt.xlabel("Predicted Class")
plt.show()

