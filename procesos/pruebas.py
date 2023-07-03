import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el contenido de la página de inicio
layout_inicio = html.Div([
    html.H1('Página de Inicio'),
    # Aquí puedes agregar otros componentes según tus necesidades
])

# Definir el contenido de la página de comerciales
layout_comerciales = html.Div([
    html.H1('Página de Comerciales'),
    dcc.Dropdown(
        id='dropdown-comerciales',
        options=[
            {'label': 'Opción 1', 'value': 'opcion1'},
            {'label': 'Opción 2', 'value': 'opcion2'},
            # Agrega más opciones si es necesario
        ],
        value=None
    ),
    html.Div(id='output-comerciales')
])

# Definir la función de devolución de llamada para la página de comerciales
@app.callback(
    Output('output-comerciales', 'children'),
    [Input('dropdown-comerciales', 'value')]
)
def actualizar_imagenes_comerciales(opcion):
    # Aquí puedes realizar las acciones necesarias según la opción seleccionada
    # y retornar los componentes que deseas mostrar en la página
    if opcion == 'opcion1':
        return html.Img(src='imagen1.png')
    elif opcion == 'opcion2':
        return html.Img(src='imagen2.png')
    else:
        return html.Div()

# Definir la estructura de las rutas y el contenido de cada página
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        dcc.Link('Inicio', href='/', className='link'),
        dcc.Link('Comerciales', href='/comerciales', className='link'),
    ]),
    html.Div(id='page-content')
])

# Definir la función de devolución de llamada para actualizar el contenido de la página
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def cargar_pagina(pathname):
    if pathname == '/':
        return layout_inicio
    elif pathname == '/comerciales':
        return layout_comerciales
    else:
        return '404 - Página no encontrada'

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
