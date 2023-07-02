import pandas as pd

def preprocesar(ventas):
    ventas['Importeprevisto'] = ventas['Importeprevisto'].replace('', '0')
    ventas['Importeprevisto'] = ventas['Importeprevisto'].replace(' ', '0')
    ventas['Importeprevisto']=ventas['Importeprevisto'].astype(float)
    return ventas


def comercial_estado(ventas):
    ventas = preprocesar(ventas)
    ventas_cerradas = ventas[ventas['Estado'].isin(["Cerrada y ganada","Cerrada y perdida","Cerrada y no presentada"])]
    
    # Agrupar por "Comercial" y "Estado" y realizar las agregaciones
    nuevo_df_t = ventas_cerradas.groupby(['Comercial', 'Estado']).agg(Cantidad=('Estado', 'count')).reset_index()
    nuevo_df = nuevo_df_t.pivot_table(index='Comercial', columns='Estado',values='Cantidad')
    nuevo_df.reset_index(inplace=True)
    nuevo_df.columns.name = None
    nuevo_df = nuevo_df.fillna(0)
    return nuevo_df

def comercial_ventas(ventas):
    ventas = preprocesar(ventas)
    # sacamos las ventas
    nuevo_df = pd.DataFrame(ventas[ventas['Estado'] == 'Cerrada y ganada'].groupby('Comercial')['Importeprevisto'].sum())
    nuevo_df.reset_index(inplace=True)
    return nuevo_df

    