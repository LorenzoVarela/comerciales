# Imports
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px
import plotnine
from plotnine import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import folium

#from
from procesos.comerciales import comercial_estado, comercial_ventas
from procesos.ficheros import leer_comerciales
# Procesados, lectua del fichero

# leemos fichero origen
ventas = leer_comerciales("c:\datos\[OPORT021]_Oportunidades_con_multiples_filtros_RAW.xls")

# procesamso los datos en función del estado de las ofertas
# nuevo_df = comercial_estado(ventas)

# procesamso los datos en función del estado de las ofertas
comercial_df = pd.DataFrame(comercial_estado(ventas))


print (comercial_df.columns)
# Importe
importes_df = pd.DataFrame(comercial_ventas(ventas))


# Empezamos con los gráficos
# Comerciales
fig_comerciales = px.bar(comercial_df, x='Comercial', y=['Cerrada y ganada','Cerrada y no presentada','Cerrada y perdida'], barmode='stack')


# ventas
fig_ventas = px.bar(importes_df, x='Comercial', y=['Importeprevisto'])

# Extraemos la lista de los comerciales
df_sp = comercial_df['Comercial']
df_sp = df_sp.drop_duplicates()
df_sp.head()
comerciales=df_sp.tolist()


###############################
# Representamos
###############################

# Fijamos el tamaño de los gráficos.

fig_comerciales.layout(
    width=800,
    height=600
)

fig_ventas.layout(
    width=800,
    height=600
)


app = dash.Dash(__name__, assets_folder='assets/css')
app.layout = html.Div([

    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': k, 'value': k} for k in df_sp],
        value=comerciales,
        multi=True
    ),

     html.Hr(),
     html.Div([dcc.Graph(id='display-selected-values', figure=fig_comerciales),],),
     html.Div([dcc.Graph(id='display-selected-values2', figure=fig_ventas),]),
])

@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    dash.dependencies.Output('display-selected-values2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])

def update_output(value):
    ts = comercial_df[comercial_df["Comercial"].isin(value)]
    fig_a = px.bar(ts, x='Comercial', y=['Cerrada y ganada','Cerrada y no presentada','Cerrada y perdida'], barmode='stack')
    ts2 = importes_df[importes_df["Comercial"].isin(value)]
    fig_b = px.bar(ts2, x='Comercial', y=['Importeprevisto'])

    return fig_a, fig_b



if __name__ == '__main__':
    app.run_server(port=8052)