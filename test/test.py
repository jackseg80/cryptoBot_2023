import sys
sys.path.append('./')
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
import ta
import numpy as np
import datetime
from IPython.display import clear_output
from utilities.strategies import MultiEnvelope
from utilities.data_manager import ExchangeDataManager
from utilities.custom_indicators import get_n_columns
from utilities.bt_analysis import get_metrics, backtest_analysis_gui
from utilities.plot_analysis import plot_equity_vs_asset, plot_futur_simulations, plot_train_test_simulation, plot_bar_by_month
import nest_asyncio
nest_asyncio.apply()

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ctkApp:
        
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x400+200x200")
        self.root.title("Dynamic Scatterplot")
        self.root.update()

        self.frame = ctk.CTkFrame(master=self.root,
                                  height= self.root.winfo_height()*0.95,
                                  width = self.root.winfo_width()*0.66,
                                  fg_color="darkblue")
        self.frame.place(relx=0.25, rely=0.025)

        # Créer un widget Text pour afficher la sortie
        self.textbox = ctk.CTkTextbox(master=self.frame, width=800, height=800, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.button = ctk.CTkButton(master = self.root,
                               text="Initialize Cryptos",
                               width=200,
                               height=50,
                               command=self.initialize_cryptos)
        self.button.place(relx=0.02,rely=0.1)
        self.button = ctk.CTkButton(master = self.root,
                               text="Run Backtest",
                               width=200,
                               height=50,
                               command=self.backtest)
        self.button.place(relx=0.02,rely=0.3)
        self.button = ctk.CTkButton(master = self.root,
                               text="Plot Graphics",
                               width=200,
                               height=50,
                               command=self.plot_equity_vs_asset)
        self.button.place(relx=0.02,rely=0.5)
        self.root.mainloop()

    def initialize_cryptos(self):
        self.params = {
            "BTC/USDT:USDT":{ "src": "close", "ma_base_window": 7, "envelopes": [0.07, 0.1, 0.15], "size": 0.1,},
            "ETH/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15], "size": 0.1,},
            "ADA/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.09, 0.12, 0.15], "size": 0.1,},
            "AVAX/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.09, 0.12, 0.15], "size": 0.1,},
            "EGLD/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "KSM/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "OCEAN/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "REN/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "ACH/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "APE/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "CRV/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "DOGE/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "ENJ/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "FET/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "ICP/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "IMX/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "LDO/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "MAGIC/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "REEF/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "SAND/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "TRX/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
            "XTZ/USDT:USDT":{ "src": "close", "ma_base_window": 5, "envelopes": [0.07, 0.1, 0.15, 0.2], "size": 0.05,},
        }

        pair_list = list(self.params.keys())
        exchange_name = "bitget"
        tf = '1h'
        self.oldest_pair = "BTC/USDT:USDT"

        exchange = ExchangeDataManager(
            exchange_name=exchange_name, 
            path_download="database/exchanges"
        )

        self.df_list = {}
        for pair in pair_list:
            df = exchange.load_data(pair, tf)
            self.df_list[pair] = df.loc[:]

        print("Data load 100%")
        self.textbox.insert("0.0", "Data load 100%\n")

    def backtest(self):
        self.textbox.delete(1.0, ctk.END)
        
        strat = MultiEnvelope(
            df_list=self.df_list,
            oldest_pair=self.oldest_pair,
            type=["long","short"],
            params=self.params,
        )

        strat.populate_indicators()
        strat.populate_buy_sell()
        bt_result = strat.run_backtest(initial_wallet=1000, leverage=5)

        df_trades, df_days = backtest_analysis_gui(self,
            trades=bt_result['trades'], 
            days=bt_result['days'],
            general_info=True,
            trades_info=True,
            days_info=True,
            long_short_info=True,
            entry_exit_info=True,
            exposition_info=True,
            pair_info=True,
            indepedant_trade=True
        )

    def plot_equity_vs_asset(self):
        print("plot")

if __name__ == "__main__":        
    CTK_Window = ctkApp()