###################################################
# Rating Products
###################################################

# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating


############################################
# Practice: User and Time Weighted Online Course Rating
############################################

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Course Name: (50+ Saat) Python A-Z™: Veri Bilimi ve Machine Learning
# Score: 4.8 (4.764925)
# Total Score: 4611
# Percentage of Scores: 75, 20, 4, 1, <1
# Approximate Numerical Equivalents: 3458, 922, 184, 46, 6

df = pd.read_csv("course_reviews.csv")
df.head()
df.shape

# distribution of ratings
df["Rating"].value_counts()

# distribution of the people and number of questions asked
df["Questions Asked"].value_counts()

# the score given in the breakdown of the questions asked
# to see if there is a relationship
df.groupby("Questions Asked").agg({"Questions Asked": "count",
                                   "Rating": "mean"})


df.head()

####################
# Average
####################

df["Rating"].mean()

####################
# Time-Based Weighted Average
####################

df.head()
df.info()

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
# Timestamp variable type is changed

df["Timestamp"].max()
current_date = pd.to_datetime('2021-02-10 0:0:0')
# Analysis date is set 5 days after the max date on data

df["days"] = (current_date - df["Timestamp"]).dt.days
# Recency of the ratings and it is added into dataframe as days

# average rating in the last 30 days:
df.loc[df["days"] <= 30, "Rating"].mean()
# loc is used since there is an operation on a different column than the condition

# average rating in between last 30 and 90 days:
df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean()

# average rating in between last 90 and 180 days:
df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean()

# average rating 6 months ago older:
df.loc[(df["days"] > 180), "Rating"].mean()


df.loc[df["days"] <= 30, "Rating"].mean() * 28/100 + \
    df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean() * 26/100 + \
    df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean() * 24/100 + \
    df.loc[(df["days"] > 180), "Rating"].mean() * 22/100

def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_weighted_average(df)

time_based_weighted_average(df, 30, 26, 22, 22)



####################
# User-Based Weighted Average
####################

df.head()

df.groupby("Progress").agg({"Rating": "mean"})

df.loc[df["Progress"] <= 10, "Rating"].mean() * 22 / 100 + \
    df.loc[(df["Progress"] > 10) & (df["Progress"] <= 45), "Rating"].mean() * 24 / 100 + \
    df.loc[(df["Progress"] > 45) & (df["Progress"] <= 75), "Rating"].mean() * 26 / 100 + \
    df.loc[(df["Progress"] > 75), "Rating"].mean() * 28 / 100



def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100


user_based_weighted_average(df, 20, 24, 26, 30)


####################
# Weighted Rating
####################

def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe)*user_w/100

course_weighted_rating(df)

course_weighted_rating(df, time_w=40, user_w=60)










