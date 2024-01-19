import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

filepath = "Task 3 and 4_Loan_Data (1).csv"
data = pd.read_csv(filepath)
fico = data["fico_score"].sort_values()
income = data["income"]

def GetDataTrainModel(filepath):
    data = pd.read_csv(filepath)
    fico = data["fico_score"].sort_values()
    fico = fico.to_numpy()
    fico = fico.reshape(-1,1)
    buckets = int(input("Enter number of buckets: "))
    model = KMeans(n_clusters=buckets)
    model.fit(fico)
    return model, buckets

def GetScore(model, buckets, fico_score):
    arr = np.array([fico_score])
    arr = arr.reshape(-1,1)
    numscore = model.predict(arr)
    print(f"{numscore}")