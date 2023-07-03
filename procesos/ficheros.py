import pandas as pd
import warnings
from openpyxl import Workbook

warnings.simplefilter("ignore")

def leer_comerciales(direccion):
    print('Estamos leyendo fichero')
    ventas = pd.read_excel(direccion, skiprows=5, decimal=',')
    # Obtenemos los nombres de la cabecera
    nombre_columnas = ventas.columns.tolist()
    # Quitramos espacios de los nombre
    nuevas_colimnas = [nombre.replace(" ","").replace("(","").replace(")","") for nombre in nombre_columnas]
    ventas.rename(columns=dict(zip(nombre_columnas, nuevas_colimnas)), inplace=True)
    return ventas


