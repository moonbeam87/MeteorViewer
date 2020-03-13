import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import wikipedia
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#import meteorData
mapbox_access_token = "pk.eyJ1IjoibW9vbmJlYW04NyIsImEiOiJjazZsajRsamwwMjJuM21udjhvZzBwcnN6In0.85-_7ylp9qSaMlAvrFpRRg"
##replace Link with MeteorData.csv
df = pd.read_csv('https://raw.githubusercontent.com/moonbeam87/MeteorViewer/master/meteorDataNew.csv')
#df = pd.read(meteorData.csv)
site_lat = df.reclat
site_lon = df.reclong
locations_name = df.name
locations_nameType = df.nametype
mass = df.mass
year = df.year
recclass = df.recclass
colorIdentifier = mass
px.set_mapbox_access_token(mapbox_access_token)

custom_style = "mapbox://styles/shaz13/cjiog1iqa1vkd2soeu5eocy4i"
fig = px.scatter_mapbox(df, title="Meteor Strikes Visualized by Mass",lat="reclat", lon="reclong", color="mass", size="mass", hover_name="name",
    color_continuous_scale=px.colors.sequential.Inferno, size_max=120,zoom=0)
#Current doesn't do anything on click :(
def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with fig.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s
#Placing a point on the graph
fig1 = make_subplots(
    rows=4, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "box"}],
           [{"type": "violin"}],
           [{"type": "scatter"}]]
)
fig1.add_trace(
    go.Scatter(
        y=mass,
        x=year,
        name="Asteroid Date v Mass Scatter Plot"
    ),
    row=4, col=1
)
fig1.add_trace(
    go.Violin(
        x=mass,
        name="Asteroid Mass Violin Plot"
    ),
    row=3, col=1
)
fig1.add_trace(
    go.Box(
        x=mass,
        notched=True,
        fillcolor= 'purple',
        jitter=0.3,
        name="Asteroid Mass Box Plot"
    ),
    row=2, col=1
)

fig1.add_trace(
    go.Table(
        header=dict(
            values=["name", "id", "nametype", "recclass", "mass", "fall"
                    , "date", "reclat", "reclong"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:9]],
            align = "left"),
    ),
    row=1, col=1
)
fig1.update_layout(
    height=800,
    showlegend=False,
    title_text="Meteor Data from 1000 AD-2011",
)
#Deprecated Dropdown menu
"""
    dcc.Dropdown(
    options=[
        {'label': 'Sort by Mass', 'value': 'mass'},
        {'label': 'Sort by Fall (fell vs found)', 'value': 'fall'},
        {'label': 'Sort by Year', 'value': 'year'},
        {'label': 'Sort by Name', 'value': 'name'},
    ],
    value='name',
    clearable=False
    ),
    """,
s = ""
#Dash App Layout
app.layout = html.Div(children=[
    html.H1(children='Meteor Strike Viewer'),

    html.H3(children='''
        Meteor Viewer: A web application that allows you to see all meteor strikes!
    '''),
    html.H4(children='''
        New Features: Wikepedia Summary based on Dropdown
    '''),
    html.H4(children='''
        Upcoming Features: CSV Dump, API, Location filtering
    '''),
    dcc.Dropdown(
    id = 'WikiDropDown',
    options=[
        {'label': 'Info on Largest Meteor', 'value': 'sikhote alin meteorite'},
        {'label': 'Info on Meteors', 'value': 'meteor'},
        {'label': 'Info on NASA', 'value': 'NASA'},
        {'label': 'Info on Meteorites', 'value': 'meteorites'},
    ],
    value='meteor',
    clearable=False
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id='my-graph',
        figure = fig
    ),
    html.H2(children = ''' '''), 
    
    dcc.Graph(
        id='my-graph-2',
        figure = fig1
    ),
    
])
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('WikiDropDown', 'value')])
def update_output(value):
    if(value == 'sikhote alin meteorite'):
        s = wikipedia.summary(value, sentences=2)
    else:
        s = (wikipedia.summary(value))
    return s
#Run App
if __name__ == '__main__':
    app.run_server(debug=True)