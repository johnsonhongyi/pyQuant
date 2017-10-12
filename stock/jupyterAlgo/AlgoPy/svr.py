import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
# %matplotlib inline

import sys
sys.path.append('../../')
import JSONData.tdx_data_Day as tdd
from  JSONData import sina_data 
import pandas as pd

def get_data(filename):
    dates = []
    prices = []
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            # print row[0],row[0].split('-')[0]
            dates.append(int(row[0].split('-')[0]))
            prices.append(float(row[1]))
    return dates,prices

def predict_prices(dates, prices, x):
    X = np.reshape(dates, (len(dates), 1))
    svr_lin = SVR(kernel= 'linear', C=1e3)
#     svr_poly = SVR(kernel= 'poly', C=1e3, degree= 2)
    svr_rbf = SVR(kernel= 'rbf', C=1e3, gamma=0.1)
#     X = np.arange(len(dates))
    svr_lin.fit(X, prices)
#     svr_poly.fit(dates, prices)
    svr_rbf.fit(X, prices)

    plt.scatter(X,
                prices,
                color="black",
                label="Data")
    plt.plot(X,
             svr_rbf.predict(X),
             color="red",
             label="RBF Model")

    plt.plot(X,
             svr_lin.predict(X),
             color="green",
             label='linear Model')

#     plt.plot(X,
#              svr_poly.predict(X),
#              color="blue",
#              label="Ploynomial Model")

    plt.xlabel('Dates')
    plt.ylabel('Price')
    fig, ax = plt.subplots()
    ticks = ax.get_xticks()
    print ticks[:-1]
    print (np.append(ticks[:-1], len(dates) - 1))
    print [dates[int(i)] for i in (np.append(ticks[:-1], len(dates) - 1))]
    ax.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(dates) - 1))],rotation=15)
    plt.title('Support Vector Reg')
    plt.legend()
    plt.autoscale(enable=True)
    plt.show()
    return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]
# dates,prices = get_data('../AlgoTest/aapl.csv')
# print dates[:2],prices[:2]
df = tdd.get_tdx_Exp_day_to_df('000002',dl=30).sort_index(ascending=True)
dates = [i.split('-')[2] for i in df.index.tolist()]
prices = df.open.apply(lambda x:round(x,2)).tolist()
# import pdb;pdb.set_trace()
# print dates[:4],prices[:4]

predicted_prices = predict_prices(dates, prices, 29)
print(predicted_prices)