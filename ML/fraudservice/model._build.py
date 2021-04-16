# -*- coding: utf-8 -*-
import pickle
import joblib
import warnings
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

sns.set(rc={'figure.figsize': (11, 8)})
# train = pd.read_csv(r'C:\Users\jusia\Desktop\xenteProjects\Data_store\training.csv')

train = pd.read_csv(r'C:\Users\jusia\PycharmProjects\xente\Data\training.csv')
# can pass amore data and run train
train["train"] = 1

statistics = []

for column in train.columns:
    statistics.append(
        (column, train[column].nunique(), train[column].isnull().sum() * 100 / train.shape[0], train[column].dtype))

statistics_df = pd.DataFrame(statistics,
                             columns=["column", "unique_values", "percentage_of_missing_values", "data_type"])

test = pd.read_csv(r'C:\Users\jusia\Desktop\xenteProjects\Data_store\test.csv')
test["train"] = 0

statistics_test = []

for column in test.columns:
    statistics_test.append(
        (column, test[column].nunique(), test[column].isnull().sum() * 100 / test.shape[0], test[column].dtype))

statistics_test_df = pd.DataFrame(statistics_test,
                                  columns=["column", "unique_values", "percentage_of_missing_values", "data_type"])
# Machine  looks at binary hence column names changed to intergers for calculations
dataset = pd.concat([train, test], ignore_index=True)
dataset = pd.concat([dataset, pd.get_dummies(dataset["ChannelId"], prefix="Channel_Id_")], axis=1)
dataset = pd.concat([dataset, pd.get_dummies(dataset["PricingStrategy"], prefix="PricingStrategy_")], axis=1)
dataset = pd.concat([dataset, pd.get_dummies(dataset["ProductCategory"], prefix="ProductCategory_")], axis=1)
dataset = pd.concat([dataset, pd.get_dummies(dataset["ProductId"], prefix="ProductId_")], axis=1)
dataset = pd.concat([dataset, pd.get_dummies(dataset["ProviderId"], prefix="ProviderId_")], axis=1)

# time feature engineering
dataset["TransactionStartTime"] = dataset["TransactionStartTime"].apply(lambda x: pd.to_datetime(x))
dataset["day_of_week"] = dataset["TransactionStartTime"].dt.dayofweek
dataset["time"] = dataset["TransactionStartTime"].dt.time
dataset["second"] = dataset["time"].apply(
    lambda x: int(str(x).split(":")[0]) * 3600 + int(str(x).split(":")[1]) * 60 + int(str(x).split(":")[2]))

dataset = pd.concat([dataset, pd.get_dummies(dataset["day_of_week"], prefix="day_of_week_")], axis=1)

# id
dataset["AccountId"] = dataset["AccountId"].apply(lambda x: int(x.split("_")[1]))
dataset["CustomerId"] = dataset["CustomerId"].apply(lambda x: int(x.split("_")[1]))
dataset["SubscriptionId"] = dataset["SubscriptionId"].apply(lambda x: int(x.split("_")[1]))

group = dataset[['CustomerId', 'ProductId', 'ProviderId', 'ChannelId', 'Amount', 'day_of_week']].groupby(
    by=['CustomerId', 'ProductId', 'ProviderId', 'ChannelId', 'Amount', ])[['day_of_week']].mean().reset_index().rename(
    index=str, columns={'day_of_week': 'Cust_prod_mean_dayofweek'})
dataset = dataset.merge(group, on=['CustomerId', 'ProductId', 'ProviderId', 'ChannelId', ], how='left')

# Drop unwanted columns.
dataset.drop(["CurrencyCode", "CountryCode", "BatchId", "ChannelId", "PricingStrategy", "ProductCategory", "ProductId",
              "ProviderId", "time", "TransactionStartTime", ], axis=1, inplace=True)

train = dataset[dataset["train"] == 1]
test = dataset[dataset["train"] == 0]

train.drop(["train"], axis=1, inplace=True)
test.drop(["train", "FraudResult"], axis=1, inplace=True)

X = train.drop(["TransactionId", "FraudResult"], axis=1)
y = train["FraudResult"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

print("Fraud case", (train["FraudResult"].value_counts()[1] / len(train) * 100), "% of the dataset")
print("Train size", y_train.shape[0], "Fraud in train size", y_train[y_train == 1].shape[0] / y_train.shape[0] * 100)
print("Test size", y_test.shape[0], "Fraud in test size", y_test[y_test == 1].shape[0] / y_test.shape[0] * 100)

rfc = RandomForestClassifier(random_state=1, n_estimators=200, max_depth=8)

rfc.fit(X_train, y_train)

# noinspection SpellCheckingInspection
rfc_pred = rfc.predict(X_test)

# print results on xls
print("rfc ", classification_report(y_test, rfc_pred))

# magic  line for prediction
predict_test = rfc.predict(X_test)

# Save to file in the current working directory
print("model score: %.3f" % rfc.predict(X_test))
joblib.dump(rfc, 'Fraud_model.sav')

