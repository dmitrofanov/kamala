import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import re
import pandas as pd

import time

import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]), style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-upload-data'),
])


def to_dataframe(file):
    data = pd.read_csv(file, sep=';', encoding='cp1251')

    lis = data.astype(str).values.tolist()

    target = []
    for rows in lis:
        date = rows[1]
        # if date:
        # date = datetime.datetime.strptime(rows[1], '%Y-%m-%d %H:%M:%S')
        services = re.findall(r'([^;]+?, \d+,)', rows[3])
        l = map(lambda x: x.rstrip(',').strip(), services)
        for x in l:
            rvs = x[::-1]
            i = rvs.find(',')
            t1 = x[:-i - 1].strip()
            t2 = x[-i:].strip()
            target.append([date, t1, int(t2)])
    df = pd.DataFrame(target, columns=['DateTime', 'ServiceName', 'Count'])
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
    return df


def to_dash_table(df):
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns]
    )


def editable_dash_table(df):
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        editable=True,
    )


def groupby_sum(df, columns):
    return df.groupby(columns).sum().reset_index()


def render_page(df):
    raw_df = df
    grouped = groupby_sum(
        df, [pd.Grouper(key="DateTime", freq='D'), 'ServiceName'])
    services = pd.unique(df['ServiceName'])
    services = pd.DataFrame(data=services, columns=['ServiceName'])
    return html.Div([
        html.H3('Points per service'),
        editable_dash_table(services),
        html.H3('Grouped by service'),
        to_dash_table(grouped),
        html.H3('Raw Parsed Data'),
        to_dash_table(raw_df),
    ])
# editable=True


@ app.callback(Output('output-upload-data', 'children'),
               [Input('upload-data', 'contents'), Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents:
        decoded = base64.b64decode(contents).decode('cp1251')
        df = to_dataframe(io.StringIO(decoded))
        return render_page(df)


if __name__ == '__main__':
    app.run_server(debug=True)

"""
with open('result20200912110233.csv', 'rb') as f:
    ftext = f.read()
    result = base64.b64encode(ftext)
    decoded = base64.b64decode(result)
    df = pd.read_csv(io.StringIO(decoded.decode('cp1251')))
    dt = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns]
    )
"""
