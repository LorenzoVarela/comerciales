import pandas as pd
from dash  import html
import dash_table

def preprocesar(ventas):
    ventas['Importeprevisto'] = ventas['Importeprevisto'].replace('', '0')
    ventas['Importeprevisto'] = ventas['Importeprevisto'].replace(' ', '0')
    ventas['Importeprevisto']=ventas['Importeprevisto'].astype(float)
    ventas['Fechacreación'] = pd.to_datetime(ventas['Fechacreación'])
    ventas['Fecha'] = ventas['Fechacreación'].dt.strftime('%Y%m')
    print('procesamos DF')
    return ventas


def comerciales_estado(ventas):
    ventas_cerradas = ventas[ventas['Estado'].isin(["Cerrada y ganada","Cerrada y perdida","Cerrada y no presentada"])]
    
    # Agrupar por "Comercial" y "Estado" y realizar las agregaciones
    nuevo_df_t = ventas_cerradas.groupby(['Comercial', 'Estado']).agg(Cantidad=('Estado', 'count')).reset_index()
    nuevo_df = nuevo_df_t.pivot_table(index='Comercial', columns='Estado',values='Cantidad')
    nuevo_df.reset_index(inplace=True)
    nuevo_df.columns.name = None
    nuevo_df = nuevo_df.fillna(0)
    return nuevo_df

def comerciales_ventas(ventas):
    # sacamos las ventas
    nuevo_df = pd.DataFrame(ventas[ventas['Estado'] == 'Cerrada y ganada'].groupby('Comercial')['Importeprevisto'].sum())
    nuevo_df.reset_index(inplace=True)
    return nuevo_df


def comercial_ventas(ventas, nombre):
    nuevo_df = pd.DataFrame(ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')].groupby('Cliente')['Importeprevisto'].sum())
    nuevo_df.reset_index(inplace=True)
    return nuevo_df

def lista_comerciales(ventas):
    # Extraemos la lista de los comerciales
    df_sp = ventas['Comercial']
    df_sp = df_sp.drop_duplicates()
    df_sp.head()
    comerciales=df_sp.tolist()
    return comerciales

def presentar_comerciales():
    return True

def comercial_fechas(ventas, nombre):
    nuevo_df = pd.DataFrame(ventas[(ventas['Comercial'] == nombre) & (ventas['Estado'] == 'Cerrada y ganada')])
    nuevo_df.reset_index(inplace=True)
    nuevo_df.columns.name = None
    nuevo_df = nuevo_df.fillna(0)    
    nuevo_df = nuevo_df.sort_values('Fecha')
    print('comercial_fechas')
    return nuevo_df