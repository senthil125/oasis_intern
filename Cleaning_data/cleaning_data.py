# -*- coding: utf-8 -*-
"""Cleaning_data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E3lrFZ-m64BKH9LZbgCuq4GhrF8K1Uaw
"""

import pandas as pd
import numpy as np
#Load dataset
ds=pd.read_csv(r"/content/AB_NYC_2019.csv")

from google.colab import drive
drive.mount('/content/drive')

#Data Intergeration
print("Data integrity and initial inspection:")
print(ds.info())#display columns and non-null values count
print("\n no of rows and column in the dataset:",ds.shape)#no of rows and columns

#Missing data handling:
print("\nMissing data handling:")
print("Checking is there any missing values:",ds.isnull().sum())

#missing values are in name,hostname,lastreview,reviewpermonth columns

#There are only very few missing values in  name and hostname columns so drop it
print('\nHandling missing values name and host_name')
#Hanlding name
print("\nbefore dropping no of rows in name:",ds['name'].shape)
#dropna: it drop the missing value row and its corresponding rows also
ds.dropna(subset=['name'], inplace=True)
print("\nafter dropping no of rows in name:",ds['name'].shape)

#Handling host_name
print("\nbefore dropping no of rows in host_name:",ds['host_name'].shape)
ds.dropna(subset=['host_name'], inplace=True)
print("\nafter dropping no of rows in host_name:",ds['host_name'].shape)

#Handling last_review and reviews_per_month
print("\n Handling missing values of last_review and reviews_per_month")

print("\n no of rows in last_review column before filling missing values:",ds['last_review'].count())
print("\n no of rows in reviews_per_month column before filling missing values:",ds['reviews_per_month'].count())

#Forward Fill (ffill) is generally more appropriate if the dates represent events that should carry over until a new event occurs
#last review date remains the same until the next review, so use ffill
ds['last_review'].fillna(method='ffill', inplace=True)

# Convert 'last_review' to datetime format to ensure that it is correct datetime format
ds['last_review'] = pd.to_datetime(ds['last_review'])

#Replacing missing value with mode because it give least mse(mean_square_error) comparing to mean,median,ffill and bfill
mode_value = ds['reviews_per_month'].mode()[0]
ds.loc[:, 'reviews_per_month'].fillna(mode_value, inplace=True)#replace the missing values by
print("\n no of rows in last_review column after filling missing values:",ds['last_review'].count())
print("\n no of rows in reviews_per_month column after filling missing values:",ds['reviews_per_month'].count())

#Duplicate removal:Identifying and eliminating duplicate
print("\n No of duplicate values:",ds.duplicated().sum())
print("\n There is no duplicate values in the dataset")

#standardization: Consistent formatting and units across the dataset for accurate analysis.
print("Overview of dataset")
print(ds.info())#overview of dataset


#To inspect unique values and  identify inconsistencies or unexpected values.
print("\nUnqiue values of each columns\n",ds.apply(lambda x: x.unique()))

#To identify any outliers or inconsistencies
print("\nDescription of dataset\n",ds.describe())

#manually check sample of rows to identitfy any irregularties
print("\nDataset manual checking \n",ds.head(10))

#price column is without unit ,add unit to price column
ds['price'] = "$"+ds['price'].astype(str)
#after added unit display the price columns
print("\n price column after unit added\n", ds['price'].head())

print("Dataset has been standardized: formats and units are now consistent across all entries.")

#outliers detection

#selecting numeric columns
n=ds.select_dtypes(include=[np.number]).columns

# Calculate Q1 (25th percentile) and Q3 (75th percentile)
Q1 = ds[n].quantile(0.25)
Q3 = ds[n].quantile(0.75)

# Calculate IQR (Interquartile Range)
IQR = Q3 - Q1

# Find outliers using IQR method
outliers = ((ds[n] < (Q1 - 1.5 * IQR)) | (ds[n] > (Q3 + 1.5 * IQR))).any(axis=1)

# Print the rows with outliers
print("\nRows with outliers and its count:")
print(ds[n][outliers].count())

print("\nFinal Data Info:")
print(ds.info())

#save the clean dataset
ds.to_csv('cleaned_airbnb_data.csv', index=False)

print("Data saved to 'cleaned_airbnb_data.csv'")
