import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from plotly.subplots import make_subplots


external_stylesheets = ['https://codepen.io/moonbeam87/pen/bGdpwYe.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#import meteorData
mapbox_access_token = "pk.eyJ1IjoibW9vbmJlYW04NyIsImEiOiJjazZsajRsamwwMjJuM21udjhvZzBwcnN6In0.85-_7ylp9qSaMlAvrFpRRg"
##replace Link with MeteorData.csv
df = pd.read_csv('https://raw.githubusercontent.com/moonbeam87/MeteorViewer/master/meteorData.csv')
#df = pd.read(meteorData.csv)
site_lat = df.reclat
site_lon = df.reclong
locations_name = df.name
locations_nameType = df.nametype
mass = df.mass
recclass = df.recclass
colorIdentifier = mass
fig = go.Figure()
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
fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color=colorIdentifier,
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    )
)
#Contrast on trace (Not enabled currently)
"""
fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
        hoverinfo='text'
    ))
"""
#Update on resize
fig.update_layout(
    title='',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
        style='mapbox://styles/srepho/cjttho6dl0hl91fmzwyicqkzf'
    ),
)

fig1 = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "box"}]]
)
fig1.add_trace(
    go.Box(
        x=mass,
        name="Asteroid Mass Box Plot"
    ),
    row=2, col=1
)

fig1.add_trace(
    go.Table(
        header=dict(
            values=["Date", "Number<br>Transactions", "Output<br>Volume (BTC)",
                    "Market<br>Price", "Hash<br>Rate", "Cost per<br>trans-USD",
                    "Mining<br>Revenue-USD", "Trasaction<br>fees-BTC"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[1:]],
            align = "left")
    ),
    row=1, col=1
)
fig1.update_layout(
    height=800,
    showlegend=False,
    title_text="Meteor Data from 1850-2020",
)
#Dash App Layout
app.layout = html.Div(children=[
    html.H1(children='Meteor Viewer'),

    html.H2(children='''
        Meteor Viewer: A web application that allows you to see all meteor strikes!.
    '''),

    dcc.Graph(
        id='my-graph',
        figure = fig
    ),
    html.H2(children = ''' '''),
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
    dcc.Graph(
        id='my-graph-2',
        figure = fig1
    ),
    
])
#Run App
if __name__ == '__main__':
    app.run_server(debug=True)