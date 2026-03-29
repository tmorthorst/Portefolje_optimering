import numpy as np
import pandas as pd

def beregn_portefolje_statistik(pris_data):
    """
    Jeg beregner årlige log-afkast og kovariansmatrix.
    """
    # jeg beregner det daglige log-afkast: ln(P_t / P_(t-1))
    log_afkast = np.log(pris_data / pris_data.shift(1)).dropna()

    #
    # jeg beregner det årlige forventede log-afkast ved at multiplicere gennemsnit af 
    # daglig log_akast med 252 (antal handelsdage)
    forventet_årlige_log_afkast = log_afkast.mean() * 252

    # Jeg beeregner den årlige kovariansmatrix ved at gange den daglige kovariansmatrix med 252
    kovarians_matrix = log_afkast.cov() * 252

    return forventet_årlige_log_afkast, kovarians_matrix
