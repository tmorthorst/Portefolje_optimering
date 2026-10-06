import yfinance as yf
import pandas as pd

import yfinance as yf
import pandas as pd

# NYT Omregnet til USD og så tilbage til danske kroner (DKK) vha. valutakursen USD/DKK. Dette sikrer, at alle aktier er i samme valuta.
def hent_aktiedata(aktier, startdato, slutdato):
    print(f"Henter Data for aktier og USD/DKK fra {startdato} til {slutdato}")

    # Hent aktier + valutakurs i ét samlet hug
    tickers = aktier + ['DKK=X']
    data = yf.download(tickers, start=startdato, end=slutdato)
    
    pris_data = data['Adj Close'] if 'Adj Close' in data.columns else data['Close']
    pris_data.index = pd.to_datetime(pris_data.index).normalize()

    # Adskil valuta fra aktierne
    valuta = pris_data['DKK=X']
    aktie_priser = pris_data.drop(columns=['DKK=X'])

    # Find de amerikanske aktier (dem der IKKE slutter på '.CO') og omregn til DKK
    usd_aktier = [aktie for aktie in aktier if not aktie.endswith('.CO')]
    for aktie in usd_aktier:
        aktie_priser[aktie] = aktie_priser[aktie] * valuta

    # Fjern helligdage
    data_renset = aktie_priser.dropna()
    
    if data_renset.empty:
        print("ADVARSEL: Al data blev slettet! Tjek dine tickers.")
    else:
        print("Data hentet, renset og omregnet til DKK med succes!")
       
    return data_renset
