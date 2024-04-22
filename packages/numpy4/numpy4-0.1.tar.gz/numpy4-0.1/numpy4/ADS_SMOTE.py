from imblearn.over_sampling import SMOTE
from matplotlib import pyplot
from numpy import where
import pandas as pd

df = pd.read_csv('Churn_Modelling.csv')
df.head()


import seaborn as sns

data = df[['CreditScore', 'Age', 'Exited',]]
print(data.head(10))
sns.scatterplot(data = data, x ='CreditScore', y = 'Age', hue = 'Exited')


from sklearn.preprocessing import LabelEncoder
for col in df.columns:
  if df[col].dtype == 'O':
    label_encode = LabelEncoder()
    df[col] = label_encode.fit_transform(df[col])
df


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
#Splitting the data
from sklearn.tree import DecisionTreeClassifier
X_train, X_test, y_train, y_test = train_test_split(df.drop('Exited',axis=1), df['Exited'], test_size = 0.2, random_state = 101)


clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)
print(classification_report(y_test, y_pred))


smote = SMOTE(sampling_strategy='auto',k_neighbors=5,random_state = 101)
X_oversample, y_oversample = smote.fit_resample(X_train, y_train)


clf.fit(X_oversample,y_oversample)
y_predo=clf.predict(X_test)
print(classification_report(y_test, y_predo))


classifier = LogisticRegression()
classifier.fit(X_train, y_train)

print(classification_report(y_test, classifier.predict(X_test)))


classifier.fit(X_oversample, y_oversample)
print(classification_report(y_test, classifier.predict(X_test)))


smote = SMOTE(random_state = 101)
X, y = smote.fit_resample(df[['CreditScore', 'Age']], df['Exited'])
#Creating a new Oversampling Data Frame
df_oversampler = pd.DataFrame(X, columns = ['CreditScore', 'Age'])
df_oversampler['Exited']=y
print(df_oversampler.head())

sns.countplot(data=df_oversampler,x='Exited')


from collections import Counter
X=df[['CreditScore', 'Age']]
y=df['Exited']

oversample = SMOTE()
X, y = oversample.fit_resample(X, y)
# summarize the new class distribution
counter = Counter(y)
print(counter)


sns.scatterplot(data = df_oversampler, x ='CreditScore', y = 'Age', hue = 'Exited')