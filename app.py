
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import statsmodels.api as sm

#Importing data----------------------------------------------------------------------------------------------

path = 'https://github.com/rsoromenho/World_Happiness/tree/main/datasets'
df_1 = pd.read_csv(path + 'df_15_19.csv')
df_2 = pd.read_csv(path + 'happiness-cantril-ladder.csv')
df_15_19_code = pd.read_csv(path + 'df_15_19_code.csv')
df_tab1_test = pd.read_csv(path + 'tab1_test.csv')
df_gdp = pd.read_csv(path + 'df_gdp.csv') 

colors = {
    'background': '#FFD300',#C4E8FA
    'text': 'black'
}

# -----------Dropdowns, Slicers and Radios  -----------------------------------------------------------------

#Creating dropdown, radio and slider for df1
country_options = [
    dict(label='' + country, value=country)
    for country in df_1['Country'].unique()]

indicator_options = [
    dict(label=''+indicator, value=indicator)
    for indicator in df_1.columns[3:9]]

region_options = [
    dict(label='' + region, value=region)
    for region in df_1['Region'].unique()]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    )

dropdown_country1 = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    )

dropdown_country2 = dcc.Dropdown(
        id='country_drop2',
        options=country_options,
        value=df_1[df_1['Year']==2019]['Country'].unique(),
        multi=True
    )

dropdown_country3 = dcc.Dropdown(
        id='country_drop3',
        options=country_options,
        value=df_tab1_test['Country'].unique()[:30],
        multi=True
    )

dropdown_region = dcc.Checklist(
        id='region_drop',
        options=region_options,
        value=df_1['Region'].unique(),
        labelStyle={'display': 'inline-block'}
    )

radio_indicator = dcc.RadioItems(
        id='indicator_radio',
        options=indicator_options,
        value='Happiness Score',
        labelStyle={'display': 'block'}
    )

radio_indicator1 = dcc.RadioItems(
        id='indicator_radio',
        options=indicator_options,
        value='Happiness Score',
        labelStyle={'display': 'block'}
    )

radio_indicator2 = dcc.RadioItems(
        id='indicator_radio',
        options=indicator_options,
        value='Happiness Score',
        labelStyle={'display': 'block'}
    )

year_slider = dcc.RangeSlider(
        id='year_slider',
        min=2015,
        max=2019,
        value=[2015, 2019],
        marks={'2015': '2015',
               '2016': '2016',
               '2017': '2017',
               '2018': '2018',
               '2019': '2019'},
        step=1
    )

year_slider1 = dcc.RangeSlider(
        id='year_slider',
        min=2015,
        max=2019,
        value=[2015, 2019],
        marks={'2015': 'Year 2015',
               '2016': 'Year 2016',
               '2017': 'Year 2017',
               '2018': 'Year 2018',
               '2019': 'Year 2019'},
        step=1
    )

year_slider2 = dcc.RangeSlider(
        id='year_slider2',
        min=2015,
        max=2019,
        value=[2019, 2019],
        marks={'2015': '2015',
               '2016': '2016',
               '2017': '2017',
               '2018': '2018',
               '2019': '2019'},
        step=1
    )
#----------------Some styling preparation -------------------------------------------------------------------

tab_style = {
    'fontWeight': 'bold',
    "font-family": "Copperplate Gothic",
}

tab_selected_style = {
    'backgroundColor': '#0099cc',
    'borderTop': '2px solid steelblue',
    'borderBottom': '2px solid steelblue',
    'borderLeft': '2px solid steelblue',
    'borderRight': '2px solid steelblue',
    'color': 'white',
    "font-family": "Copperplate Gothic",
    'fontWeight': 'bold'
}

# --------------APP--------------------------------------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([html.Br(),html.Div([html.H2('How happy is your country?',
                                                   style={'textAlign': 'center'
                                                          }),
                                           html.P('The World Happiness Report is a landmark survey of the state of global happiness that ranks countries by how happy their citizens perceive themselves to be.',
                                                  style={'textAlign': 'center'
                                                         })],
                                style={"text-align": "center"}),
                       html.Br(),
                       dcc.Tabs(id='tabs', value='tab-1', children=[
                           dcc.Tab(label='Happiness around the World', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                           dcc.Tab(label='Happiness components', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                           dcc.Tab(label="Country comparison", value='tab-3', style=tab_style, selected_style=tab_selected_style),
                           dcc.Tab(label="Can money buy happiness?", value='tab-4', style=tab_style, selected_style=tab_selected_style)

                       ]),
                       html.Div(id='tabs_content'),

                       ], style={'backgroundColor': colors['background'], 'font-family': 'Copperplate Gothic', 'margin-bottom': '0px'}) 
  #-----------------------------------------------------------------------------------------------------------
 
#Callback for map

@app.callback(
    dash.dependencies.Output('happiness_map', 'figure'),
    [dash.dependencies.Input('year_slider2', 'value')]
)
def update_map(year):

    df_test = df_15_19_code[df_15_19_code['Year']==year[0]]

    fig = go.Figure(data=go.Choropleth(
        locations = df_test['Code'],
        z = df_test['Happiness Score'],
        text = df_test['Country'],
        colorscale = 'earth',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='black',
        marker_line_width=0.5,
        colorbar_ticksuffix = '',
        zmin=2,
        zmax=8,
        ))

    fig.update_layout(
        #title='World Happiness Map',
        font=dict(family='Arial', color='rgb(0,0,0)'),
        geo=dict(
            bgcolor='#C4E8FA',
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
            ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    return fig 
#Callback for top happy
@app.callback(
    dash.dependencies.Output('tableTop', 'figure'),
    [
     dash.dependencies.Input('year_slider2', 'value')]
)

def update_table2(year):

    df = df_1[(df_1['Year']==year[0])].iloc[:25,:].sort_values(by='Happiness Score')

    fig = px.bar(df, x='Happiness Score', y='Country', orientation='h')
    
    fig.update_traces(marker_color='#1E90FF')#lightblue

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )
    
    return fig        
  
#Callback for top sad      
@app.callback(
    dash.dependencies.Output('tableBottom', 'figure'),
    [
     dash.dependencies.Input('year_slider2', 'value')]
)

def update_table2(year):

    df = df_1[(df_1['Year']==year[0])].iloc[-25:,:].sort_values(by='Happiness Score', ascending=True)

    fig = px.bar(df, x='Happiness Score', y='Country', orientation='h')
    
    fig.update_traces(marker_color='#4682B4')#darkblue

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )
    
    return fig

#Add callback from comparison graph
@app.callback(
    dash.dependencies.Output('graph_example', 'figure'),
    [dash.dependencies.Input('country_drop', 'value'),
     dash.dependencies.Input('indicator_radio', 'value'),
     dash.dependencies.Input('year_slider', 'value')]
)
def update_graph_1(countries, indicator, year):
    filtered_by_year_df = df_1[(df_1['Year'] >= year[0]) & (df_1['Year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['Country'] == country]

        temp_data = dict(
            type='scatter',
            y=filtered_by_year_and_country_df[indicator],
            x=filtered_by_year_and_country_df['Year'],
            name=country
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Year'),
                          yaxis=dict(title=indicator)
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)
    
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    return fig        

#Callback for paralel graph
@app.callback(
    dash.dependencies.Output('paralel_graph', 'figure'),
    [dash.dependencies.Input('region_drop', 'value'),
     ]
)

def update_paralel(region):
    df = df_1[df_1['Year']==2019]
    df = df[df['Region'].isin(region)]
    #df = df[df['Country'].isin(countries)]

    group_vars = df['Region'].unique()
    dfg = pd.DataFrame({'Region':df['Region'].unique()})
    dfg['dummy'] = dfg.index
    df = pd.merge(df, dfg, on = 'Region', how='left')


    dimensions = list([dict(range=[0,df['dummy'].max()],
                       tickvals = dfg['dummy'], ticktext = dfg['Region'],
                       label='Region', values=df['dummy']),
                   dict(range=[df['Happiness Rank'].min(),df['Happiness Rank'].max()],
                        label='Happiness Rank', values=df['Happiness Rank']),
                   dict(range=[df['GDP per capita'].min(),df['GDP per capita'].max()],
                        label='GDP', values=df['GDP per capita']),
                  dict(range=[df['Social support'].min(),df['Social support'].max()],
                       label='Social support', values=df['Social support']),
                  dict(range=[df['Healthy life expectancy'].min(),df['Healthy life expectancy'].max()],
                       label='Healthy life', values=df['Healthy life expectancy']),
                  dict(range=[df['Freedom to make life choices'].min(),df['Freedom to make life choices'].max()],
                       label='Freedom', values=df['Freedom to make life choices']),
                  dict(range=[df['Generosity'].min(),df['Generosity'].max()],
                       label='Generosity', values=df['Generosity']),
                  dict(range=[df['Perceptions of corruption'].min(),df['Perceptions of corruption'].max()],
                       label='Corruption', values=df['Perceptions of corruption']),
                   
                  
                  
                  ])

    fig = go.Figure(data=go.Parcoords(line = dict(color = df['dummy'],
                   colorscale = 'Earth'), dimensions=dimensions,name='Country'))
    
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    return fig

#Callback for bubble graph
@app.callback(
    dash.dependencies.Output('bubble_graph', 'figure'),
    [dash.dependencies.Input('country_drop3', 'value'),
    ]
)
def update_bubble(countries):
    df = df_gdp[df_gdp['Country'].isin(countries)]
    
    fig = px.scatter(df, x="Logged GDP per capita", y="Happiness Score", color="Region",
           hover_name="Country")
    
    # linear regression
    regline = sm.OLS(df_gdp['Happiness Score'],sm.add_constant(df_gdp['Logged GDP per capita'])).fit().fittedvalues

    # add linear regression line for whole sample
    fig.add_traces(go.Scatter(x=df_gdp['Logged GDP per capita'], y=regline,
                          mode = 'lines',
                          line=dict(dash='dot'),
                          marker_color='darkblue',
                          name='Expected happiness for wealth level (linear)')
                          )
    
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    return fig
  #-----------------------------------------------------------------------------------------------------------
  # Callback to make use of the tabs component
@app.callback(Output('tabs_content', 'children'),
              [Input('tabs', 'value')])
def show_content(tab):
    """"This function receives as input the user's tab choice and shows the correspondent content."""
    if tab == 'tab-1':
        return html.Div([
            html.Div([
            html.Div([html.Br(), html.H3('What is happiness?'),
                                         html.Iframe(src='https://www.youtube.com/embed/6Pm0Mn0-jYU'),
                                         html.Br(),
                                         ],
                                        style={'padding-left': '10%','width': '40%'}, className='box'),
                
            html.Div([html.Br(),html.Br(), html.H4('5 definitions you must know!'),
                     html.P('1. Happiness is not something ready made. It comes from your own actions. – Dalai Lama'),
                     html.P('2. Happiness is when what you think, what you say, and what you do are in harmony. – Mahatma Gandhi'),
                     html.P('3. Happiness doesn’t depend on any external conditions, it is governed by our mental attitude. – Dale Carnegie'),
                     html.P('4. Happiness depends more on how life strikes you than on what happens. – Andy Rooney'),
                     html.P('5. Happiness is itself a kind of gratitude. – Joseph Wood Krutch'),
                     ],
                     style={'textAlign': 'left','padding-right': '10%','width': '60%'}, className='box'),
            
            ],
            style={'display': 'flex'}),
        
            html.Div([html.Br(), html.H3('World Happiness Map',
                              style={'textAlign': 'center',}),
                      html.P('Select a year and see wich country would you move to!',
                             style={'textAlign': 'center'}),
                      year_slider2,
                      dcc.Graph(id='happiness_map')], 
                                 style={'padding-left': '15%', 'padding-right': '15%','width': '70%'}, className='box'),
            
            html.Div([
                html.Div([
                    html.H3('Happiest countries in the world',
                            style={'textAlign': 'center',
                                   'backgroundColor': colors['background'],
                                   'color': colors['text']
                                   }),
                    dcc.Graph(id='tableTop'),
                    ], 
            style={'padding-left': '10%','width': '40%'}, className='box'),
        
            html.Div([
                    html.H3('Least happy countries in the world',
                            style={'textAlign': 'center',
                                   'backgroundColor': colors['background'],
                                   'color': colors['text']
                                   }),
                    dcc.Graph(id='tableBottom'),
                    ], style={'padding-right': '10%','width': '40%'}, className='box'),
                ],
            style={'display': 'flex'}),
            
            html.Div(html.Img(src=app.get_asset_url('whr-logo.png'), style={'height': '10%', 'width': '10%'}))
            ])

    elif tab == 'tab-2':
        return html.Div([html.Br(),
            html.Div([html.H3('Happiness Components:',
                              style={'padding-left': '5%'}),
                html.Div([html.Br(),
                          html.P('1. GDP - value of happiness explained by GDP per capita of the country'),
                          html.P('2. Social Support - value of happiness explained by social support received from the country'),
                          html.P('3. Healthy Life - value of happiness explained by quality of life within the country'),
                          html.P('4. Freedom - value of happiness explained by perceived freedom to make own choices within country'),
                          html.P('5. Generosity - value of happiness explained by perceived generosity among country fellows'),
                          html.P('6. Corruption - value of happiness explained by perception corruption within the country'),
                ], style={'textAlign': 'left',
                          'backgroundColor': 'lightblue',
                          'borderTop': '2px solid steelblue',
                          'borderBottom': '2px solid steelblue',
                          'borderLeft': '2px solid steelblue',
                          'borderRight': '2px solid steelblue',
                          "font-family": "Copperplate Gothic",
                          'padding-up': '5%',
                          'padding-left': '5%'
                          }, className='box')
                
            ], style={'padding-up': '5%', 'padding-left': '5%', 'width': '65%'}),
            
            html.Div([
                html.Div([html.Br(),
                    html.P('Here you may explore the differences and understand how people perceive the components across regions.'),
                    dcc.Graph(id='paralel_graph'),
                    ], style={'padding-left': '5%', 'width': '80%'}, className='box'),
        
                html.Div([
                    html.H3('Select regions:'),
                    dropdown_region,
            
                    html.Br(),
                    ], style={'padding-left': '1%', 'padding-right': '5%','width': '18%', 'background-color': colors['background']}, className=''),

            ], style={'padding-right': '5%','display': 'flex'})
        ])


    elif tab == 'tab-3':
        return html.Div([
            html.Div([html.H3('Select countries to compare:'),
                      dropdown_country,
                      html.Br(),
                      html.H3('Select your indicator:'),
                      radio_indicator2], 
                     style={'padding-left': '10%', 'padding-right': '5%','width': '30%', 'background-color': colors['background']}, className=''),

            html.Div([html.Br(),
                    html.P('Feel free to compare countries across happiness scores and components.'),
                    html.P('You may compare more than 2 countries at once and explore the evolution by year!'),
                    dcc.Graph(id='graph_example'),
                      year_slider],
                     style={'width': '70%'}, className='box')], 
            
            style={'padding-right': '10%','display': 'flex'})
    
    elif tab == 'tab-4':
        return html.Div([
            html.Div([
                    html.H3('Select countries:'),
                      dropdown_country3,
                      html.Br(),
                      ],
                     style={'padding-left': '10%', 'padding-right': '5%','width': '30%', 'background-color': colors['background']}, className=''),

            html.Div([html.Br(),
                    html.P('There is a well known saying that states that money cannot buy happiness. Do you agree? Explore for each country and region if this is actually true or just a fairy tail invented from rich people to keep poor people in line!'),
                    html.P('Hint: Are South American people happier with less? Explore and find the answer to this question!'),
                    dcc.Graph(id='bubble_graph')
                      ],
                     style={'width': '70%'}, className='box')], 
            
            style={'padding-right': '10%','display': 'flex'})
    
app.title = "World Happiness"

if __name__ == '__main__':
    app.run_server(debug=True)
