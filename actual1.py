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
from bokeh.models.widgets import Button, PasswordInput, Paragraph
from bokeh.layouts import column, row
from bokeh.transform import cumsum


def updateGraphBarChart(count, label,title):
    """
    Updates the page with a new vertical bar chart.
    count gives the data for the column heights and label gives the label at the bottom.
    Title gives the title of the graph
    """
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
    """
    Updates the page with a new pie chart.
    count gives the data for the column heights and label gives the label at the bottom.
    Title gives the title of the graph.
    Method is taken from the official bokeh documentation https://docs.bokeh.org/en/latest/docs/gallery/pie_chart.html
    """
    x=0
    y=1
    radius=0.7

    d = {}

    for i in range(len(count)):
        d[label[i]] = count[i]

    print(d,len(d))
    i = 0
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
    """
    Gets the amount of commits per person for a given repo
    """
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
    """
    Gets the amount of forks per month for a given repo
    """
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
    """
    Gets the percentage of languages for a given repo
    """
    repo = gh.get_repo(repo)
    langs = repo.get_languages()

    counts = []
    lang = []

    for i,j in langs.items():
        counts.append(j)
        lang.append(i)

    updateGraphBarChart(counts,lang,"Lines of Code per Language")

def CvOIssues(repo):
    """
    Gets the amount of open and closed issues of a given repo
    """
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
    """
    stops the server
    """
    sys.exit()

def handler(event):
    """
    handles the events on the dropdown button
    """
    if event.item=="Commits":
        commitsPerPerson(text.value)
    elif event.item=="Forks":
        forksPerMonth(text.value)
    elif event.item=="LOCLangs":
        percentageLanguages(text.value)
    elif event.item=="Issues":
        CvOIssues(text.value)

token = ""
tokenNotFound = False
try:
    token = open("token.txt","r").read()
except:
    tokenNotFound = True
    
gh = Github(token)

badToken = False
try:
    gh.get_user("torvalds")
except:
    badToken = True

if(tokenNotFound):
    p = Paragraph(text="""Token wasn't found. Please put in a valid Github API token into a file called token.txt.""",
width=200, height=100)
    curdoc().add_root(p)
elif(badToken):
    p = Paragraph(text="""Token in token.txt is invalid or bad in some way. Please put a valid Githib API token into the file.""",
width=200, height=100)
    curdoc().add_root(p)
else:
    text = TextInput(value="", title="enter repo")

    stopbutton = Button(label="shut down", button_type="danger")
    stopbutton.on_click(stop)

    menu = [("Commits per Person", "Commits"), ("Forks per Month", "Forks"),
        ("Lines of Code per Language","LOCLangs"),("Closed vs Open Issues","Issues")]
    dropdown = Dropdown(label="Graph type", button_type="default", menu=menu)

    dropdown.on_click(handler)

    buttonRow = row(dropdown,stopbutton)

    layout = column(text, buttonRow)

    curdoc().add_root(layout)

if __name__ == "__main__":
    #os.system("start http://localhost:5006/actual1")
    os.system("bokeh serve actual1.py --o")