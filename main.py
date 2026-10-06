import datetime as dt
from data_henter import hent_aktiedata
from beregninger import beregn_capm_afkast
from optimering import optimer_portefølje
from visualisering import plot_efficient_frontier

#1 Setup
#vælger otte aktier (4 fra OMXC25 og 4 fra USA) til porteføljen
aktier = ['NOVO-B.CO', 'DANSKE.CO', 'VWS.CO', 'CARL-B.CO', 'AAPL', 'MSFT', 'GOOGL', 'META']

#sætter slutdato til i dag:
slutdato = dt.datetime.today().strftime('%Y-%m-%d')

#sætter startdato til 5 år tilbage fra i dag:
startdato = (dt.datetime.today() - dt.timedelta(days=5*365)).strftime('%Y-%m-%d'  )

#2 pipeline
pris_data = hent_aktiedata(aktier, startdato, slutdato)
mu, sigma = beregn_capm_afkast(pris_data)
vægte, info, alle_resultater = optimer_portefølje(mu, sigma)


#3 print resultat
print("\n" + "="*30)
print("OPTIMAL PORTEFØLJE (Max Sharpe vha. Capm)")
print("="*30)
print("Vægte for de optimale aktier:")
for i in range(len(vægte)):
    print(f"{mu.index[i]}: {vægte[i]:.2%}")

print("-"*30)
print(f"Forventet årligt afkast: {info[0]:.2%}")
print(f"Forventet Årlig risiko:  {info[1]:.2%}")
print(f"Sharpe ratio:            {info[2]:.2f}")


# plot
plot_efficient_frontier(alle_resultater, info)