import yfinance as yf
import pandas as pd

def hent_aktiedata(aktier, startdato, slutdato):
    """
    Henter historiske 'Adj Close' kurser og fjerner rækker med manglende data.
    """
    print(f"Henter Data for {aktier} fra {startdato} til {slutdato}")

    #jeg henter data
    data = yf.download(aktier, start = startdato, end = slutdato, auto_adjust = True)['Close']

    #jeg sikrer at output altid er en dataframe (Matrix), selv kun ved 1 aktie
    if isinstance(data, pd.Series):
        data = data.to_frame()

    #jeg fjerner helligdage og manglende data (NaN)
    data_renset = data.dropna()
    
    print("Data hentet og rentet med succes!")
    return data_renset
