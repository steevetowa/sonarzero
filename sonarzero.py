# -*- coding: utf-8 -*-
"""sonarzero.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZsjW-YDQHIY7mxfOEPADjbtiizbl0NeJ
"""



"""Presentation:

We are compiling the data from different datasets on US Car Insurance Claims in order train the model SonarZero built to predict if a car insurance application will be the object of a claim during the time period covered by the policy coverage or not.

Made by: Steeve Towa

Data Sources:

Main Data::

Vehicle Insurance Data:
https://www.kaggle.com/datasets/imtkaggleteam/vehicle-insurance-data
*   motor_data11-14lats.csv(29.24 MB)
*   motor_data14-2018.csv(50.78 MB)

Secondary Data::

Car Insurance Claim Data:
https://www.kaggle.com/datasets/xiaomengsun/car-insurance-claim-data
*   car_insurance_claim.csv(1.58 MB)


Insurance_claims:
https://www.kaggle.com/datasets/harshvardhan7695/insurance-claims
*   insurance_claims.csv(266.96 kB)

Dataset of an actual motor vehicle insurance portfolio:
https://data.mendeley.com/datasets/5cxyb5fp4f/2
*   Motor vehicle insurance data.csv(13.9 MB)


For the first version of the model SONARZERO will only use the main datasets to train the model. Then, we will process the secondary data to re-train the model and compare the accuracy.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

"""#1. Main File #1 : motor_data11-14lats.csv"""

df1 = pd.read_csv('/content/motor_data11-14lats.csv')
# df1.head()

# Customer sex has alredy been labelled as 0 for male, 1 for female and 2 for commercial
df1['SEX'].value_counts()

# Many varible/columns are without explanation. Only necessary and explanamble parameters will be kept, i.e: Insured_value, Prod_Year, Seat_Num, Carr_Cap, Type_Vehicle, Make, Usage and Claim_paid.
# We are making the assumption that all policies have a 1-year term
df1 = df1.drop(['INSR_BEGIN', 'INSR_END', 'EFFECTIVE_YR', 'INSR_TYPE','OBJECT_ID', 'CCM_TON'], axis=1)
# df1.head()

#Determining and handling missing values
df1.isnull().sum()

df1.shape

#We are dropping the few datapoints with no Premium, Usage.
df1.dropna(subset=['PREMIUM'], inplace=True)
df1.dropna(subset=['USAGE'], inplace=True)
df1.shape

df1.describe()

#We are now replacing the missing values for PROD_YEAR (with mean=2001), CLAIM_APID (with 0), CARR_CAP (with mean) and SEATS_NUM (with mean)
df1['PROD_YEAR'] = df1['PROD_YEAR'].replace('NaN', pd.NA).fillna(2001).astype(int)
df1['CLAIM_PAID'] = df1['CLAIM_PAID'].replace('NaN', pd.NA).fillna(0).astype(int)
df1['CARRYING_CAPACITY'].fillna(df1['CARRYING_CAPACITY'].mean(), inplace=True)
df1['SEATS_NUM'].fillna(df1['SEATS_NUM'].mean(), inplace=True)
df1.isnull().sum()

df1.tail()

df1.shape

df0 = df1 #backup data

#We are removing lines where the insured value is 0
df1 = df1.drop(df1[df1['INSURED_VALUE'].isnull()].index)
df1.shape

#We are creating a 'Target' Column for a binary value to know if a claim has been paid or not, then we drop the Claim column
df1['Target'] = df1['CLAIM_PAID']

mask = df1['Target'] != 0
df1.loc[mask, 'Target'] = 1

df1 = df1.drop(['CLAIM_PAID'], axis=1)
df1.head()

df1.describe()

#About 7.7% of the applications result in claims.
df0=df1
df1.to_csv('df1.csv', index=False)

"""#2. Main File #2: motor_data14-2018.csv"""

df2 = pd.read_csv('/content/motor_data14-2018.csv')
#df2.head()

#We run the same data process as df1
df2 = df2.drop(['INSR_BEGIN', 'INSR_END', 'EFFECTIVE_YR', 'INSR_TYPE','OBJECT_ID', 'CCM_TON'], axis=1)
df2.dropna(subset=['PREMIUM'], inplace=True)
df2.dropna(subset=['USAGE'], inplace=True)
df2['PROD_YEAR'] = df2['PROD_YEAR'].replace('NaN', pd.NA).fillna(2001).astype(int)
df2['CLAIM_PAID'] = df2['CLAIM_PAID'].replace('NaN', pd.NA).fillna(0).astype(int)
df2['CARRYING_CAPACITY'].fillna(df2['CARRYING_CAPACITY'].mean(), inplace=True)
df2['SEATS_NUM'].fillna(df2['SEATS_NUM'].mean(), inplace=True)
df00=df2 #backup data
df2 = df2.drop(df2[df2['INSURED_VALUE'].isnull()].index)
df2['Target'] = df2['CLAIM_PAID']
mask = df2['Target'] != 0
df2.loc[mask, 'Target'] = 1
df2 = df2.drop(['CLAIM_PAID'], axis=1)
df00=df2
df2.describe()

#About 8.4% of the applications result in claims.
df00=df2
df2.to_csv('df2.csv', index=False)	#exporting the data

#We are now merging both main dataframes
frames = [df1, df2]
main_df = pd.concat(frames)
main_df.shape

#Let's examine the new dataset
main_df.describe()

#A last, this specific dataset shows that about 8% of applications ends up in one or multiple claims
df0 = main_df #backup the main data
main_df.to_csv('main_df.csv', index=False)	#exporting the data

"""#3. Training SONARZERO"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

main_df.head()

"""Turning string data into numeric data with label encoding"""

from sklearn.preprocessing import LabelEncoder

#Sorting and counting the non-numerical data
#Sorting TYPE_VEHICLE for labelling
main_df['TYPE_VEHICLE'].value_counts()

main_df['TYPE_VEHICLE'].value_counts().shape

#TYPE_VEHICLE Legend
tv_list = main_df['TYPE_VEHICLE'].sort_values().values

list1 = list(dict.fromkeys(tv_list))
x = np.arange(0,12,1)

tv_values = pd.DataFrame(list1, columns=['TV'])
x_label = pd.DataFrame(x, columns=['Labels'])

tv_legend = pd.concat([x_label, tv_values], axis=1)

print(tv_legend)

tv_legend.shape

#Sorting USAGE for labelling
main_df['USAGE'].value_counts()

main_df['USAGE'].value_counts().shape

#USAGE Legend
usage_list = main_df['USAGE'].sort_values().values

list1 = list(dict.fromkeys(usage_list))
x = np.arange(0,15,1)

usage_values = pd.DataFrame(list1, columns=['usage'])
x_label = pd.DataFrame(x, columns=['Labels'])

usage_legend = pd.concat([x_label, usage_values], axis=1)

print(usage_legend)

usage_legend.shape

#Sorting and counting Make for labelling
main_df['MAKE'].value_counts()

main_df['MAKE'].value_counts().shape

#MAKE legend
make_list = main_df['MAKE'].sort_values().values

list1 = list(dict.fromkeys(make_list))
x = np.arange(0,798,1)

make_values = pd.DataFrame(list1, columns=['make'])
x_label = pd.DataFrame(x, columns=['Labels'])

make_legend = pd.concat([x_label, make_values], axis=1)

print(make_legend)

make_legend.shape

#Setup the labelling process
label_encode = LabelEncoder()

#Encoding the selected columns data with new labels
tv_labels = label_encode.fit_transform(main_df.TYPE_VEHICLE)
usage_labels = label_encode.fit_transform(main_df.USAGE)
make_labels = label_encode.fit_transform(main_df.MAKE)

#Appending the new label to the DataFrame
main_df['tv'] = tv_labels
main_df['usage'] = usage_labels
main_df['make'] = make_labels

main_df.head()

#Dropping the non-numerical columns
main_df = main_df.drop(['TYPE_VEHICLE', 'USAGE', 'MAKE'], axis=1)

print(main_df)

#Representing the target by group
main_df.groupby('Target').mean()

#A lot of insights can be driven from the above table regarding the parameters leading to a specific target
#All labelled parameters (tv,usage and make) cannot provide insights from the mean table

"""Training and test data:

"""

# separating data and labels
X = main_df.drop(['Target'], axis=1)
Y = main_df['Target']

print(X)
print(Y)

#preparing the data for the model
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, stratify=Y, random_state=1)

#checking the size split
print(X.shape, X_train.shape, X_test.shape)

#Applying the Logistic Regression Model to the data
model = LogisticRegression()

#Training the logisitic regression model with training data
model.fit(X_train, Y_train)

#creating our sonarzero model and checkinng its accuracy on the training data
sonarzero_train_prediction = model.predict(X_train)
sonarzero_train_accuracy = accuracy_score(sonarzero_train_prediction, Y_train)

print('SonarZero Accuracy on training data: ', sonarzero_train_accuracy)

#accuracy on the testing data
sonarzero_test_prediction = model.predict(X_test)
sonarzero_test_accuracy = accuracy_score(sonarzero_test_prediction, Y_test)

print('SonarZero Accuracy on test data: ', sonarzero_test_accuracy)

#92.4% accuracy on training and test data is very good for the sonarzero model