import numpy as np
import pandas as pd
import yfinance as yf

def beregn_capm_afkast(aktie_data, markeds_ticker = '^GSPC', rf = 0.04, mrp=0.06):
    """
    Beregner forventet afkast vha. CAPM: E[R_i] = R_f + Beta * (E[R_m] - R_f)
    - rf: Risikofri rente sat til 4,0% (Forår 2026 niveau).
    - mrp: Markedsrisikopræmie sat til 6,0% (Skattestyrelsens anbefaling for 2026).
    - markeds_ticker: S&P 500 (^GSPC) bruges som proxy for markedsporteføljen.
    """
    print(f"Henter markedsdata ({markeds_ticker}) til Beta-beregning...")

    #1 Tidsrammen for aktiernes datagrundlag
    startdato = aktie_data.index[0]
    slutdato = aktie_data.index[-1]

   # Henter markedsdata OG valutakurs
    marked_data = yf.download([markeds_ticker, 'DKK=X'], start=startdato, end=slutdato)
    
    if 'Adj Close' in marked_data.columns:
        marked_pris_df = marked_data['Adj Close']
    else:
        marked_pris_df = marked_data['Close']

    # NYT: Nulstil klokkeslæt for at matche aktierne
    marked_pris_df.index = pd.to_datetime(marked_pris_df.index).normalize()

    # Udtræk S&P 500 og omregn til DKK
    marked_pris = marked_pris_df[markeds_ticker] * marked_pris_df['DKK=X']

    # 4. Synkroniser tidsrækker PÅ PRISNIVEAU (før vi regner afkast)
    fælles_index = aktie_data.index.intersection(marked_pris.index)

    # Sikkerheds-tjek
    if len(fælles_index) == 0:
        raise ValueError("FEJL: Ingen fælles datoer mellem aktier og markedet!")

    aktie_data = aktie_data.loc[fælles_index]
    marked_pris = marked_pris.loc[fælles_index]

    # Beregn kontinuerte log-afkast på de matchede dage: ln(P_t / P_{t-1})
    marked_afkast = np.log(marked_pris / marked_pris.shift(1)).dropna()
    aktie_afkast = np.log(aktie_data / aktie_data.shift(1)).dropna()


    # 5. Beregn markedets årlige varians: Var(R_m) * 252
    marked_varians = marked_afkast.var() * 252

    forventet_afkast = {}

    # 6. Beregn Beta og CAPM-afkast per aktie
    for aktie in aktie_afkast.columns:
        # Årlig kovarians mellem aktien og markedet: Cov(R_i, R_m) * 252
        kovarians = aktie_afkast[aktie].cov(marked_afkast) * 252

        # beta = Cov(R_i, R_m) / Var(R_m)
        beta = kovarians / marked_varians
        
        #E[R_i] = R_f + Beta * mrp
        forventet_afkast[aktie] = rf + beta * mrp
    
    # 7. Formater output
    mu_capm = pd.Series(forventet_afkast).reindex(aktie_afkast.columns)

    # Den historiske kovariansmatrix (Sigma) bevares til beregning af porteføljens risiko
    sigma = aktie_afkast.cov() * 252

    return mu_capm, sigma