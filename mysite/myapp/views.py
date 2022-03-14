import pandas as pd
import requests

from django.shortcuts import render

from django.http import  HttpResponse

from alpha_vantage.timeseries import TimeSeries

API_key = '03QDMPDVX4N8GR4U'

#   https://medium.com/codex/alpha-vantage-an-introduction-to-a-highly-efficient-free-stock-api-6d17f4481bf
def get_monthly_data(symbol):
    api_key = '03QDMPDVX4N8GR4U'
    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'
    raw_df = requests.get(api_url).json()

    df = pd.DataFrame(raw_df[f'Monthly Time Series']).T
    df = df.rename(
        columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1]
    return df

def index(request): # http://127.0.0.1:8000

    data = get_monthly_data('AAPL')

    #ts = TimeSeries(key=API_key)
    #data1 = ts.get_monthly_adjusted('AAPL')

    html = data.to_html()
    return HttpResponse(html)
