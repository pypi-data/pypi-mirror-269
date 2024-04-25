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






# ************************************* SECOND METHOD *************************************

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import pandas as pd

df = pd.read_csv("london_weather.csv")
df.head()

df = df.fillna(df.mean())
print("After filling NUll values")
print(df.head())

df.describe()

sunshine_median = df['sunshine'].median()
transform = lambda x: 1 if x>=sunshine_median else 0
df['sunshine'] = df['sunshine'].apply(transform)

X = df.drop(['sunshine', 'date'], axis='columns')

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_sc = scaler.fit_transform(X)
print(X_sc)
df_scaled = pd.DataFrame(X_sc, columns=X.columns)
print(df_scaled.head())

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
target = df['sunshine']

X_train, X_test, y_train, y_test = train_test_split(df_scaled, target, train_size=0.8)


model = KNeighborsClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, roc_auc_score

import math

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("True Negatives {}".format(tn))
print("False Negatives {}".format(fn))
print("True Positives {}".format(tp))
print("False Positives {}".format(fp))
print()
print("Accuracy:", ((tp+tn)/(tp+tn+fp+fn)))
print("Error Rate:", ((fp+fn)/(tp+tn+fp+fn)))
PRC=(tp/(tp+fp))
print("Precision:", PRC)
SNS=(tp/(tp+fn))
SPC=(tn/(tn+fp))
print("Sensitivity:", SNS)
print("Specificity:", SPC)
print("ROC area under the curve score:", math.sqrt((SNS**2+SPC**2)/2))
print("F1 Score:", (2*PRC*SNS/(PRC+SNS)))
print("Geometric Mean:", math.sqrt(SNS*SPC))

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
fpr, tpr, thresholds = roc_curve(y_test, y_pred)
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()



X = df_scaled.min_temp
y = df_scaled.max_temp

corr, _ = pearsonr(X, y)
print("Karl Pearson's coefficient of correlation:", corr)

reg = LinearRegression()
X = X.values
X = X.reshape(-1, 1)
reg.fit(X, y)
y_pred = reg.predict(X)

r_squared = r2_score(y, y_pred)
print("R-squared:", r_squared)

mse = mean_squared_error(y, y_pred)
print("Mean Squared Error:", mse)

rmse = math.sqrt(mse)
print("RMSE:", rmse)

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y, y_pred)
print("MAE:", mae)

print("MAPE:", mae*100, end="%")