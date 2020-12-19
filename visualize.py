#!/usr/bin/python3

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import math
import dash
import dash_core_components as dcc
import dash_html_components as html


def genDateRange():
    import datetime
    start_date = datetime.date(2014,8,1)
    end_date = datetime.date(2020,12,1)
    date_range = pd.date_range(start_date, end_date)
    date_range = date_range[date_range.day==1]
    return date_range

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

final = {}
with open('testMaterial.txt', 'r') as d:
    amount = d.readlines()
    d.close()
    for line in amount:
        index = line.find("=")
        name = line[:index]
        history = line[index+2:-2].split(",")
        history = [float(h) for h in history]
        # [round(math.log(10, int(h)),2) for h in history]
        final[name] = history


# number of recorded months
xlen = (2019-2014+1)*12 + 8
# number of factors
ynum = 5

import plotly.express as px
phaseX = ["G/F", "1/F", "2/F", "3/F", "4/F", "5/F","RF"]
ptCost = [1,2,3,4,5,6,7]
tcostFig = px.bar(x=phaseX,y=ptCost, labels={'x':'Floor', 'y':'Total Cost'})
tcostFig.update_layout(title_text="Total Cost by Floor")


### phase cost ###

## figure set ##
rnum = 4
cnum = 1

# comsuption of each material
com = {
    "AGG": 1252,
    "CEMENT": 461,
    "SAND": 512,
    "WATER": 175/1000
}

### material price ###
fig = make_subplots(rows=rnum, cols=cnum, shared_xaxes=False, shared_yaxes=False)

for i, (k, v) in enumerate(final.items()):
    nrow = i//cnum + 1
    ncol = i%cnum + 1

    subfig = go.Scatter(x=genDateRange(),y=v,name=k)
    fig.add_trace(
        subfig,
        row=nrow,col=ncol
    )
    fig.update_yaxes(
        type="linear",
        row=nrow,
        col=ncol)

fig.update_layout(title="Material Price")
# fig.show()

### material cost ###
costFig = make_subplots(rows=nrow, cols=ncol, shared_xaxes=False, shared_yaxes=False)

for i, (k, v) in enumerate(final.items()):
    nrow = i//cnum + 1
    ncol = i%cnum + 1

    # compute comsumed price
    name = k.split("_")[1]
    if name in com:
        v = [com[name]*d*5.92 for d in v]
    else:
        continue
    
    subfig = go.Scattergl(x=genDateRange(),y=v,name=k)
    costFig.add_trace(
        subfig,
        row=nrow,col=ncol
    )
    costFig.update_yaxes(
        type="linear",
        row=nrow,
        col=ncol)

costFig.update_layout(title="Material Total Cost")

## do NOT modify the following code
app.layout = html.Div(children=[
    html.H1(children='Integrated Building Information Management'),

    html.Div(children='''
        BIMcost: A dashboard for realtime and interative cost monitoring.
    '''),

    dcc.Graph(
        id='phase-cost',
        figure=tcostFig
    ),

    dcc.Graph(
        id='material-price',
        figure=costFig
    ),

    #  dcc.Graph(
    #     id='material-cost',
    #     figure=fig
    # )
])


if __name__ == '__main__':
    app.run_server(debug=True)