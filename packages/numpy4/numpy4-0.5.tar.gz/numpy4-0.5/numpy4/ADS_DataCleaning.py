import pandas as pd
import numpy as np
df =pd.read_csv("loan_data_set.csv")
df

print(df["LoanAmount"].isnull().sum())


na_variables = [var for var in df.columns if df[var].isnull().mean() > 0]
#for finding null values in cols
na_variables


# mean imputation
df1 = df.copy()
df1
missing_col = ["LoanAmount"]

# for i in missing_col:
#   df1.loc[df1.loc[:,i].isnull(),i]=df1.loc[:,i].mean()

df1["LoanAmount"]=df1["LoanAmount"].fillna(df1["LoanAmount"].mean())
print(df1["LoanAmount"].isnull().sum())
df1




# median imputation
df2=df.copy()
# for i in missing_col:
#   df2.loc[df2.loc[:,i].isnull(),i]=df2.loc[:,i].median()

df2["LoanAmount"]=df2["LoanAmount"].fillna(df2["LoanAmount"].median())
print(df2["LoanAmount"].isnull().sum())
df2


# Mode imputation

df4 = df.copy()
df4
missing_col = ["LoanAmount"]

# for i in missing_col:
#   df4.loc[df4.loc[:,i].isnull(),i]=df4.loc[:,i].mode()

df4["LoanAmount"]=df4["LoanAmount"].fillna(df4["LoanAmount"].mode()[0])
print(df4["LoanAmount"].isnull().sum())
df4



#categorical to numerical

from sklearn.preprocessing import OrdinalEncoder

data=df.copy()
oe =OrdinalEncoder()
result = oe.fit_transform(data)
print(result)


#random sample
df5=df.copy()
# df5['LoanAmount'].dropna().sample(df5['LoanAmount'].isnull().sum(),random_state=0)
# df5



missing = df5.isnull().sum()

for col in df5.columns:
    if(missing[col] > 0):
        values = df5[col].dropna().values
        imputed_value = np.random.choice(values,size=missing[col])
        print(imputed_value)
        df5[col].loc[df5[col].isnull()] = imputed_value

print(df5["LoanAmount"].isnull().sum())
df5


# frequent category imputation
df6=df.copy()
m= df6["Gender"].mode()
m=m.tolist()

frq_imp = df6["Gender"].fillna(m[0])
frq_imp.unique()


#regression imputation
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
df1=df[["CoapplicantIncome","LoanAmount"]]
print(df1["LoanAmount"].isnull().sum())
print(df1["CoapplicantIncome"].isnull().sum())


# col=df1["LoanAmount"].dropna()
# df1.head()
testdf = df1[df1['LoanAmount'].isnull()]
testdf
traindf = df1[df1['LoanAmount'].isnull()==False]
traindf


lr.fit(traindf['LoanAmount'].values.reshape(-1, 1),traindf['CoapplicantIncome'])
# testdf.drop("LoanAmount",axis=1,inplace=True)
# testdf
pred = lr.predict(testdf['CoapplicantIncome'].values.reshape(-1, 1))
testdf['LoanAmount']= pred
print(df1["CoapplicantIncome"].isnull().sum())

print(pred)