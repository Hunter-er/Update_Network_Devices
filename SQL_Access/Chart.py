# Creates the plots based on selected criteria
def Create_Plot(ChartData, Taglist, CombinedChart, SeperatedChart):
    import plotly.graph_objects as plot
    from plotly.subplots import make_subplots as sub

    ChartTitle = "SQL Chart Plot"
    XaxisTitle = "Time"
    YaxisTitle = "Values"

    ##########################
    # Combined chart
    if CombinedChart is True:
        tagcount = 0
        figure = plot.Figure()
        while tagcount < len(Taglist):
            figure.add_trace(plot.Scatter(x=ChartData[0][tagcount], y=ChartData[1][tagcount], mode='lines',
                                           line={"shape":'hv'}, name=Taglist[tagcount]))
            tagcount = tagcount + 1

        figure.update_layout(
            title=ChartTitle,
            xaxis_title=XaxisTitle,
            yaxis_title=YaxisTitle
            )

        figure.show()

    ############################
    # Seperated charts
    if SeperatedChart is True:
        tagcount = 0
        figure2 = sub(rows=len(Taglist), cols=1)
        while tagcount < len(Taglist):
            figure2.add_trace(plot.Scatter(x=ChartData[0][tagcount], y=ChartData[1][tagcount], mode='lines',
                                            line={"shape":'hv'}, name=Taglist[tagcount]), row=tagcount+1, col=1)
            tagcount = tagcount + 1

        figure2.update_layout(
            title=ChartTitle,
            xaxis_title=XaxisTitle,
            yaxis_title=YaxisTitle
        )
        figure2.show()

    ################################


# Exports data to CSV file, build title then start appending data
def Export_to_CSV(Data, Tags, FileName):
    import csv

    TitleBar = ['TagName', 'Time', 'Value']
    tag = 0
    item = 0

    with open(FileName, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(TitleBar)

    with open(FileName, mode='a', newline='') as file:
        writer = csv.writer(file)

        while tag < len(Tags):
            item = 0
            while item < len(Data[0][tag]):

                Time = Data[0][tag][item]
                Value = Data[1][tag][item]
                TagName = Tags[tag]

                newrow = [TagName, Time, Value]
                writer.writerow(newrow)

                item = item + 1

            tag = tag + 1
