import matplotlib.pyplot as plt
import numpy as np

def plot_efficient_frontier(resultater, optimal_punkt):
    """
    Tegner alle simulerede porteføljer og markerer den optimale.
    resultater: Matrix med [afkast, risiko, sharpe] for alle simuleringer
    optimal_punkt: Liste/array med [afkast, risiko, sharpe] for den bedste
    """
    plt.figure(figsize=(10, 6))

    #Tegn alle simuleringer (farvet efter Sharpe Ratio)
    plt.scatter(resultater[1,:], resultater[0,:], c=resultater[2,:], cmap='viridis', marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Sharpe Ratio')
    # Markér den optimale portefølje
    plt.scatter(optimal_punkt[1], optimal_punkt[0], color='red', marker='*', s=200, label='Optimal Portefølje (Max Sharpe)')

    plt.title('Efficient Frontier - Monte Carlo Simuleringer')
    plt.xlabel('Årlig Risiko (Standardafvigelse)')
    plt.ylabel('Årligt Forventet Afkast')
    plt.legend()
    plt.grid(True)
    plt.show()