import numpy as np
import pandas as pd
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
cols = ['2022 Population', 'Growth Rate',  'World Population Percentage', 'Area (km²)', 'Density (per km²)']
app = dash.Dash(__name__)
options = [{'label': col, 'value': col} for col in cols]
cor = cleaned_data.corr(numeric_only=True)
pops = ['2022 Population','2020 Population','2015 Population','2010 Population','2000 Population','1990 Population','1980 Population','1970 Population']
text = np.round(cor.values, 2).astype(str)
corelation_map = go.Figure(data=go.Heatmap(
    z = cor.values,
    x = cor.columns,
    y=cor.columns,
    zmin = -1 , zmax = 1,
    colorscale='blues',
    colorbar=dict(title="Correlation"),
    text=text
))
corelation_map.update_traces(text=text, texttemplate="%{text}", textfont_size=12)
corelation_map.update_layout(title = {"text":"Correlation Heatmap",'x':.5,'xanchor':'center','yanchor':'top'},
                             xaxis_nticks=36,
                             plot_bgcolor='#caf0f8',
                             paper_bgcolor='#caf0f8',
                             font=dict(color='#03045e'),
                             height=750)
top_10_growth_rate = cleaned_data.sort_values(by='Growth Rate', ascending=False).head(10)
data1 = [go.Bar(
                y = top_10_growth_rate['Country'],
                x = top_10_growth_rate['Growth Rate'],
                orientation='h',marker=dict(colorscale='Viridis'))]
top10_growth = go.Figure(data = data1)
top10_growth.update_layout(
    title = {"text":"Top 10 Countries by Growth Rate",'x':.5,'xanchor':'center','yanchor':'top'},
                            xaxis_nticks=36,
                             plot_bgcolor='#caf0f8',
                             paper_bgcolor='#caf0f8',
                             font=dict(color='#03045e'),
                             xaxis=dict(showgrid=False),
                             yaxis=dict(showgrid=False)
)
lowest_10_growth_rate = cleaned_data.sort_values(by='Growth Rate', ascending=True).head(10)
data2 = [go.Bar(
                y = lowest_10_growth_rate['Country'],
                x = lowest_10_growth_rate['Growth Rate'],
                orientation='h',
                marker=dict(colorscale='Viridis'))]
low10_growth = go.Figure(data = data2)
low10_growth.update_layout(
    title = {"text":"Lowest 10 Countries by Growth Rate",'x':.5,'xanchor':'center','yanchor':'top'},
                            xaxis_nticks=36,
                             plot_bgcolor='#caf0f8',
                             paper_bgcolor='#caf0f8',
                             font=dict(color='#03045e'),
                             xaxis=dict(showgrid=False),
                             yaxis=dict(showgrid=False)
)
population_by_continent = cleaned_data.groupby('Continent').sum()[pops]
pie_con = px.pie(population_by_continent, values='2022 Population', names=population_by_continent.index,hole=0.6)
pie_con.update_layout(
    title = {"text":"Population per continent",'x':.5,'xanchor':'center','yanchor':'top'},
    xaxis_nticks=36,
    plot_bgcolor='#caf0f8',
    paper_bgcolor='#caf0f8',
    font=dict(color='#03045e'),
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [{"values": [population_by_continent['2022 Population']]}],
                    "label": "2022",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['2020 Population']]}],
                    "label": "2020",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['2015 Population']]}],
                    "label": "2015",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['2010 Population']]}],
                    "label": "2010",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['2000 Population']]}],
                    "label": "2000",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['1990 Population']]}],
                    "label": "1990",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['1980 Population']]}],
                    "label": "1980",
                    "method": "restyle"
                },
                {
                    "args": [{"values": [population_by_continent['1970 Population']]}],
                    "label": "1970",
                    "method": "restyle"
                }
            ],
            
            "direction": "right",
            "showactive": True
        }
    ]
)
countries_per_continent = cleaned_data['Continent'].value_counts()
pie_num = px.pie(countries_per_continent, values=countries_per_continent.values,
             names=countries_per_continent.index, title="Number of Countries per Continent",
             hole=0.6)
pie_num.update_layout(
    title = {"text":"Number of Countries per Continent",'x':.5,'xanchor':'center','yanchor':'top'},
    xaxis_nticks=36,
    plot_bgcolor='#caf0f8',
    paper_bgcolor='#caf0f8',
    font=dict(color='#03045e')
)
population_by_year = cleaned_data[pops].sum().T.reset_index()
population_by_year.columns = ['Year', 'Total Population']
population_by_year['Year'] = pd.to_numeric(population_by_year['Year'].str.replace(' Population', ''))
line_trend = px.line(population_by_year, x='Year', y='Total Population')
line_trend.update_layout(
    xaxis_nticks=36,
    plot_bgcolor='#caf0f8',
    paper_bgcolor='#caf0f8',
    font=dict(color='#03045e'),
    xaxis = dict(showgrid=False),
    yaxis = dict(showgrid=False)
)
app.layout = html.Div(children=[
    html.Div(children=[
        html.Img(src='/assets/header.jpg',style={'width':'100%',
             'height':'50%',
             'margin':'0auto'})
    ]
             ),
    html.Div(children=[html.H1("Explatory Data analysis", style={"textAlign": "center",
                                                   'color': '#03045e',
                                                   'background-color':'#caf0f8',
                                                   'padding-top':'10px'}),
                       dcc.Dropdown(id='column-dropdown',
                                    options=options,
                                    value=cols[0],style={'margin':'0 auto',                                                          
                                                         'width':'100%'}
        )],style={'background-color': '#caf0f8',
                  'width': '100%',
                  'margin':'0 auto'}),
    html.Div(children=[
                        dcc.Graph(
                            id="Null_values",
                            style={"border": "5px solid #caf0f8",
                                'width': '100%',
                                'height': '100%',
                                'display': 'inline-block',
                                'margin':'0 auto'}
        )],style={'background-color': '#caf0f8',
                  'width': '50%',
                  'height': '500px',
                  'display':'inline-block',
                  'margin':'0 auto',
                  'vertical-align': 'top'}),
    html.Div(children=[
        dcc.Graph(
            id="box_ouliars",
            style={'display': 'inline-block',
                   'height':'100%',
                   'margin':'0 auto',
                   'width': '100%'}
        )
    ], style={'background-color': '#caf0f8', 
              'width': '50%',
              'height': '500px',
              'display':'inline-block',
              'margin':'0 auto',
              'vertical-align': 'top'}),
    html.Div(children=[
        dcc.Graph(id="hist_distributions",
                  style={
                   'height':'100%',
                   'margin':'0 auto',
                   'width': '100%'
                  })
    ]),
    html.Div(children=[
        html.Img(src=r'\assets\insights1.jpg',style={
            'width':'100%',
            'height':'25%',
            'box-shadow': '0px 2px 5px rgba(0,0,0,.2)'
        })
    ]),
    html.H2("Relationship between different columns",
            style={
                'textAlign':'center',
                'color': '#03045e',
                'background-color':'#caf0f8',
                'padding-top':'20px'
            }),
    html.Div(
        dcc.Graph(
            figure=corelation_map,
            id='corelation'
        )
    ),
    html.H2("Top V.s low countries by growth rate",
            style={
                'textAlign':'center',
                'color': '#03045e',
                'background-color':'#caf0f8',
                'padding-top':'10px'
            }),
    html.Div(children=[
        dcc.Graph(
            figure=top10_growth,
            style={
                'width':'50%',
                'height':'100%',
                'display':'inline-block'
            }
        ),
        dcc.Graph(figure=low10_growth,
            style={
                'width':'50%',
                'height':'100%',
                'display':'inline-block'
            })
    ]
    ),
    html.H2("Population Distribution by Continent",
            style={
                'textAlign':'center',
                'color': '#03045e',
                'background-color':'#caf0f8',
                'padding-top':'10px'
            }),
    html.Div(children=[
        dcc.Graph(
            figure=pie_con
        )],
        style={'width':'50%',
                   'display':'inline-block',
                   'vertical-align': 'top',
                   'margin':'0 auto',
                   'justify-content': 'space-around',
                   'height' : '500px',
                   'padding-top':'14px'}
        ),
    html.Div(children=[
        dcc.Graph(
            figure=pie_num
        )],
        style={'width':'50%',
                   'display':'inline-block',
                   'vertical-align': 'top',
                   'margin':'0 auto',
                   'justify-content': 'space-around',
                   'height' : '500px'}
        ),
    html.H2("Changing of total population over the years",
            style={
                'textAlign':'center',
                'color': '#03045e',
                'background-color':'#caf0f8',
                'padding-top':'10px'
            }),
    html.Div(
        dcc.Graph(
            figure=line_trend
        )
    ),
    html.Div(children=[
        html.Img(src=r'\assets\insights2.jpg',style={
            'width':'100%',
            'height':'25%',
            'box-shadow': '0px 2px 5px rgba(0,0,0,.2)'
        })
    ]),
    html.Div(children=[
        html.Img(src=r'\assets\End_EDA.jpg',style={
            'width':'100%',
            'height':'25%',
            'box-shadow': '0px 2px 5px rgba(0,0,0,.2)'
        })])
    ])
@app.callback(
    Output('box_ouliars', 'figure'),
    [Input('column-dropdown', 'value')]
)
def update_box_plot(selected_column):
    box_outliars = px.box(x=selected_column,
                        data_frame=raw_data, 
                        orientation='h',
                        color_discrete_map={'category_name': '#03045e'})
    box_outliars.update_traces(marker_color='#03045e',customdata=raw_data[['Country']].values,
            hovertemplate='Country: %{customdata}<br>Value: %{y}<br>Median: %{median}<br>Q1: %{q1}<br>Q3: %{q3}<extra></extra>')
    box_outliars.update_layout(
    title = {'text':f'describtion & outlier testing of {selected_column}','x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
    xaxis_title="Values",
    yaxis_title=selected_column,
    boxmode='group',
    plot_bgcolor='#caf0f8',
    paper_bgcolor='#caf0f8',
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    xaxis_linecolor='#03045e',
    yaxis_linecolor='#03045e', 
    xaxis_tickfont=dict(color='#03045e'),
    yaxis_tickfont=dict(color='#03045e'),
    xaxis_title_font=dict(color='#03045e'),
    yaxis_title_font=dict(color='#03045e') 
    )
    return box_outliars
@app.callback(
    Output('Null_values', 'figure'),
    [Input('column-dropdown', 'value')]
)
def update_null_graph(selected_column):
    null_data = raw_data[selected_column].isna().astype(int).values
    null_representation = go.Figure()
    null_representation.add_trace(go.Heatmap(
        z=[null_data],
        colorscale=["#caf0f8", "#03045e"],
        showscale=True,
        colorbar=dict(
            tickcolor='#03045e',
            tickfont=dict(color='#03045e')
        )
    ))
    null_representation.update_layout(
        title={'text': f'Null Values in {selected_column}', 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
        xaxis=dict(title="Index", color='#03045e', title_standoff=20),
        yaxis=dict(title="Null Values", color='#03045e', title_standoff=20),
        plot_bgcolor='#caf0f8',
        paper_bgcolor='#caf0f8',
        font=dict(color='#03045e')
    )
    return null_representation
@app.callback(
    Output('hist_distributions', 'figure'),
    [Input('column-dropdown', 'value')]
)
def update_hist(selected_column):
    hist = px.histogram(df, x=raw_data[selected_column], title=f"Distribution of {raw_data[selected_column]}")
    hist.update_traces(hovertemplate=raw_data['Country'] + '<br>' + '%{x}: %{y}<extra></extra>',
                       customdata=df[['Country']].values,
                       marker_color='#03045e')
    hist.update_layout(
        title={'text': f'Frequency of {selected_column}', 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
        xaxis=dict(title=selected_column, color='#03045e', title_standoff=20,showgrid=False),
        yaxis=dict(title="Count", color='#03045e', title_standoff=20,showgrid=False),
        plot_bgcolor='#caf0f8',
        paper_bgcolor='#caf0f8',
        font=dict(color='#03045e')
    )
    return hist
if __name__ == '__main__':

    app.run_server(debug=True)