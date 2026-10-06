# Porteføljeoptimering (Max Sharpe Ratio)

Kvantitativ investeringsmodel i Python, der finder den aktiefordeling (vægte), som giver den højeste Sharpe Ratio for en portefølje på otte aktier. Forventet afkast estimeres med CAPM, og optimeringen sker ved Monte Carlo-simulering af tilfældige porteføljer.

Projektet er lavet som en øvelse i at omsætte porteføljeteori til kode og er opdelt i separate moduler til datahentning, beregning, optimering og visualisering.

## Aktier

Fire danske aktier fra OMXC25 og fire amerikanske:

| Danske | Amerikanske |
|---|---|
| Novo Nordisk B (`NOVO-B.CO`) | Apple (`AAPL`) |
| Danske Bank (`DANSKE.CO`) | Microsoft (`MSFT`) |
| Vestas (`VWS.CO`) | Alphabet (`GOOGL`) |
| Carlsberg B (`CARL-B.CO`) | Meta (`META`) |

Aktierne og tidsrammen (de seneste 5 år) kan ændres i `main.py`.

## Sådan virker det

1. **`data_henter.py`** henter daglige kurser fra Yahoo Finance via `yfinance` sammen med valutakursen USD/DKK. De amerikanske aktier omregnes til DKK, så alle aktier er i samme valuta. Datoer, hvor en eller flere kurser mangler (fx helligdage på en af børserne), fjernes.
2. **`beregninger.py`**
   - Omregner S&P 500 (`^GSPC`), som bruges som proxy for markedsporteføljen, til DKK.
   - Synkroniserer aktier og marked på de samme datoer på prisniveau, *før* afkast beregnes, så alle afkast dækker samme periode.
   - Beregner daglige log-afkast og estimerer hver akties beta: `Cov(R_i, R_m) / Var(R_m)`.
   - Beregner forventet afkast med CAPM: `E[R_i] = r_f + β_i · MRP`.
   - Beregner den årlige kovariansmatrix (daglig kovarians × 252).
3. **`optimering.py`** simulerer 10.000 tilfældige long-only-porteføljer (vægte summer til 1) og beregner for hver afkast, risiko (`√(wᵀΣw)`) og Sharpe Ratio `(μ_p − r_f) / σ_p`. Porteføljen med højest Sharpe Ratio vælges. Der bruges et fast random seed (42), så resultaterne kan gentages.
4. **`visualisering.py`** plotter alle simulerede porteføljer (risiko mod afkast, farvet efter Sharpe Ratio) og markerer den optimale.
5. **`main.py`** kører hele forløbet og printer de optimale vægte (med korrekte aktienavne), forventet afkast, risiko og Sharpe Ratio.

## Antagelser

| Parameter | Værdi |
|---|---|
| Risikofri rente (`rf`) | 4,0 % |
| Markedsrisikopræmie (`mrp`) | 6,0 % |
| Handelsdage pr. år | 252 |
| Antal simuleringer | 10.000 |
| Valuta | Alle priser omregnet til DKK |

Risikofri rente og markedsrisikopræmie er faste antagelser, ikke estimeret fra data, og bør opdateres og kildebelægges, hvis modellen skal bruges til mere end øvelse. Den risikofri rente på 4 % svarer til et amerikansk renteniveau, mens afkastene er opgjort i DKK.

## Kom i gang

```bash
pip install numpy pandas yfinance matplotlib
python main.py
```

Der kræves internetforbindelse, da kurserne hentes live. Resultatet afhænger derfor af, hvornår koden køres.

## Begrænsninger

- **Markedsproxy:** S&P 500 bruges som markedsportefølje for alle aktier, også de danske. En global eller dansk indeksproxy kunne give mere retvisende betaer for de danske aktier.
- **Valutaeffekt:** Omregning til DKK betyder, at de amerikanske aktiers afkast indeholder udsving i USD/DKK, og den risikofri rente er ikke tilpasset DKK.
- **CAPM:** Forventet afkast bestemmes udelukkende af beta og de faste antagelser, ikke af aktiernes egen afkasthistorik.
- **Monte Carlo er en tilnærmelse:** Tilfældige vægte giver et godt, men ikke eksakt, optimum. En numerisk optimering (fx `scipy.optimize`) kunne finde det præcise.
- **Plottet:** Viser tilfældige porteføljer. Den egentlige effektive rand er den øvre kant af punktskyen.
- **In-sample:** Vægtene er optimeret på samme data, som parametrene er estimeret på, uden out-of-sample-test.

Projektet er en øvelse og ikke investeringsrådgivning.

## Mulige forbedringer

- Dansk risikofri rente og et mere passende markedsindeks
- Eksakt optimering med `scipy.optimize` og restriktioner på maksimal vægt pr. aktie
- Out-of-sample-test af porteføljen
