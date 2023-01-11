#Simulations de Monte Carlo (Loi normale)

import seaborn as sns
import datetime
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold

def plot_futur_simulations(df_trades, trades_multiplier, trades_to_forecast, number_of_simulations, true_trades_to_show, show_all_simulations=False):
    sns.set_style("darkgrid")
    sns.set(rc={'figure.figsize':(17,8)})
    plt.title("Simulation de " + str(number_of_simulations) + " scénarios différents")
    inital_wallet = df_trades.iloc[-1]['wallet']
    number_of_trade_last_year = len(df_trades[df_trades["close_date"]>datetime.datetime.now()-datetime.timedelta(days=365)])
    mean_trades_per_day = number_of_trade_last_year/365
    start_date = df_trades.iloc[-1]["close_date"]
    time_list = [(start_date:=start_date+datetime.timedelta(hours=int(24/mean_trades_per_day))) for x in range(trades_to_forecast)]
    trades_pool = list(df_trades["trade_result_pct_wallet"] + 1) * trades_multiplier
    true_trades_date = list(df_trades.iloc[-true_trades_to_show:]["close_date"])
    true_trades_result = list(df_trades.iloc[-true_trades_to_show:]["wallet"])
    mu, sigma = 0, df_trades["trade_result_pct_wallet"].std() # mean and standard deviation
    simulations = {}
    result_simulation = []
    for i in range(number_of_simulations):
        current_trades_pool = random.sample(trades_pool, trades_to_forecast)
        noise_result = np.random.normal(mu, sigma, len(current_trades_pool))
        current_trades_pool = current_trades_pool + noise_result
        curr=1
        current_trades_result = [(curr:=curr*v) for v in current_trades_pool]
        simulated_wallet = [x*inital_wallet for x in current_trades_result]
        result_simulation.append({"key": i, "result": simulated_wallet[-1]})
        simulations[i] =  simulated_wallet
        if show_all_simulations:
            plt.plot(true_trades_date+time_list, true_trades_result+simulated_wallet)
            
    if show_all_simulations == False:
        sorted_simul_result = sorted(result_simulation, key=lambda d: d['result']) 
        for i in range(10):
            index_to_show = i*int(len(sorted_simul_result)/9)
            if index_to_show>=len(sorted_simul_result):
                index_to_show = len(sorted_simul_result)-1
            if i != 9:
                plt.plot(true_trades_date+time_list, true_trades_result+simulations[sorted_simul_result[index_to_show]["key"]])

    plt.show()
    
def plot_train_test_simulation(df_trades, train_test_date, trades_multiplier, number_of_simulations):
    sns.set_style("darkgrid")
    sns.set(rc={'figure.figsize':(17,8)})
    plt.title("Courbe de surapprentissage sur " + str(number_of_simulations) + " scénarios différents")
    df_train = df_trades.loc[df_trades["close_date"]<train_test_date]
    df_test = df_trades.loc[df_trades["close_date"]>=train_test_date]
    trades_to_forecast = len(df_test)
    inital_wallet = df_train.iloc[-1]['wallet']
    trades_to_show = len(df_test)*2
    time_list = list(df_test["close_date"])
    trades_pool = list(df_train["trade_result_pct_wallet"] + 1) * trades_multiplier
    true_trades_date = list(df_train.iloc[-trades_to_show:]["close_date"])
    true_trades_result = list(df_train.iloc[-trades_to_show:]["wallet"])
    mu, sigma = 0, df_trades["trade_result_pct_wallet"].std() # mean and standard deviation
    simulations = {}
    result_simulation = []
    for i in range(number_of_simulations):
        current_trades_pool = random.sample(trades_pool, trades_to_forecast)
        noise_result = np.random.normal(mu, sigma, len(current_trades_pool))
        current_trades_pool = current_trades_pool + noise_result
        curr=1
        current_trades_result = [(curr:=curr*v) for v in current_trades_pool]
        simulated_wallet = [x*inital_wallet for x in current_trades_result]
        result_simulation.append({"key": i, "result": simulated_wallet[-1]})
        simulations[i] =  simulated_wallet
    sorted_simul_result = sorted(result_simulation, key=lambda d: d['result']) 
    for i in range(10):
        index_to_show = i*int(len(sorted_simul_result)/9)
        if index_to_show>=len(sorted_simul_result):
            index_to_show = len(sorted_simul_result)-1
        if i != 9:
            plt.plot(true_trades_date+time_list, true_trades_result+simulations[sorted_simul_result[index_to_show]["key"]])
            
    plt.plot(true_trades_date+time_list, true_trades_result+list(df_test["wallet"]), linewidth=3.0, color="green")
    plt.show() 
