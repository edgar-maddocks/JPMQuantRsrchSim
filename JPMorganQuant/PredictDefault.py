import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

filepath = "Task 3 and 4_Loan_Data (1).csv"
def GetDataTrainModel(filepath):
    data = pd.read_csv(filepath)
    X = data.drop(["customer_id", "default"], axis = 1)
    y = data["default"]
    X_train, X_test , y_train, y_test = train_test_split(X, y, test_size = 0.2)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    return model

def GetExpectedLoss(model, loan_amount, credit_lines_outstanding, loan_amt_outstanding, total_debt_outstanding, income, years_employed, fico_score):
    arr = np.array([credit_lines_outstanding, loan_amt_outstanding, total_debt_outstanding, income, years_employed, fico_score])
    arr = arr.reshape(1,-1)
    default = model.predict(arr)
    if (default == 0):
        print("Customer likely not to default")
    elif (default == 1):
        print("Customer likely to default")
        print(f"Expected loss of: {loan_amount * 0.9}")

