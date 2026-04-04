import numpy as np
import pandas as pd

def optimer_portefølje( mu, sigma, antal_simuleringer =10000, rf=0.04):
    """
    Jeg optimerer porteføljen ved at simulere tilfældige vægte og beregne Sharpe Ratio for hver simulering.
    """
    np.random.seed(42)  # For reproducibility

    if len(mu) == 0:
      raise ValueError("mu er tom. Tjek beregn_capm_afkast().")

    antal_aktier = len(mu)

    # NYT: Vi trækker de rå tal (.values) ud som rene Numpy-matricer.
    # Dette forhindrer dimensions-fejl og gør koden lynhurtig.
    mu_matrix = mu.values
    sigma_matrix = sigma.values

    resultater = np.zeros((3, antal_simuleringer))  # Kolonner: afkast, risiko, sharpe ratio
    alle_vægte = [] # For at gemme vægte for hver simulering

    for i in range(antal_simuleringer):
        # Jeg lader computeren simulere tilfældige vægte og normalisere dem
        vægte = np.random.random(antal_aktier)
        vægte /= np.sum(vægte) # Sikrer at sum(w) = 1
        alle_vægte.append(vægte) # Gemmer vægtene for denne simulering

        # Jeg beregner porteføljeafkast: w^T * mu
        portefølje_afkast = np.dot(vægte, mu_matrix)

        # Jeg beregner porteføljerisiko(standardafvigelse): sqrt(w^T * sigma * w)
        portefølje_risiko = np.sqrt(np.dot(vægte.T, np.dot(sigma_matrix, vægte)))

      # Jeg gemmer resultaterne (Afkast, Risiko og Sharpe Ratio):
      # Jeg antager en risikofri rente på 0 for at forenkle Sharpe Ratio beregningen

        resultater[0, i] = portefølje_afkast
        resultater[1, i] = portefølje_risiko
        resultater[2, i] = (portefølje_afkast - rf) / portefølje_risiko  # Sharpe Ratio
    
    # jeg finder indeks for porteføljen med højeste Sharpe Ratio
    max_sharpe_indeks = resultater[2].argmax()

    bedste_vægte = alle_vægte[max_sharpe_indeks]
    ret_risk_sharpe = resultater[:, max_sharpe_indeks]
    
    return bedste_vægte, ret_risk_sharpe, resultater
