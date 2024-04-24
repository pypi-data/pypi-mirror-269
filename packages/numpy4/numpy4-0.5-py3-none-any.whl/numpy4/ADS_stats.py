import pandas as pd
import numpy as np
# from google.colab import drive
# drive.mount('/content/drive')


df = pd.read_csv(f'/content/supermarket_sales - Sheet1.csv')
df.head()


#Mean SD LQ UQ max min
df.describe()


#Count of null values
df.info()


#Median
df.select_dtypes(include=['number']).median()


#Mode
print(df['Product line'].mode())
print(df['City'].mode())
print(df['Payment'].mode())
print(df['Customer type'].mode())
print(df['Gender'].mode())


#Scatter plot
import matplotlib.pyplot as plt
plt.scatter(df['Tax 5%'], df['Unit price'], c ="blue")


import matplotlib.pyplot as plt
plt.scatter(df['gross income'], df['Unit price'], c ="blue")

import matplotlib.pyplot as plt
plt.scatter(df['Quantity'], df['Total'], c ="blue")

#Box plot
x2=df['Tax 5%']
x4=df['gross income']
x5=df['Rating']
data = pd.DataFrame({ "Tax 5%": x2,"gross income": x4,"Rating": x5})

# Plot the dataframe
ax = data[[ 'Tax 5%','gross income','Rating']].plot(kind='box', title='boxplot')



plt.boxplot(df['Total'])


#Trimmed mean
from scipy import stats
stats.trim_mean(df['Total'], 0.1)


#Summation

df['Total'].sum()

#Frequency
count = df['Product line'].value_counts()
print(count)

#Variance
df.select_dtypes(include=['number']).var()

#Correlation matrix
df.select_dtypes(include=['number']).corr()

#Standard error of mean
df.select_dtypes(include=['number']).sem()

#sum of squares
sos=0
for val in df['Total']:
  sos=val*val+sos
print(sos)

#Skewness
df.select_dtypes(include=['number']).skew()

#kurtosis
sr = pd.Series(df['Total'])
print(sr.kurtosis())

import seaborn as sns

g=sns.distplot(df['Total'])

