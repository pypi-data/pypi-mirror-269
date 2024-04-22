from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


dataset = datasets.load_breast_cancer()
X = dataset.data
y = dataset.target


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


clf_tree = DecisionTreeClassifier()
clf_tree.fit(X_train, y_train); 


y_pred = clf_tree.predict(X_test)
print(y_pred)


from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(y_test,y_pred).ravel()
print("True Negatives {}".format(tn))
print("False Negatives {}".format(fn))
print("True Positives {}".format(tp))
print("False Positives {}".format(fp))


acc = (tn+tp)/(tn+tp+fn+fp)
print("Accuracy {}".format(acc))


error_rate = (fn+fp)/(tn+tp+fn+fp)
print("Error Rate {}".format(error_rate))


precision = tp/(tp+fp)
print("Precision {}".format(precision))


sns = tp/(tp+fn)
spc = tn/(tn+fp)
print("Sensitivity {}".format(sns))
print("Specificity {}".format(spc))


import math
roc = math.sqrt((sns*sns)+(spc*spc))/math.sqrt(2)
print("ROC {}".format(roc))


GM = math.sqrt(sns*spc)
print("Geometric Mean {}".format(GM))


f1 = (2*sns*precision)/(precision+sns)
print("f1 score {}".format(f1))


fpr = 1-spc
fnr = 1 -sns
power = 1 - fnr
print("False positive Rate {}".format(fpr))
print("false negative Rate {}".format(fnr))
print("Power {}".format(power))


from sklearn.metrics import roc_curve, roc_auc_score
false_positive_rate1, true_positive_rate1, threshold1 = roc_curve(y_test, y_pred)
print('roc_auc_score for DecisionTree: ', roc_auc_score(y_test, y_pred))


import matplotlib.pyplot as plt
plt.subplots(1, figsize=(10,10))
plt.title('Receiver Operating Characteristic - DecisionTree')
plt.plot(false_positive_rate1, true_positive_rate1)
plt.plot([0,1],ls='--')
plt.plot([0,0],[0,1],c='.7')
plt.plot([1,1],c='.7')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


from google.colab import files
import io
import pandas as pd
import numpy as np
uploaded = files.upload()
df = pd.read_excel(io.BytesIO(uploaded['regdata.xlsx']))


import seaborn as sns
df2 = df[['Price','Dem']]
#rho=df2['Price'].corr(df2['Demand'])
df2['naturalLogPrice'] = np.log(df2['Price'])
df2['naturalLogDemand'] = np.log(df2['Dem'])

sns.regplot(x="naturalLogPrice", y="naturalLogDemand", data=df2, fit_reg=True)


X=df2[['naturalLogPrice']]
y=df2['naturalLogDemand']


from sklearn.linear_model import LinearRegression

model= LinearRegression()
model.fit(X,y)
y_pred = model.predict(X)
print(y_pred)


from scipy.stats import pearsonr
list1 = df2['naturalLogPrice']
list2 = df2['naturalLogDemand']
 

corr, _ = pearsonr(list1, list2)
print('Pearsons correlation: %.3f' % corr)


a = np.sum((y-y_pred)**2)
n =np.size(y)

mse = a/n
print("Mean Squared Error",mse)


rmse = math.sqrt(mse)
print("Root Mean Squared Error ",rmse)


q = np.sum((y-y_pred)**2)
my = np.sum(y)/n
mx =np.sum(X)/n
p = np.sum((y-my)**2)

R2 = 1-(q/p)
print("Coefficient of Determination ",R2)


b = np.sum(((y-y_pred)/y)**2)
rmsre = math.sqrt(b/n)
print("Root Mean Squared Relative Error ",rmsre)


a = np.sum(abs(y-y_pred))
n =np.size(y)

mae = a/n
print("Mean Absolute Error ",mae)


b = np.sum(abs((y-y_pred)/y))
mape = (100*b)/n
print("Mean absolute Percentage Error",mape)