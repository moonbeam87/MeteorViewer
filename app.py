import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
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
def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with fig.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s


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
    ))
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
        style='dark'
    ),
)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Meteor Viewer'),

    html.Div(children='''
        Meteor Viewer: A web application that allows you to see all meteor strikes!.
    '''),

    dcc.Graph(
        id='my-graph',
        figure = fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)