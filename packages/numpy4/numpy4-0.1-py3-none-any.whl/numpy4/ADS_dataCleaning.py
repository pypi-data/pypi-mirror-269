import pandas as pd
import numpy as np
df =pd.read_csv("/content/loan_data_set.csv")
df

na_variables = [ var for var in df.columns if df[var].isnull().mean() > 0 ]
#for finding null values in cols
na_variables

# mean imputation
df1 = df
df1
missing_col = ["LoanAmount"]

for i in missing_col:
  df1.loc[df1.loc[:,i].isnull(),i]=df1.loc[:,i].mean()

df1


# median imputation
df2=df
for i in missing_col:
  df2.loc[df2.loc[:,i].isnull(),i]=df2.loc[:,i].median()

df2

# Mode imputation

df4 = df
df4
missing_col = ["LoanAmount"]

for i in missing_col:
  df4.loc[df4.loc[:,i].isnull(),i]=df4.loc[:,i].mode()

df4


#categorical to numerical 

from sklearn.preprocessing import OrdinalEncoder

data=df
oe =OrdinalEncoder()
result = oe.fit_transform(data)
print(result)

#random sample
df5=df
df5['LoanAmount'].dropna().sample(df5['LoanAmount'].isnull().sum(),random_state=0)
df5

# frequent category imputation
df6=df
m= df6["Gender"].mode()
m=m.tolist()

frq_imp = df6["Gender"].fillna(m[0])
frq_imp.unique()


#regression imputation
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
df1=df[["CoapplicantIncome","LoanAmount"]]


# col=df1["LoanAmount"].dropna()
# df1.head()
testdf = df1[df1['LoanAmount'].isnull()==True]
testdf
traindf = df1[df1['LoanAmount'].isnull()==False]
traindf


lr.fit(traindf['LoanAmount'],traindf['CoapplicantIncome'])
# testdf.drop("LoanAmount",axis=1,inplace=True)
# testdf
pred = lr.predict(testdf)
# testdf['LoanAmount']= pred

