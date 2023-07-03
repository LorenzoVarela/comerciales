import pandas as pd
from dash  import html, dcc, dash_table
import plotly.express as px
from urllib.parse import quote



def listar_comerciales(lista):
    data = [{'Columna':elemento} for elemento in lista]
    tabla = dash_table.DataTable(
        id='tabla',
        columns=[{'name': 'Columna', 'id': 'Columna'}],
        data=data,
        style_table={'width': '100%'},
        style_data={'whiteSpace': 'normal'},
    )
    return tabla


def graficas_comerciales(comerciales_lt, comercial_df, importes_df ) -> html.Div:

    # Empezamos con los gráficos
    # Comerciales
    fig_comerciales = px.bar(comercial_df, x='Comercial', y=['Cerrada y ganada','Cerrada y no presentada','Cerrada y perdida'], barmode='stack')
    fig_comerciales.update_layout(xaxis_tickangle=45)
    # ventas
    fig_ventas = px.bar(importes_df, x='Comercial', y=['Importeprevisto'])
    fig_ventas.update_layout(xaxis_tickangle=45)
    div = html.Div([
        html.Div([
#            dcc.Dropdown(
#            id='demo-dropdown',
#            options=[{'label': k, 'value': k} for k in comerciales_lt],
#            value=comerciales_lt,
#            multi=True
#        ),
#
#        html.Hr(),
        html.Div([dcc.Graph(id='display-selected-values', figure=fig_comerciales),],),
        html.Div([dcc.Graph(id='display-selected-values2', figure=fig_ventas),]),
        ])
    ])
    return div

def graficas_comercial(datos, fechas, nombre) -> html.Div:
    fig_comercial = px.treemap(datos, path=['Cliente'], values='Importeprevisto')
    fig_comercial.update_layout(height=900)

    fechas = fechas.sort_values('Fecha')
    fig_scatter = px.scatter(fechas, x='Fecha', y='Importeprevisto', color='Cliente')
    fig_scatter.update_layout(height=900)

    div = html.Div([
        html.H1(nombre), 
        html.Div([dcc.Graph(id='display-selected-values', figure=fig_comercial),],),
        html.Div([dcc.Graph(id='display-selected-values2', figure=fig_scatter),],),
    ])
    return div

# Tabla

def codificar_nombre(nombre):
    return quote(nombre)

# Crear los enlaces a los comerciales
def crear_enlace(nombre_comercial):
    nombre_codificado = codificar_nombre(nombre_comercial)
    enlace = f"/comerciales?nombre={nombre_codificado}"
    return html.A(nombre_comercial, href=enlace)

# Crear la tabla con los enlaces a los comerciales
def generar_tabla(comerciales):
    comerciales_lt = sorted(comerciales) 
    filas = []
    for i in range(0, len(comerciales_lt), 3):
        fila = [
            html.Td(crear_enlace(comerciales_lt[i])),
            html.Td(crear_enlace(comerciales_lt[i + 1])) if i + 1 < len(comerciales_lt) else html.Td(),
            html.Td(crear_enlace(comerciales_lt[i + 2])) if i + 2 < len(comerciales_lt) else html.Td()
        ]
        filas.append(html.Tr(fila))

    tabla = html.Table([
        html.Thead([
            html.Tr([
                html.Th("Comercial"),
                html.Th("Comercial"),
                html.Th("Comercial")
            ])
        ]),
        html.Tbody(filas)
    ])

    return tabla

#Tabla

