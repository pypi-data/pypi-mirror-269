import pandas as pd
import numpy as np
# from google.colab import drive
# drive.mount('/content/drive')
df = pd.read_csv('ADS Datasets/supermarket_sales - Sheet1.csv')


df.head()



#Scatter plot
import matplotlib.pyplot as plt
plt.scatter(df['Tax 5%'], df['Unit price'], c ="blue")


#BoxPlot

ax = df[[ 'Tax 5%','gross income','Rating']].plot(kind='box', title='boxplot')



#Distribution Chart / Distplot
import seaborn as sns

g=sns.distplot(df['Total'])


#JoinPlot
sns.jointplot(x ='Total', y ='Tax 5%', data = df)


#Pairplot
sns.pairplot(df)
# to show
plt.show()


# Histogram
df['Rating'].hist()
plt.show()


lst = df['Product line'].unique()
print(lst)

print(df[df['Product line']=='Electronic accessories'].count())


t=[23,17,35,29,12,41]
plt.pie(t,labels=lst,autopct ='% 1.1f %%', shadow = True)
plt.show()


#Density Chart
df['Rating'].plot.density(color='green')
plt.title('Density plot for Speeding')
plt.show()


#scatter Matrix
pd.plotting.scatter_matrix(df)


# rugplot
import seaborn as sns
import matplotlib.pyplot as plt
data = df
data.head(5)
plt.figure(figsize=(15,5))
sns.rugplot(data=data, x ="Total")
plt.show()



#column chart
# plot between 2 attributes
df1 = df.head(10)
df1.plot.bar()
plt.bar(df1['Gender'], df1['Total'])
plt.xlabel("Gender")
plt.ylabel("Total")
plt.show()



import plotly.express as px
df1=df.head(15)
fig = px.line(df1, x="Date", y="Total", color='City')
fig.show()


#Bubble Chart
import plotly.express as px

fig = px.scatter(df1, x="Total", y="Tax 5%", size="Quantity", color="City", hover_name="Product line", log_x=True, size_max=60)
fig.show()



#Parallel
import plotly.express as px
df1 =df.sample(n=100)
fig = px.parallel_coordinates(df1, color="Total",
                              dimensions=['Quantity','Unit price','Rating',],
                              color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)
fig.show()


# Creating Andrews curves
df1 = df[['Quantity','Total','Rating']]
df1=df1.sample(n=50)
x = pd.plotting.andrews_curves(df1,'Rating')
 
# plotting the Curve
x.plot()
 
# Display
plt.show()



import plotly.express as px

# df = px.data.medals_wide(indexed=True)
fig = px.imshow(df1)
fig.show()


import plotly.express as px

fig = px.line(df1, x='Date', y="Total")
fig.show()