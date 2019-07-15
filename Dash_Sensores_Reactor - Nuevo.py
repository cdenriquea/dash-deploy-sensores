import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import serial
import time
import plotly
import datetime
from collections import deque
import plotly.graph_objs as go
import random


GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL",1000)


app = dash.Dash(__name__, meta_tags=[{'name': 'dash-reactor-hidrogeno','content': 'Aplicacion que visualiza variables de un reactor de hidrogeno'},
                                     {'http-equiv': 'X-UA-Compatible','content': 'IE=edge'},
                                     {'name': 'viewport','content': 'width=device-width, initial-scale=1,maximum-scale=0.75'}])
server = app.server

#ARDUINO
#ser = serial.Serial('COM4', baudrate=9600,timeout=5)
#ser.flush()

##arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)
##arduino.setDTR(False)
##arduino.flushInput()
##time.sleep(1)
##arduino.setDTR(True)


#TAMAÑO ARREGLOS

tamaño = 50
tiempo = deque(maxlen=tamaño)
fixed_t=range(0,20,1)
t = deque(maxlen=100)
t.append(0)
Concentracion_H2 = deque(maxlen=tamaño)
Flujo_H2 = deque(maxlen=tamaño)
Presion_T = deque(maxlen=tamaño)
Generacion_V = deque(maxlen=tamaño)
Generacion_I = deque(maxlen=tamaño)
Generacion_P = deque(maxlen=tamaño)
Consumo_V = deque(maxlen=tamaño)
Consumo_I = deque(maxlen=tamaño)
Consumo_P = deque(maxlen=tamaño)



#DEFINICIONES


colores = {'fondo': '#FFFFFF','texto': '#111111'}#7FDBFF #082255

variables_1 = {"Concentracion H2":Concentracion_H2,
"Flujo H2":Flujo_H2,
"Presion tanque":Presion_T}


variables_2 = {"Generacion panel v": Generacion_V,
"Generacion panel i": Generacion_I,
"Generacion panel p": Generacion_P,}

variables_3 = {"Consumo reactor v":Consumo_V,
"Consumo reactor i":Consumo_I,
"Consumo reactor p":Consumo_P,}


unidades = {"Concentracion H2":"Concentracion [%H2]",
"Flujo H2":"Flujo [m3/s]",
"Presion tanque": "Presion [lbf/in2]",
"Generacion panel v": "Voltios[v]",
"Generacion panel i": "Amperios[i]",
"Generacion panel p": "Vatios[W]",
"Consumo reactor v": "Voltios[v]",
"Consumo reactor i": "Amperios[i]",
"Consumo reactor p": "Vatios[W]"}

relleno = {"Concentracion H2":"#B7E4F6",
"Flujo H2":"#C9C2FF",
"Presion tanque": "#DADADA",
"Generacion panel v": "#FCDEB8",
"Generacion panel i": "#EFF6C3",
"Generacion panel p": "#F2B2B2",
"Consumo reactor v": "#FCDEB8",
"Consumo reactor i": "#EFF6C3",
"Consumo reactor p": "#F2B2B2"}

linea = {"Concentracion H2":"#4C8DA8",
"Flujo H2":"#4C4DA8",
"Presion tanque": "#838383",
"Generacion panel v": "#A8804C",
"Generacion panel i": "#92A245",
"Generacion panel p": "#B64444",
"Consumo reactor v": "#A8804C",
"Consumo reactor i": "#92A245",
"Consumo reactor p": "#B64444"}


tabs_styles = {'height': '42px','position':'relative'}

tab_style = {'borderBottom': '1px solid #d6d6d6',
'padding': '6px','fontWeight': 'bold'}

tab_selected_style = {'borderTop': '1px solid #d6d6d6',
'borderBottom': '1px solid #d6d6d6',
'backgroundColor': '#119DFF',
'color': 'white',
'padding': '6px',}

grid = {0:'col s12 m6 l4', 1: 'col s12', 2: 'col s12 m6 l6', 3: 'col s12 m6 l4'}



#LECTURA DE DATOS


def datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P):

        #Recibir cadena de datos arduino
        #string_datos= ser.readline()
        #(H,F,G)= string_datos.decode().split(';')
        
        #Definir y truncar valores
        #CH ="{0:.1f}".format(float(H))
        #FH ="{0:.3f}".format(float(F))
        #GV =int(G)
        
        
        #Valores para grafica
        t.append(t[-1]+1)
        tiempo.append(datetime.datetime.now() - datetime.timedelta())
        Concentracion_H2.append("{0:.1f}".format(random.uniform(6.1,8.3)))
        Flujo_H2.append("{0:.1f}".format(random.uniform(10,13)))
        Presion_T.append(7)
        Generacion_V.append(t[-1])
        Generacion_I.append(random.randrange(0,40))
        Generacion_P.append(Generacion_V[-1]*Generacion_I[-1])
        Consumo_V.append(15)
        Consumo_I.append(random.randrange(0,12))
        Consumo_P.append(Consumo_V[-1]*Consumo_I[-1])
        

        return Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P

Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P = datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P)




#DISEÑO APLICACION 

app.layout = html.Div([

  dcc.Loading( id="loading-int",
  children=[html.Div([html.Div(id="loading-tab")])],
  fullscreen=True,
  type="cube"),


   dcc.Tabs(id="tabs",children=[
    

      ##TAB1
      
      dcc.Tab(value='tab-1',label='Sensores',style=tab_style, selected_style=tab_selected_style,
              children=html.Div([
              html.Div(className="row center-align",children=[
                       html.H6([html.H3([('Sensores CFIS')],className="center-align")],className="col s12 m12 l3"),

        html.P([html.Div(children='Play/Stop'),
        daq.PowerButton(
        id='Inicio',
        color='#FF5E5E',
        on=True,
        className='btn-floating pulse',
        )],className="col s2 m1 l1"), #Tamaño PLAY
                        
        html.Div([
        html.Div([
        html.Div([         
        html.P([
        daq.Indicator(
        id='indicador',
        label="Control",
        value=False,
        )                
        ],className="col s12 m12 l12"),

        html.Div([
        html.Button(
        'On/Off',
        id='Control',
        n_clicks=0,
        )
        ],className="col s12 m12 l12"),
        ],className="row"),
        ],className="valign-wrapper"),#hide-on-small-only
        ],className="col s2 m2 l0 "),#Tamaño Control
                              

   html.Div([
   html.Div([
   html.P([

    daq.LEDDisplay(
        id='led1',
        label="% H2",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        size=30,
        value=0,
        
    )
    ],className="col s4 m4 l4"),
                        
   html.P([

    daq.LEDDisplay(
        id='led2',
        label="Flujo H2",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        size=30,
        value=0,

         ),
      ],className="col s4 m4 l4"),
                        
    html.P([
    
     daq.LEDDisplay(
        id='led3',
        label="Presion T",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        size=30,
        value=0,

        ),
      ],className="col s4 m4 l4"),
   ],className="row"),
   ],className="col s8 m5 l3"),#Tamaño Leds

      html.P([
      html.Div([
      html.Div([
      html.Div([html.Div(children='Tanque'),
       daq.GraduatedBar(
       id='tanque_bar',
       step=2,
       color={"gradient":True,"ranges":{"green":[0,80],"yellow":[80,150],"red":[150,200]}},
       showCurrentValue=True,
       min=0,
       max=200,
       value=0,
       size=200,
       )                  
       ],className="col s6 m12 l12"),

       
        html.Div([html.Div(children='Zoom'),
        dcc.Slider(
        id='slider_1',
        min=0,
        max=20,
        step=5,
        value=0,
        updatemode='drag',
        marks={
              0: {'label': '0X'},
              5: {'label': '5X'},
              10: {'label': '10X'},
              15: {'label': '15X'},
              20: {'label': '20X'},
              },
        
        )
        ],className="col s6 m12 l12"),
        ],className="row"),
        ],className="container"),
        ],className="col s12 m4 l3"),#Tamaño zomm y tanque

    ]),             

     
    dcc.Loading(id="loading",
              children=[html.Div([html.Div(id="loading-output")])],
              type="default",
              #style={'display': 'none'}
              style={'position': 'absolute','float': 'left','left': '690px',
                      'margin-top':'-50px','margin-bottom': '10px'}
                ),
    
    html.Div(className='row',children=[
              html.Div([
                 dcc.Dropdown(id='tipo_sensor_1',
                 options=[{'label': s, 'value': s}
                 for s in variables_1.keys()],
                 value=['Concentracion H2','Flujo H2','Presion tanque'],
                 placeholder="Seleccionar sensor",
                 searchable=False,
                 multi=True,
                 style={'backgroundColor': colores['fondo']}
                 
                 ),
                 ],className="col s12 m12 l12"),
             html.Div([dcc.Graph(style={'height': '66vh'},id='graficas_1',animate=False )],
             className="col s12 m6 l8"),#Grafica 1/Contenedor 1
             html.Div([
             html.Div([
             html.Div([dcc.Graph(style={'height': '33vh'},id='graficas_1a',animate=False)
             ],className="col s6 m12 l12"),#Grafica 2
             html.Div([dcc.Graph(style={'height': '33vh'},id='graficas_1b',animate=False )
             ],className="col s6 m12 l12"),#Grafica 3
             ],className="row"),
             ],className="col s12 m6 l4"),#Contenedor 2
             ],style={'backgroundColor': colores['fondo']}),


  
           
        dcc.Interval(
        id='actualizar_1',
        interval=int(GRAPH_INTERVAL),
        n_intervals=0,
        ),
        dcc.Interval(
        id='actualizar_2',
        interval=5*1000,
        n_intervals=0,
        ),


    ])),
      
      ##TAB 2

      dcc.Tab(value='tab-2',label='Estadisticas',style=tab_style, selected_style=tab_selected_style)


  ],style=tabs_styles)
   

],style={'width':'97%','height':'100%','margin-left':10,'margin-right':10,'max-width':50000,
                                    'backgroundColor': colores['fondo']})


#ACTUALIZACION DE GRAFICAS Y FUNCIONES


@app.callback(
    [Output('led1', 'value'),
     Output('led2', 'value'),
     Output('led3', 'value')],
    [Input('actualizar_1', 'n_intervals')]) #Leds 1
def update_output(n):
    value=Concentracion_H2[-1]
    value1=Flujo_H2[-1]
    value2=Presion_T[-1]
    return str(value),str(value1),str(value2)

@app.callback(
    Output('actualizar_1', 'max_intervals'),
    [Input('Inicio', 'on')])
def update_output(on):
    if on is True:
       max_intervals=1000000000000
    else:
       max_intervals=0
    return max_intervals


@app.callback(
     Output('tanque_bar', 'value'),
    [Input('actualizar_1', 'n_intervals')]) #Tanque

def update_output(n):
    value=Presion_T[-1]
    return value

@app.callback(
     Output('indicador', 'value'),
    [Input('Control', 'n_clicks')] #Control
)
def update_output(value):
    if value % 2 is 0:
        value = True
    else: 
        value = False
    return value


@app.callback(
     Output('graficas_1','figure'),
    [Input('tipo_sensor_1', 'value'),Input('actualizar_1', 'n_intervals')])

def update_graph(seleccion,n):
        
       datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P)
       data=[]

       trace1=go.Scatter(
       x=list(tiempo),
       y=list(Flujo_H2),
       name='{}'.format(unidades['Concentracion H2']),
       line = dict(color = ('#fdae61'),width = 3,dash =None),
       mode='lines+markers',
       showlegend=True)

       trace2=go.Scatter(
       x=list(tiempo),
       y=list(Presion_T),
       name='{}'.format(unidades['Flujo H2']),
       line = dict(color = ('#5c39dd'),width = 3,dash ='dash'),
       mode='lines',
       showlegend=True)

       trace3=go.Scatter(
       x=list(tiempo),
       y=list(Concentracion_H2),
       name='{}'.format(unidades['Presion tanque']),
       mode='lines',
       fill='tozeroy',
       line=dict(color='rgb(127, 166, 238)',width=1),
       showlegend=True)

       data_dict = {"Concentracion H2":trace1,"Flujo H2":trace2,"Presion tanque":trace3}

       for sensor in seleccion:

           data.append(data_dict[sensor])

 
       figure1={'data': data,'layout' : go.Layout(paper_bgcolor=colores['fondo'],
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        legend=dict(orientation="v",x=0, y=1.1,font=dict(family='sans-serif',size=12,color='#000'),
                                                        bgcolor='rgba(0,0,0,0)',bordercolor='rgba(0,0,0,0)', borderwidth=2),
                                                        font={'color': colores['texto']},
                                                        xaxis=dict(range=[min(tiempo),max(tiempo)],title='Tiempo [s]', ticklen= 3,autorange=False, zeroline=False, gridwidth= 1),
                                                        yaxis=dict(ticklen= 3,autorange=True, gridwidth= 2,automargin=True),
                                                        margin={'l':25,'r':0,'t':40,'b':40},
                                                         )}


       return figure1


@app.callback(
    [Output('graficas_1a','figure'),Output('graficas_1b','figure')],
    [Input('actualizar_2', 'n_intervals')])

def update_graph(n):
        


        data1=go.Scatter(
        x=list(t),
        y=list(Generacion_P),
        name="G.Panel[Watts]",
        mode= "lines",
        showlegend=True,
            )

        data2=go.Bar(
        x=list(t),
        y=list(Consumo_P),
        name="C.Reactor[Watts]",
        showlegend=True,
            )

                                                
                                                        
        figure1={'data': [data1],'layout' : go.Layout(paper_bgcolor=colores['fondo'],
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        font={'color': colores['texto']},
                                                        legend=dict(orientation="v",x=0, y=1.1,font=dict(family='sans-serif',size=12,color='#000'),
                                                        bgcolor='rgba(0,0,0,0)',bordercolor='rgba(0,0,0,0)', borderwidth=2),
                                                        xaxis=dict(ticklen= 3,autorange=True, zeroline=False, gridwidth= 1),
                                                        yaxis=dict(title='Generacion',ticklen= 5,autorange=True, gridwidth= 2),
                                                        margin={'l':40,'r':0,'t':20,'b':20},
                                                         )}

        figure2={'data': [data2],'layout' : go.Layout(paper_bgcolor=colores['fondo'],
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        font={'color': colores['texto']},
                                                        legend=dict(orientation="v",x=0, y=1.1,font=dict(family='sans-serif',size=12,color='#000'),
                                                        bgcolor='rgba(0,0,0,0)',bordercolor='rgba(0,0,0,0)', borderwidth=2),
                                                        #transition={'duration': 5,'easing': 'cubic-in-out'},
                                                        xaxis=dict(title='Muestras', ticklen= 3,autorange=True, zeroline=False, gridwidth= 1),
                                                        yaxis=dict(title='Consumo',ticklen= 5,autorange=True, gridwidth= 2),
                                                        margin={'l':40,'r':0,'t':20,'b':40},
                                                      
                                                         )}







        return figure1, figure2





@app.callback(Output("loading-output", "children"), [Input("tipo_sensor_1", "value")])
def delay(value):
    time.sleep(0.3)
    return None




@app.callback(
        [Output("loading-tab", "children"),Output("loading-int", "type")], [Input("tabs", "value")])
def delay(tab):
    type='graph'
    time.sleep(0)        
    return None,type



if __name__ == '__main__':
    app.run_server(debug=True)

