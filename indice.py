import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from urllib.parse import parse_qs

from procesos.comerciales import comerciales_estado, comerciales_ventas, comercial_ventas, preprocesar, lista_comerciales, comercial_fechas
from procesos.ficheros import leer_comerciales
from procesos.comerciales_representacion import graficas_comerciales, graficas_comercial, generar_tabla

ventas = None
comerciales_df = None
importes_df = None
comercial_df = None
comerciales_lt = None

ventas = leer_comerciales("c:\datos\[OPORT021]_Oportunidades_con_multiples_filtros_RAW.xls")
print('Primera lectura')
ventas = preprocesar(ventas)
comerciales_lt = lista_comerciales(ventas)
comerciales_df = pd.DataFrame(comerciales_estado(ventas))
importes_df = pd.DataFrame(comerciales_ventas(ventas))



app = dash.Dash(__name__, suppress_callback_exceptions=True)

layout_inicio = html.Div([
    html.H1('Página Principal'),
    graficas_comerciales(comerciales_lt, comerciales_df, importes_df),
    generar_tabla(comerciales_lt),
])

layout_comerciales = html.Div([
    html.Div(id='comercial-content')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# @app.server.before_first_request
# def inicializar():
#     print("inicializar_datos")
#     inicializar_datos()

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        print('diplay_page')
        return layout_inicio
    elif pathname == '/comerciales':
        return layout_comerciales
    else:
        return 'Página no encontrada'


@app.callback(Output('comercial-content', 'children'), [Input('url', 'search')])
def display_comercial(search):
    params = parse_qs(search[1:])
    nombre_comercial = params.get('nombre', [''])[0]
    comercial_df = comercial_ventas(ventas, nombre_comercial)
    fechas_df = comercial_fechas(ventas, nombre_comercial)
    return graficas_comercial(comercial_df,fechas_df, nombre_comercial)


if __name__ == '__main__':
    app.run_server(debug=True)
