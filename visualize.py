#!/usr/bin/python3

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

### predicted unit price ###
predict = dict()
price = {
    "agg": [],
    "sr": [],
    "cement": [],
    "sand": [],
    "glass": [],
    "salary": [],
    "water": []
}

with open('materialPredict.txt', 'r') as d:
    amount = d.readlines()
    d.close()
    for line in amount:
        index = line.find("=")
        name = line[:index]
        history = line[index+2:-2].split(",")
        new = []
        key = name.split("_")[1].lower()
        for i, h in enumerate(history):
            m = 0
            try:
                m = int(h)
            except ValueError:
                m = round(float(h),2)
            finally:
                if i % 3 == 0:
                    # print(key)
                    # print(price[key])
                    price[key].append(m)
                new.append(m)
        predict[name] = new


### generate x axis ###
def genDateRange():
    import datetime
    start_date = datetime.date(2014,8,1)
    end_date = datetime.date(2020,12,1)
    date_range = pd.date_range(start_date, end_date)
    date_range = date_range[date_range.day==1]
    return date_range

def genPredictDateRange():
    import datetime
    start_date = datetime.date(2021,1,1)
    end_date = datetime.date(2022,12,1)
    date_range = pd.date_range(start_date, end_date)
    date_range = date_range[date_range.day==1]
    return date_range

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# number of recorded months
xlen = (2019-2014+1)*12 + 8
# number of factors
ynum = 5

### phase cost ###
phaseMaterial = {
    "G/F": {
        "CONCRETE": 957.38,
        "GLASS": 329.0,
    },
    "1/F": {
        "CONCRETE": 392.37,
        "GLASS": 1053.0
    }, 
    "2/F": {
        "CONCRETE": 370.8,
        "GLASS": 470.0
    }, 
    "3/F": {
        "CONCRETE": 349.17,
        "GLASS": 455.0
    }, 
    "4/F": {
        "CONCRETE": 363.39,
        "GLASS": 469.0
    }, 
    "5/F": {
        "CONCRETE": 347.27,
        "GLASS": 443.0
    },
    "RF": {
        "CONCRETE": 344.86,
        "GLASS": 10.0
    }
}

## figure set ##
rnum = 7
cnum = 1

# density of each material
com = {
    "AGG": 1252/1000,
    # 0.025 * 8000
    "SR": 200, 
    "CEMENT": 461/1000,
    "SAND": 512/1000,
    "WATER": 175/1000,
    "GLASS": 1,
    "SALARY": 300
}

import plotly.express as px
phaseX = ["G/F", "1/F", "2/F", "3/F", "4/F", "5/F","RF", "Curtain Wall"]
ptCost = []

glass = 0
labor = 0
for i, k in enumerate(phaseX[:-1]):
    vol = phaseMaterial[k]
    conVol = vol["CONCRETE"]
    glassVol = vol["GLASS"]
    conTotal = conVol * \
        ( 1 * 
        ( com["AGG"]*price["agg"][i] \
            + com["CEMENT"]*price["cement"][i] \
            + com["SAND"]*price["sand"][i] \
            + com["WATER"]*7.11 
        ) \
        + price["sr"][i] )
    if i == 0:
        labor = com["SALARY"] * price["salary"][i]
    floorCost = labor + conTotal
    ptCost.append(floorCost)
    glass = glass + 300 + glassVol * 1 * ( price["glass"][-1]*5)

finalPhase = glass + labor
ptCost.append(finalPhase)

tcostFig = px.bar(x=phaseX,y=ptCost,labels={'x':'Floor', 'y':'Total Cost'})
tcostFig.update_layout(title_text="Predcited Total Cost by Floor (3 months)")


### predicted total cost ###
preFig = make_subplots(rows=rnum, cols=cnum, shared_xaxes=False, shared_yaxes=False)

for i, (k, v) in enumerate(predict.items()):
    nrow = i + 1 
    ncol = 1
    
    subfig = go.Scattergl(x=genPredictDateRange(),y=v,name=k)
    preFig.add_trace(
        subfig,
        row=nrow,col=ncol
    )
    preFig.update_yaxes(
        type="linear",
        row=nrow,
        col=ncol)

preFig.update_layout(title="Predicted Material Cost",height=600)


### material ###
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

### material cost predcited ###
costFig = make_subplots(rows=rnum, cols=ncol, shared_xaxes=False, shared_yaxes=False)

for i, (k, v) in enumerate(final.items()):
    nrow = i+1
    ncol = 1

    # compute comsumed price
    name = k.split("_")[1]
    if k == "SALARY" or k == "GLASS":
        continue
    if name not in com:
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

costFig.update_layout(title="Volume Concrete Price",height=600)


### material price history ###
fig = make_subplots(rows=rnum, cols=cnum, shared_xaxes=False, shared_yaxes=False)

for i, (k, v) in enumerate(final.items()):
    nrow = i+1
    ncol = 1

    subfig = go.Scatter(x=genDateRange(),y=v,name=k)
    fig.add_trace(
        subfig,
        row=nrow,col=ncol
    )
    fig.update_yaxes(
        type="linear",
        row=nrow,
        col=ncol)

fig.update_layout(title="Volume Concrete Price Hisotry",height=600)


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
        id='predict-cost',
        figure=preFig
    ),

    # dcc.Graph(
    #     id='material-price',
    #     figure=costFig
    # ),

     dcc.Graph(
        id='material-cost',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)