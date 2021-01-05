from github import Github

import math
from math import pi
import os
import sys

import pandas as pd

import bokeh
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import CustomJS, TextInput, ColumnDataSource, FixedTicker, LabelSet, Dropdown
from bokeh.models.widgets import Button
from bokeh.layouts import column, row
from bokeh.transform import cumsum


def updateGraphBarChart(count, label,title):
    source = ColumnDataSource(data=dict(label=label, count=count))

    plot = figure(title=title, x_range=label,
                  x_axis_label='', y_axis_label='', toolbar_location=None, tools="hover", tooltips="@label @count")

    plot.vbar(x='label', width=0.5, top='count',
              color="firebrick", source=source)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0
    nlayout = column(text, buttonRow, plot)
    layout.children = nlayout.children

def updateGraphPieChart(count,label,title):
    x=0
    y=1
    radius=0.7

    d = {}

    for i in range(len(count)):
        d[label[i]] = count[i]

    print(d,len(d))

    data = pd.Series(d).reset_index(name='value').rename(columns={'index':'state'})

    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = ["firebrick","blue"]
    
    plot = figure(title=title, x_range=(-1,1),
                  x_axis_label='', y_axis_label='', toolbar_location=None, 
                  tools="hover", tooltips="@state @value")
    
    plot.wedge(x=x, y=x, radius=radius,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white",source=data,fill_color='color')
    
    plot.axis.axis_label=None
    plot.axis.visible=False
    plot.grid.grid_line_color = None

    nlayout = column(text, buttonRow, plot)
    layout.children = nlayout.children


def commitsPerPerson(repo):
    repo = gh.get_repo(repo)
    contributors = repo.get_contributors()
    commitCounts = []
    for contrib in contributors:
        commitCounts.append(
            (repo.get_commits(author=contrib).totalCount, contrib.id))

    counts = []
    IDs = []

    for count, contribID in commitCounts:
        counts.append(count)
        contribName = [x for x in contributors if contribID == x.id]
        IDs.append(contribName[0].login)

    updateGraphBarChart(counts, IDs,"Commits per Person")

def forksPerMonth(repo):
    repo = gh.get_repo(repo)
    forks = repo.get_forks()

    forkCount = [0,0,0,0,0,0,0,0,0,0,0,0]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for fork in forks:
        try:
            forkCount[fork.created_at.month-1]+=1
        except:
            pass
    updateGraphBarChart(forkCount,months,"Forks per Month")

def percentageLanguages(repo):
    repo = gh.get_repo(repo)
    langs = repo.get_languages()

    counts = []
    lang = []

    for i,j in langs.items():
        counts.append(j)
        lang.append(i)

    updateGraphBarChart(counts,lang,"Lines of Code per Language")

def CvOIssues(repo):
    repo = gh.get_repo(repo)
    issues = repo.get_issues(state="all")

    openClosed = [0,0]
    OC = ["Open","Closed"]

    for issue in issues:
        state = issue.state
        if state=="open":
            openClosed[0]+=1
        elif state=="closed":
            openClosed[1]+=1
    
    updateGraphPieChart(openClosed,OC,"Open vs Closed Issues")


def stop():
    sys.exit()



token = os.getenv('GITHUB_TOKEN')
gh = Github(token)

text = TextInput(value="", title="enter repo")

stopbutton = Button(label="shut down", button_type="danger")
stopbutton.on_click(stop)

menu = [("Commits per Person", "Commits"), ("Forks per Month", "Forks"),
        ("Lines of Code per Language","LOCLangs"),("Closed vs Open Issues","Issues")]
dropdown = Dropdown(label="Graph type", button_type="default", menu=menu)

def handler(event):
    if event.item=="Commits":
        commitsPerPerson(text.value)
    elif event.item=="Forks":
        forksPerMonth(text.value)
    elif event.item=="LOCLangs":
        percentageLanguages(text.value)
    elif event.item=="Issues":
        CvOIssues(text.value)

dropdown.on_click(handler)

buttonRow = row(dropdown,stopbutton)

layout = column(text, buttonRow)
curdoc().add_root(layout)

if __name__ == "__main__":
    #os.system("start http://localhost:5006/actual1")
    os.system("bokeh serve actual1.py")