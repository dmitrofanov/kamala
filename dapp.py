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
        # Dissalow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-upload-data'),
])


def parse(file):
    data = pd.read_csv(file, sep=';', encoding='cp1251')

    lis = data.astype(str).values.tolist()

    target = []
    for rows in lis:
        date = rows[1]
        services = re.findall(r'([^;]+?, \d+,)', rows[3])
        l = map(lambda x: x.rstrip(',').strip(), services)
        for x in l:
            rvs = x[::-1]
            i = rvs.find(',')
            t1 = x[:-i - 1].strip()
            t2 = x[-i:].strip()
            target.append([date, t1, int(t2)])
    df = pd.DataFrame(target, columns=['day', 'service', 'count'])
    #df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d').dt.floor('d')
    df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d').dt.floor('d')
    #df.day = pd.DatetimeIndex(df.day).strftime("%Y-%m-%d")
    return df


def service_score():
    df = pd.read_csv(
        filepath_or_buffer='service_score.csv',
        encoding='cp1251',
        names=[
            'service',
            'score'
        ]
    )
    return df


def score_bonus():
    df = pd.read_csv(
        filepath_or_buffer='score_bonus.csv',
        encoding='cp1251',
        names=[
            'score',
            'bonus'
        ]
    )
    return df


def t(title, df):
    tab = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        export_format='csv'
    )
    return html.Div([html.H3(title), tab])


def groupby_sum(df, columns):
    return df.groupby(columns).sum().reset_index()


def render(df):
    ra = df
    se = service_score()
    sc = score_bonus()

    gr = groupby_sum(
        ra,
        [
            pd.Grouper(
                key="day",
                freq='D'
            ),
            'service',
        ])

    #ct = pd.concat([gr, se], keys='service,score')
    ct = pd.merge(gr, se, how='left', on='service')

    ct['temp_score'] = ct['count'] * ct['score']

    dt = ct.groupby('day').agg({'temp_score': ['sum']})
    dt.columns = ['sum_temp_score']
    dt = dt.reset_index()

    dt = pd.merge(dt, sc, how='left',
                  left_on='sum_temp_score', right_on='score')

    total = dt.bonus.sum()

    result = html.Div([
        html.H2(f'Total bonus: {total}'),
        t(
            title='ref score bonus',
            df=sc
        ),
        t(
            title='ref service score',
            df=se
        ),
        t(
            title='day view',
            df=dt
        ),
        t(
            title='concated',
            df=ct
        ),
        t(
            title='grouped',
            df=gr
        ),
        t(
            title='raw',
            df=ra
        ),
    ])

    return result


@ app.callback(Output('output-upload-data', 'children'),
               [Input('upload-data', 'contents'), Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents:
        decoded = base64.b64decode(contents).decode('cp1251')
        df = parse(io.StringIO(decoded))
        return render(df)


#if __name__ == '__main__':
#    app.run_server(debug=True)
