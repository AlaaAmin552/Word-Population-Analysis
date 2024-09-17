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
app = dash.Dash(__name__)
app.layout=html.Div(children=[
    html.Img(src='/assets/header.png',style={'width':'100%',
             'height':'50%',
             'margin':'0auto'}),
    html.H1("Medical requirments company",
            style={'color':'#273943',
                   'textAlign':'center',
                   'padding-top':'10px'}),
    html.Div(children=[
        dcc.Dropdown(
            id="continent",
            options=[{'label': con, 'value': con} for con in cleaned_data['Continent'].unique()],
            value=cleaned_data['Continent'].unique()[0]
        )
    ]),
    html.Div(children=
             dcc.Graph(id="child")
    ),
    html.Div(children=[
        dcc.Graph(id="old",style={'width':'50%','display':'inline-block'}),
        dcc.Graph(id="growth",style={'width':'50%','display':'inline-block'})
    ]),
    html.Div(children=[
        dcc.Graph(
            id = "density"
        )
    ]),
    html.Div(children=[
        dcc.Graph(
            id = "Area"
        )
    ])
])
@app.callback(
    Output("child","figure"),
    [Input("continent","value")]
)
def update_child(selected):
    con_df = cleaned_data[cleaned_data['Continent'] == selected]
    large_num_of_children = px.scatter(con_df, x='Country', y='Growth Rate', size='2022 Population',size_max=60,
                    hover_data=['1990 Population', '2022 Population'],
                    title=f'Countries in {selected} with Large Number of Children (Growth Rate and Population)',
                    labels={'Growth Rate': 'Population Growth Rate (%)', '2022 Population': 'Population in 2022'})

    large_num_of_children.update_layout(xaxis_showgrid=False,
                                         yaxis_showgrid=False,
                                         height = 750)
    return large_num_of_children
@app.callback(
    Output("old","figure"),
    [Input("continent","value")]
)
def update_child(selected):
    con_df = cleaned_data[cleaned_data['Continent'] == selected]
    large_num_of_elder_people = px.bar(con_df, x='2022 Population', y='Country', color='Growth Rate',
                hover_data=['World Population Percentage'],
                    title=f'Countries in {selected} with Large Number of Elderly People',
                    orientation='h')
    large_num_of_elder_people.update_coloraxes( colorbar=dict(
        tickvals=[],       
        title=None ))
    large_num_of_elder_people.update_layout(xaxis_title='Country', yaxis_title='Population in 2022')
    large_num_of_elder_people.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    return large_num_of_elder_people
@app.callback(
    Output("growth","figure"),
    [Input("continent","value")]
)
def update_child(selected):
    con_df = cleaned_data[cleaned_data['Continent'] == selected]
    df_sorted = con_df.sort_values(by='Growth Rate', ascending=False)
    high_pop_growth = px.bar(df_sorted, x='Growth Rate', y='Country',orientation='h',
               hover_data=['2022 Population'],
               title=f'Countries in {selected} with High Population Growth',
               labels={'Growth Rate': 'Population Growth Rate (%)', 'Country': f'Countries in {selected}'},
               color='World Population Percentage')
    high_pop_growth.update_coloraxes( colorbar=dict(
        tickvals=[],       
        title=None ))
    return high_pop_growth
@app.callback(
    Output("density","figure"),
    [Input("continent","value")]
)
def update_child(selected):
    con_df = cleaned_data[cleaned_data['Continent'] == selected]
    high_pop_density_treemap = px.treemap(
    con_df,
    path=['Continent', 'Country'],
    values='Density (per km²)',     
    hover_data=['Area (km²)', 'Density (per km²)'], 
    title=f'Countries in {selected} with High Population Density'
)
    return high_pop_density_treemap
@app.callback(
    Output("Area","figure"),
    [Input("continent","value")]
)
def update_child(selected):
    con_df = cleaned_data[cleaned_data['Continent'] == selected]
    high_pop_Area_treemap = px.treemap(
    con_df,
    path=['Continent', 'Country'], 
    values='Area (km²)',     
    hover_data=['2022 Population', 'Density (per km²)'],
    title=f'Countries in {selected} with High Area'
)
    return high_pop_Area_treemap
if __name__ == '__main__':
    app.run_server(debug=True)