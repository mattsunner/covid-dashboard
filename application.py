import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import sqlite3


app = dash.Dash(__name__)

conn = sqlite3.connect('./data/output_data/covidDB.db')
federal_df = pd.read_sql("SELECT * FROM federaldata", conn)
state_df = pd.read_sql("SELECT * FROM statedata", conn)

# Federal Level Analysis
fig_1 = px.scatter(x=federal_df['date'], y=federal_df['positive'], title='Running Total of Positive Cases in the United States (U.S.) by Date', labels={
                   'x': 'Date', 'y': 'Number of Positive Cases (M)'})

fig_2 = px.scatter(x=federal_df['date'], y=federal_df['totalTestResultsIncrease'], title='Total Increase in Daily Testing for COVID-19 (U.S.)',
                   labels={'x': 'Date', 'y': 'Number of Tests Completed'})

fig_3 = px.line(federal_df, x='date', y=['death', 'totalTestResultsIncrease', 'positive'],
                title="COVID-19 Deaths Compared to Tests Administered - Baseline Values (Single-Axis)")

# State Level Analysis
fig_4 = px.scatter(x=state_df['date'], y=state_df['positive'], color=state_df['state'], title='Overall Positive Cases by State in the United States (U.S.) by Date',
                   labels={'x': 'Date', 'y': 'Number of Positive Cases (M)'})

app.layout = html.Div(children=[
    html.H1(children="COVID-19 Case Analysis"),

    dcc.Graph(
        id='fig_1',
        figure=fig_1
    ),

    dcc.Graph(
        id='fig_2',
        figure=fig_2
    ),

    dcc.Graph(
        id='fig_3',
        figure=fig_3
    ),

    dcc.Graph(
        id='fig_4',
        figure=fig_4
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True)
