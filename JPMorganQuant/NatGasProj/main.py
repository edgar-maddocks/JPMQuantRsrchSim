import pandas as pd
import numpy as np
import datetime
import tensorflow as tf


def createandfitmodel(csvname):
    data = pd.read_csv(csvname)
    DatesObj = []
    months = []
    years = []
    seasons = []
    for i in range(data.shape[0]):
        date_str = data["Dates"].iloc[i]
        month_day_yr = date_str.split("/")
        month_day_yr_int = [int(x) for x in month_day_yr]
        dateobj = datetime.date(month_day_yr_int[2],month_day_yr_int[0],month_day_yr_int[1])
        if dateobj.month >= 12 or dateobj.month < 3:
            seasons.append(1)
        elif 3 <= dateobj.month < 6:
            seasons.append(2)
        elif 6 <= dateobj.month < 9:
            seasons.append(3)
        elif 9 <= dateobj.month < 12:
            seasons.append(4)
        DatesObj.append(dateobj)
        months.append(dateobj.month)
        years.append(dateobj.year)
    data["DatesAsObj"] = DatesObj
    data["month"] = months
    data["year"] = years
    data["season"] = seasons
    data.drop("Dates", axis = 1, inplace=True)
    data.drop("DatesAsObj", axis=1, inplace=True)
    X = data[["month", "year", "season"]]
    y = data["Prices"]
    X_train, y_train = X[:35], y[:35]
    X_val, y_val = X[35:], y[35:]
    cp = tf.keras.callbacks.ModelCheckpoint("NatGasModel", save_best_only=True)
    model = tf.keras.models.Sequential([tf.keras.layers.Input((3, 1), name="input"),
                        tf.keras.layers.LSTM(128),
                        tf.keras.layers.Dense(64),
                        tf.keras.layers.Dense(1, name="Dense_layer"),
                        tf.keras.layers.Activation("linear", name="output")])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=5000, callbacks=cp)

def takeinputgiveoutput():
    date = input("Please input date in format of (2-digit year/2-digit month/2-digit day)")
    datesplit = date.split("/")
    datesplit = [int(x) for x in datesplit]
    seasonpred = 0
    if datesplit[1] >= 12 or datesplit[1] < 3:
        seasonpred = 1
    elif 3 <= datesplit[1] < 6:
        seasonpred = 1
    elif 6 <= datesplit[1] < 9:
        seasonpred = 1
    elif 9 <= datesplit[1] < 12:
        seasonpred = 1
    array2pred = np.array([datesplit[1], datesplit[0], seasonpred])
    array2pred = np.resize(array2pred,(array2pred.shape[0],1))
    filename = "NatGasModel"
    model = tf.keras.models.load_model(filename)
    print(model.predict(np.reshape(array2pred, (1,3)))[0][0])


createandfitmodel("Nat_Gas.csv")
takeinputgiveoutput()
