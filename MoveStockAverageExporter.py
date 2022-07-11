
import requests
import pandas as pd
from operator import itemgetter

API_KEY='21a6d5c742dc0d5fc99fb55c2e40dd0a'

class MovingStockExporter(object):

    def __init__(self,number_of_days,ticker):
        self.number_of_days=number_of_days
        self.ticker=ticker
        self.get_stock_avg()


    '''validate ticker '''
    def validate_ticker(self):
        
        response = requests.get(f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}")
        if response.status_code==200:
            list_of_tickers=list(map(itemgetter('symbol'),response.json()))
        if self.ticker not in list_of_tickers:
            raise Exception ('Not a valid ticker')

    '''export to csv file in the same python file directory '''
    def export_to_csv(self,data):
        df_stock = pd.DataFrame.from_dict(data)

        #year 2021 is only selected 

        df_stock_2021=df_stock[(df_stock["date"] >'2020-12-31') & ('2022-01-01'> df_stock["date"]) ]
        df_stock_2021 = df_stock_2021.set_index('date')
        df_stock_2021=df_stock_2021.loc[:, ['ema']]
        return df_stock_2021.to_csv('Moving_stock_average_2021', sep=';')

    '''gets daily stock indicators  using EMA average calculation'''
    def get_stock_avg(self):
        # validate ticker
        self.validate_ticker()
        try:
            #request for daily indicators
            response=requests.get(f"https://financialmodelingprep.com/api/v3/technical_indicator/daily/{self.ticker}?period={self.number_of_days}&type=ema&apikey={API_KEY}")
            self.export_to_csv(response.json())


        except:
            raise Exception ('Getting stock price service failed '+ str(response.status_code))
        



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    MovingStockExporter(2,'AMZN')
    
    
 
