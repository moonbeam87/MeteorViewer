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

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color=mass,
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    ))

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
        hoverinfo='none'
    ))

fig.update_layout(
    title='Meteor Strikes Across the world',
    autosize=True,
    hovermode='closest',
    showlegend=True,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
        style='light'
    ),
)

fig.show()