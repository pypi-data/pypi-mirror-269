# Nell'init.py, puoi lasciarlo vuoto poiché non è necessario per il tuo progetto. 
# Tuttavia, è comune includere alcune informazioni sul pacchetto. Ecco un esempio di cosa potresti includere:          

"""
Economic-Finance Correlation Package

A Python package for investigating the correlation between economic and financial data.
"""

__version__ = "0.1"

from .api import app
from .functions import (
    get_stock_data,
    plot_candlestick,
    avg_stock_data,
    get_world_bank_data,
    calculate_correlation,
    plot_correlation,
    generate_text,
)


# Questo file fornisce una breve descrizione del pacchetto e definisce la versione. 
# Infine, importa tutte le funzioni dal modulo functions.py in modo che siano disponibili quando importi il tuo pacchetto.