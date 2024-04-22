import pandas as pd
import numpy as np
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/My Drive/ADS/supermarket_sales - Sheet1.csv')


df.head()


from re import S
import math as m
#  we will do a hypothesis on total as total amount can be above a certain amount
# z test when pop size > 30  and t test will be when  pop size<30

#  Null hypo will be that total amt <= 250
#  alternate hypo will total amt > 250
df1 = df.sample(n=28)
df2=df.sample(n=100)

#sample size
nt = len(df1)
nz= len(df2)

#sample mean
x_bar_t= df1["Total"].mean()
x_bar_z= df2["Total"].mean()

# Population size
n=len(df)

# pop mean
meu = df["Total"].mean()

# STANDARD DEVIATION
s_t = df1["Total"].std()
s_z = df2["Total"].std()
sigma = df["Total"].std()


#  formula for Z test
print("for Z test")
Z_SCORE = (x_bar_z-meu)/(sigma/m.sqrt(nz))
# Z_SCORE = round(Z_SCORE,1)
print(Z_SCORE)
alpha = 0.05

critical_val = 1.65 #VALUE FOR RIGHT TAIL AND SIGNIFICANCE 
#  if z score is greater than critical val then reject null hypothesis
if Z_SCORE > critical_val:
  print("We reject Null Hypothesis")
else :
  print("We Do NOT REJECT Null Hypothesis")


#  formula for T test

print("for T test")
T_SCORE = (x_bar_t-meu)/(s_t/m.sqrt(nt))
# T_SCORE = round(T_SCORE,1)
print(T_SCORE)
alpha = 0.05

critical_val = 1.703 # N-1 =27 AND 0.05 KA INTERSECTION
#  if z score is greater than critical val then reject null hypothesis
if T_SCORE > critical_val:
  print("We reject Null Hypothesis")
else :
  print("We Do NOT REJECT Null Hypothesis")


# FOR 2 SMPLE TEST  WE CAN CREATE  DATA FRAME FOR MEN AND WOMEN ON GENDER FOR Quantity

# Two sample Independent T Test
men_arr=[]
women_arr=[]
import statistics ,math
#  for t test
for i in range(29):
  if df["Gender"][i]=="Female":
    women_arr.append(df["Quantity"][i])
  else:
    men_arr.append(df["Quantity"][i])

# means
men_mean= statistics.fmean(men_arr)
women_mean= statistics.fmean(women_arr)

# print(men_mean)
# print(women_mean)

#std dev if xbar is not given then std dev for both men and women comes out to be same
men_std = statistics.stdev(men_arr,xbar=men_mean)
women_std = statistics.stdev(women_arr,xbar=women_mean)
# print(men_std)
# print(women_std)

# lengths
men_len = len(men_arr)
women_len =len(women_arr)

# formula  

lower = math.sqrt((1/men_len)+(1/women_len))
s = math.sqrt((((men_len-1)*men_std*men_std)+((women_len-1)*women_std*women_std))/(men_len+women_len-2))
print(s)

T_SCORE = abs(men_mean-women_mean)/(s*lower)
print(T_SCORE)
# tscore cross verified by hand calc

degree_freedom = men_len+women_len-2
# we check degree_freedom=27 and alpha = 0.05
tcritical = 1.703

if T_SCORE > tcritical:
  print("We reject Null Hypothesis")
else :
  print("We Do NOT REJECT Null Hypothesis")


# Two sample Independent Z Test 
# null hypo = meu2>meu1
# alternate hypo =meu1 > meu2 so right tailed test at alpha = 0.05

men_arr=[]
women_arr=[]
import statistics ,math
#  for t test
for i in range(100):
  if df["Gender"][i]=="Female":
    women_arr.append(df["Quantity"][i])
  else:
    men_arr.append(df["Quantity"][i])

# means
men_mean= statistics.fmean(men_arr)
women_mean= statistics.fmean(women_arr)

# print(men_mean)
# print(women_mean)

#std dev if xbar is not given then std dev for both men and women comes out to be same
men_std = statistics.stdev(men_arr,xbar=men_mean)
women_std = statistics.stdev(women_arr,xbar=women_mean)
# print(men_std)
# print(women_std)

# lengths
men_len = len(men_arr)
women_len =len(women_arr)

# formula  x1-x2/s

lower = math.sqrt((men_std*men_std/men_len)+(women_std*women_std/women_len))

Z_SCORE = abs(men_mean-women_mean)/lower
print(Z_SCORE)

Zcritical = 1.645

if Z_SCORE > Zcritical:
  print("We reject Null Hypothesis")
else :
  print("We Do NOT REJECT Null Hypothesis")