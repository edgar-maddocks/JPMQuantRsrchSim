import pandas as pd
import datetime
from dateutil import relativedelta
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

def GetInjectionsDateAndQ():
    Injections = {"Date" : [], "Quantity" : []}
    while True:
        date = input("Please input an injection date in format of (4-digit year/2-digit month/2-digit day)")
        yr_month_day = date.split("/")
        yr_month_day_int = [int(x) for x in yr_month_day]
        dateobj = datetime.date(yr_month_day_int[0],yr_month_day_int[1],yr_month_day_int[2])
        quantity = int(input("Please input the quantity of gas you will purchase at this date, e.g. 1000000: "))
        Injections["Date"].append(dateobj)
        Injections["Quantity"].append(quantity)
        quit = input("Would you like to enter more injections? y/n:")
        if quit == "y":
            continue
        else:
            break
    InjectionsPd = pd.DataFrame(data=Injections, columns=["Date", "Quantity"])
    return InjectionsPd

def GetWithdrawalsDateAndQ():
    Withdrawals = {"Date" : [], "Quantity" : []}
    while True:
        date = input("Please input a withdrawal date in format of (4-digit year/2-digit month/2-digit day)")
        yr_month_day = date.split("/")
        yr_month_day_int = [int(x) for x in yr_month_day]
        dateobj = datetime.date(yr_month_day_int[0],yr_month_day_int[1],yr_month_day_int[2])
        quantity = int(input("Please input the quantity of gas you will sell at this date, e.g. 1000000: "))
        Withdrawals["Date"].append(dateobj)
        Withdrawals["Quantity"].append(quantity)
        quit = input("Would you like to enter more withdrawals? y/n:")
        if quit == "y":
            continue
        else:
            break
    WithdrawalsPd = pd.DataFrame(data=Withdrawals, columns=["Date", "Quantity"])
    return WithdrawalsPd

def UpdateInjections(Injections):
    prices = []
    pricesbyq = []
    type = []
    from keras.models import load_model
    filename = "NatGasModel"
    model = load_model(filename)
    for i in range(len(Injections)):
        seasonpred = 0
        month = Injections["Date"].iloc[i].month
        year = Injections["Date"].iloc[i].year
        if Injections["Date"].iloc[i].month >= 12 or Injections["Date"].iloc[i].month < 3:
            seasonpred = 1
        elif Injections["Date"].iloc[i].month >= 3 and Injections["Date"].iloc[i].month < 6:
            seasonpred = 2
        elif Injections["Date"].iloc[i].month >= 6 and Injections["Date"].iloc[i].month < 9:
            seasonpred = 3
        elif Injections["Date"].iloc[i].month >= 9 and Injections["Date"].iloc[i].month < 12:
            seasonpred = 4
        array2pred = np.array([month, year, seasonpred])
        array2pred = np.resize(array2pred,(array2pred.shape[0],1))
        price = model.predict(np.reshape(array2pred, (1,3)))[0][0]
        prices.append(price)
        type.append("I")
        pricesbyq.append(price * int(Injections["Quantity"].iloc[i]))
    Injections["PriceAtDate"] = prices
    Injections["PriceByQ"] = pricesbyq
    Injections["Type"] = type
    return Injections

def UpdateWithdrawals(Withdrawals):
    prices = []
    pricesbyq = []
    type = []
    from keras.models import load_model
    filename = "NatGasModel"
    model = load_model(filename)
    for i in range(len(Withdrawals)):
        seasonpred = 0
        month = Withdrawals["Date"].iloc[i].month
        year = Withdrawals["Date"].iloc[i].year
        if Withdrawals["Date"].iloc[i].month >= 12 or Withdrawals["Date"].iloc[i].month < 3:
            seasonpred = 1
        elif Withdrawals["Date"].iloc[i].month >= 3 and Withdrawals["Date"].iloc[i].month < 6:
            seasonpred = 2
        elif Withdrawals["Date"].iloc[i].month >= 6 and Withdrawals["Date"].iloc[i].month < 9:
            seasonpred = 3
        elif Withdrawals["Date"].iloc[i].month >= 9 and Withdrawals["Date"].iloc[i].month < 12:
            seasonpred = 4
        array2pred = np.array([month, year, seasonpred])
        array2pred = np.resize(array2pred,(array2pred.shape[0],1))
        price = model.predict(np.reshape(array2pred, (1,3)))[0][0]
        prices.append(price)
        type.append("W")
        pricesbyq.append(price * int(Withdrawals["Quantity"].iloc[i]))
    Withdrawals["PriceAtDate"] = prices
    Withdrawals["PriceByQ"] = pricesbyq
    Withdrawals["Type"] = type
    
    return Withdrawals

def TypePlusMinusPrice(df, runningtotal, rate):
    for i in range(len(df)):
        if df.iloc[i]["Type"] == "I":
            runningtotal -= df.iloc[i]["PriceByQ"]
            runningtotal -= rate
        elif df.iloc[i]["Type"] == "W":
            runningtotal += df.iloc[i]["PriceByQ"]
            runningtotal -= rate
    return runningtotal

def TypePlusMinusQuantity(df, runningquantity, maxvolume):
    for i in range(len(df)):
        if 0 > runningquantity > maxvolume:
            print(f"At date: {df.iloc[i]['Date']} the stored valume is greater than maximum.")
        elif df.iloc[i]["Type"] == "I":
            runningquantity += df.iloc[i]["Quantity"]
        elif df.iloc[i]["Type"] == "W":
            runningquantity -= df.iloc[i]["Quantity"]
    return runningquantity

def RunningQuantity(df):
    runningquantity = 0
    maxvolume = float(input("Enter the maximum volume which can be stored at one time: "))
    return TypePlusMinusQuantity(df, runningquantity, maxvolume)

def RunningTotal(df):
    runningtotal = 0
    firstdate = df.iloc[0]["Date"]
    lastdate = df.iloc[-1]["Date"]
    rate = float(input("Enter the rate for an injection/withdrawal: "))
    runningtotal = TypePlusMinusPrice(df, runningtotal, rate)
    return StorageCosts(runningtotal, firstdate, lastdate)

def DiffBetweenTwoDates(date1, date2):
    r = relativedelta.relativedelta(date1, date2)
    return (r.years * 12) + r.months

def StorageCosts(runningtotal, date1, date2):
    storagecostspm = float(input("Please enter the storage costs per month: "))
    dist = float(DiffBetweenTwoDates(date1, date2))
    return runningtotal + (storagecostspm * dist)

def PriceContract():
    Injections = GetInjectionsDateAndQ()
    Withdrawals = GetWithdrawalsDateAndQ()
    Injections = UpdateInjections(Injections)
    Withdrawals = UpdateWithdrawals(Withdrawals)
    df = pd.concat([Injections, Withdrawals]).sort_values("Date")
    runningtotal = RunningTotal(df)
    runningquantity = RunningQuantity(df)
    
    return df, runningtotal, runningquantity

df, rt, rq = PriceContract()
print(f"The contract's worth is : {rt}")