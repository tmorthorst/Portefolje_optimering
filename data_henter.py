import yfinance as yf
import pandas as pd

def hent_aktiedata(aktier, startdato, slutdato):
    print(f"Henter Data for {aktier} fra {startdato} til {slutdato}")

    data = yf.download(aktier, start=startdato, end=slutdato)
    
    if 'Adj Close' in data.columns:
        pris_data = data['Adj Close']
    else:
        pris_data = data['Close']

    if isinstance(pris_data, pd.Series):
        pris_data = pris_data.to_frame()

    # NYT: Nulstil klokkeslæt og tidszoner til midnat, så DK og USA kan matches!
    pris_data.index = pd.to_datetime(pris_data.index).normalize()

    # Nu kan vi fjerne de rigtige helligdage uden at slette alt
    data_renset = pris_data.dropna()
    
    if data_renset.empty:
        print("ADVARSEL: Al data blev slettet! Tjek dine tickers.")
    else:
        print("Data hentet og renset med succes!")
    
    return data_renset