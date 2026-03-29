import datetime as dt
from data_henter import hent_aktiedata
from beregninger import beregn_portefolje_statistik
from optimering import optimer_portefølje
from visualisering import plot_efficient_frontier


#1 Setup
#vælger fem aktier fra C25
aktier = ['NOVO-B.CO', 'MAERSK-A.CO', 'DANSKE.CO', 'VWS.CO', 'CARL-B.CO']

#sætter slutdato til i dag:
slutdato = dt.datetime.today().strftime('%Y-%m-%d')

#sætter startdato til 1 år tilbage fra i dag:
startdato = (dt.datetime.today() - dt.timedelta(days=5*365)).strftime('%Y-%m-%d'  )

#2 pipeline
pris_data = hent_aktiedata(aktier, startdato, slutdato)
mu, sigma = beregn_portefolje_statistik(pris_data)
vægte, info, alle_resultater = optimer_portefølje(mu, sigma)


#3 print resultat
print("\n" + "="*30)
print("OPTIMAL PORTEFØLJE (Max Sharpe)")
print("="*30)
for i in range(len(aktier)):
    print(f"{aktier[i]}: {vægte[i]:.2%}")

print("-"*30)
print(f"Forventet årligt afkast: {info[0]:.2%}")
print(f"Forventet Årlig risiko:  {info[1]:.2%}")
print(f"Sharpe ratio:            {info[2]:.2f}")


# print og plot
print(f"\nOptimal Sharpe Ratio: {info[2]:.2f}")
plot_efficient_frontier(alle_resultater, info)