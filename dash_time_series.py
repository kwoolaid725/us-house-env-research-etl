from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# import excel file
df = pd.read_excel('HouseData-All.xlsx', sheet_name='Combined')
df['Floor_Type'] = df['Floor_Type'].str.capitalize()
df['Built Year'] = df.groupby('ZPID')['Built Year'].ffill()
df['Built Year'] = df['Built Year'].astype(int)

# '*' values in the 'Floor_Type' column are replaced with blank
df['Floor_Type'] = df['Floor_Type'].replace('*', None)
df['Count'] = 1
df = df.dropna(subset=['Floor_Type'])
df['Room'] = df['Room'].replace(r'^Bed.*', 'Bedroom', regex=True)

df_bedroom = df[df['Room'] == 'Bedroom']
df_bedroom = df_bedroom.groupby(['State', 'Home_Type', 'Home_Price', 'Sq_ft', 'Built Year', 'Floor_Type'])[
    'Count'].sum().reset_index()

df_bedroom = df_bedroom.pivot_table(index=['State', 'Home_Type', 'Home_Price', 'Sq_ft', 'Built Year'],
                                    columns='Floor_Type', values='Count').reset_index()
df_bedroom = df_bedroom.fillna(0)

df_bedroom = df_bedroom.groupby(['State', 'Built Year'])[['Bare', 'Carpet', 'Rug']].sum().reset_index()

df_bedroom['Bare%'] = (
            df_bedroom['Bare'] / (df_bedroom['Bare'] + df_bedroom['Carpet'] + df_bedroom['Rug']) * 100).round(1)
df_bedroom['Carpet%'] = (
            df_bedroom['Carpet'] / (df_bedroom['Bare'] + df_bedroom['Carpet'] + df_bedroom['Rug']) * 100).round(1)
df_bedroom['Rug%'] = (df_bedroom['Rug'] / (df_bedroom['Bare'] + df_bedroom['Carpet'] + df_bedroom['Rug']) * 100).round(
    1)

app.layout = html.Div([
    html.H4('Carpet % analysis'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select state:"),
    dcc.Dropdown(
        id="State",
        options=['NY', 'IL', 'CA', 'TX', 'FL', 'WA'],
        value="NY",
        clearable=False,
    )

])


@app.callback(
    Output("time-series-chart", "figure"),
    Input("State", "value"))
def display_time_series(state):
    filtered_df = df_bedroom[df_bedroom['State'] == state]
    fig = px.scatter(filtered_df, x='Built Year', y='Carpet%')
    return fig


app.run_server(debug=True)