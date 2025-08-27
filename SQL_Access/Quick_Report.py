import SQL_connect
import Format
import Chart
import datetime as datetime


# EndTime = YYYYMMDD hh:mm:ss.000 SQL Datetime format                     End time of range
# EndTime = "GetDate()"
EndTime = "'20240217 07:00:00.000'"
# TimeRangeMin = Negative value since based on end time                 Time in minutes
TimeRangeMin = '-30'
# Taglist = ('Tag1', 'Tag2', 'Tag3')                                    SQL Tag format string
Taglist = "('Utility_Main_Current_Iavg', 'ASRS2_Current_Iavg', 'TC3.PAS.PAS_ZSE4803_EXT_POS')"
# Create single chart
CreateSingleChart = True
# Create stacked chart
CreateStackedChart = True
# Create CSV export
ExportData = True


def Quick_Report_Run(TimeRangeMin, EndTime, Tagstring, CreateSingleChart, CreateStackedChart, ExportData):
    # Generates SQL command
    SQLCommand = SQL_connect.HistTagPull(TimeRangeMin, EndTime, Tagstring)

    # Connects to historian server and runs SQL command
    SQLData = SQL_connect.HistConnect(SQLCommand)

    # Format Tag List for Chart
    Taglist = Format_TagList(Tagstring)

    # Format Data for Chart
    ChartData = Format.Plot_Data(SQLData, Taglist)

    # Create charts if needed
    if (CreateStackedChart or CreateSingleChart):
        Chart.Create_Plot(ChartData=ChartData, Taglist=Taglist, CombinedChart=CreateSingleChart,
                        SeperatedChart=CreateStackedChart)
    # Create csv if needed
    if ExportData:
        FileName = ('NewReport' + '.csv')
        Chart.Export_to_CSV(Data=ChartData, Tags=Taglist, FileName=FileName)


def Format_TagList(Tags):
    ListofTags = []
    tagstart = 0
    tagend = 0
    charcount = 0

    # Taglist = ('Tag1', 'Tag2', 'Tag3')
    for character in Tags:
        # print(character)
        if character == "'" and tagstart == 0:
            tagstart = charcount
        elif character == "'" and tagstart != 0 and tagend == 0:
            tagend = charcount
            ListofTags.append(Tags[tagstart + 1: tagend])
            tagstart = 0
            tagend = 0

        charcount = charcount + 1

    return ListofTags


Quick_Report_Run(TimeRangeMin, EndTime, Taglist, CreateSingleChart, CreateStackedChart, ExportData)
