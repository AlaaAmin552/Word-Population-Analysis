import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go 
import dash
from dash import dcc, html
from dash.dependencies import Input, Output 

def clean_df(df):
    cleaned_data = df
    total_population = cleaned_data['2022 Population'].sum()
    mask = (cleaned_data['World Population Percentage'] == 0) & (cleaned_data['2022 Population'].notna())
    cleaned_data.loc[mask, 'World Population Percentage'] = cleaned_data.loc[mask, '2022 Population'] / total_population
    pops = ['2022 Population','2020 Population','2015 Population','2010 Population','2000 Population','1990 Population','1980 Population','1970 Population']
    for pop in pops:
        total_population = cleaned_data[pop].sum()
        mask1 = (cleaned_data[pop].isna())
        cleaned_data.loc[mask1,pop] = cleaned_data.loc[mask1,'World Population Percentage'] * total_population
    cleaned_data.loc[cleaned_data['Country'] == 'Venezuela', 'Area (km²)'] = 916445
    cleaned_data.loc[cleaned_data['Country'] == 'Senegal', 'Area (km²)'] = 196722
    cleaned_data.loc[cleaned_data['Country'] == 'Senegal', 'Density (per km²)'] = 85
    cleaned_data.loc[cleaned_data['Country'] == 'Ivory Coast', 'Density (per km²)'] = 86
    cleaned_data.loc[cleaned_data['Country'] == 'Ivory Coast', 'Growth Rate'] = 2.6
    cleaned_data.loc[cleaned_data['Country'] == 'Trinidad and Tobago', 'Density (per km²)'] = 281
    cleaned_data.loc[cleaned_data['Country'] == 'Jamaica', 'Density (per km²)'] = 274
    cleaned_data.loc[cleaned_data['Country'] == 'Jamaica', 'Growth Rate'] = 0.7
    cleaned_data.loc[cleaned_data['Country'] == 'Thailand', '1970 Population'] = 3284365
    cleaned_data.loc[cleaned_data['Country'] == 'India', '1980 Population'] = 557501301
    cleaned_data.loc[cleaned_data['Country'] == 'India', '1990 Population'] = 696828385
    cleaned_data.loc[cleaned_data['Country'] == 'Mozambique', '2015 Population'] = 11413587
    cleaned_data.loc[cleaned_data['Country'] == 'Mozambique', '2010 Population'] = 23073723
    cleaned_data.loc[cleaned_data['Country'] == 'Colombia', '2010 Population'] = 44816108
    cleaned_data.loc[cleaned_data['Country'] == 'Malaysia', '2010 Population'] = 2807731
    cleaned_data.loc[cleaned_data['Country'] == 'Zambia', '2015 Population'] = 16248230
    cleaned_data.loc[cleaned_data['Country'] == 'Malaysia', '2000 Population'] = 22945150
    cleaned_data.loc[cleaned_data['Country'] == 'Somalia', '1970 Population'] = 3720977
    cleaned_data.loc[cleaned_data['Country'] == 'Venezuela', '2000 Population'] = 2442779
    cleaned_data[pops] = cleaned_data[pops].astype(int)
    cleaned_data['Growth Rate'] = np.round(cleaned_data['Growth Rate'],3)
    cleaned_data[['Density (per km²)','Area (km²)']]= np.round(cleaned_data[['Density (per km²)','Area (km²)']],2)
    cleaned_data['World Population Percentage'] = cleaned_data['World Population Percentage'] * 100
    return cleaned_data
df = pd.read_csv(r"E:\programming\Dash\world_population.csv")
df1 = df.copy()
raw_data = df
cleaned_data = clean_df(df1)
cols = ['Area (km²)','Density (per km²)','Growth Rate','World Population Percentage']
data = cleaned_data[['CCA3', 'Country','2022 Population','2020 Population','2015 Population','2010 Population','2000 Population','1990 Population','1980 Population','1970 Population']]
map1 = px.choropleth(data,
                    locations="CCA3",
                    color="2022 Population",
                    hover_name="Country",
                    projection="natural earth",
                    color_continuous_scale="YlOrBr")
map1.update_coloraxes( colorbar=dict(
        tickvals=[],       
        title=None ,
        len = .5
    ))
for year in ['2020 Population', '2015 Population', '2010 Population', '2000 Population', '1990 Population', '1980 Population', '1970 Population']:
    map1.add_trace(px.choropleth(data,
                            locations="CCA3",
                            color=year,
                            hover_name="Country",
                            projection="natural earth",
                            color_continuous_scale="Viridis").data[0])
map1.update_layout(
    geo=dict(
        bgcolor="black"
    ),
    width = 1200,
    height = 1000,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='#ffca2b'),
    title = {'text':'World population number across years','x':.5,'y':.2,'xanchor':'center','yanchor':'top'},
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[{"visible": [True, False, False, False, False, False, False, False]}],
                    label="2022",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False, False, False, False, False, False]}],
                    label="2020",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, True, False, False, False, False, False]}],
                    label="2015",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, False, True, False, False, False, False]}],
                    label="2010",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, False, False, True, False, False, False]}],
                    label="2000",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, False, False, False, True, False, False]}],
                    label="1990",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, False, False, False, False, True, False]}],
                    label="1980",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, False, False, False, False, False, True]}],
                    label="1970",
                    method="update"
                )
            ]),
            direction="down",

            showactive=True
        )
    ]
)
app = dash.Dash(__name__)
app.layout = html.Div(children = [
    html.Div(children =[
        html.Img(src='/assets/header.png',style={'width':'100%',
             'height':'50%',
             'margin':'0auto'})]),
    html.H1("Demographical analysis",
            style={'color':'#ffca2b',
                   'textAlign':'center',
                   'padding-top':'10px'}),
    html.Div(children=[
        dcc.Graph(figure=map1,
                  style={
                      'width':'100%',
                      'margin':'0 auto'
                  })
    ]
    ),
    html.Div(children=[
        html.H2("Distribution of features arround the world",style={'color':'#ffca2b',
                   'textAlign':'center'}),
        dcc.Dropdown(id="columns",
                     options=[{'label': col, 'value': col} for col in cols],value=cols[0])
]),
    html.Div(children=(
        dcc.Graph(
            id = "map2"
        )
    ))
])
@app.callback(
    Output("map2", "figure"),
    [Input("columns", "value")],
)
def update_map(selected_column):
    # Check if selected column is numeric
    if not pd.to_numeric(cleaned_data[selected_column], errors='coerce').notnull().all():
        return go.Figure(data=[go.Layout(title="Invalid column selected: Data must be numeric")])

    # Check for valid CCA3 codes
    invalid_cca3 = cleaned_data[cleaned_data['CCA3'].isna()]
    if not invalid_cca3.empty:
        return go.Figure(data=[go.Layout(title="Invalid CCA3 codes found in data")])

    map2 = px.scatter_geo(cleaned_data, locations="CCA3", locationmode="ISO-3",
                          size=selected_column,
                          hover_name="Country",
                          projection="natural earth",
                          title=f"World {selected_column} Distribution",
                          size_max=50)
    if selected_column == 'Growth Rate':
        map2.update_traces(marker=dict(sizeref=max(cleaned_data[selected_column])**15,sizemin=5))
    else:   
        map2.update_traces(marker=dict(sizeref=2.*max(cleaned_data[selected_column])/(50.**2),
                                        sizemin=3))
    map2.update_layout(
    geo=dict(
        bgcolor="black"
    ),
    width = 1200,
    height = 750,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='#ffca2b'),
    title = {'text':f'{selected_column} Distribution','x':.5,'y':.1,'xanchor':'center','yanchor':'top'}
    )

    return map2
if __name__ == "__main__":
    app.run_server(debug=True)