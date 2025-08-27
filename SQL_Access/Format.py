# File formats data to send to SQL
import main


# Takes Python date and converts to SQL
# YYYY-MM-DD HH:MI:SS SQL Datetime format
def SQL_Date(PyTime):
    from datetime import datetime

    if PyTime == 'now': return 'GetDate()'

    day = '%02d' % PyTime.day
    month = '%02d' % PyTime.month
    year = '%04d' % PyTime.year
    hour = '%02d' % PyTime.hour
    minute = '%02d' % PyTime.minute
    second = '%02d' % PyTime.second
    microsecond = '000'

    SQLTime = "'%s%s%s %s:%s:%s.%s'" % (year, month, day, hour, minute, second, microsecond)

    return SQLTime


# Takes list of tags and converts to SQL .TagName format
# ('Tag1', 'Tag2', 'Tag3') SQL Tag format
def SQL_Tag(TagList):
    FirstTag = True
    SQLTagName = "("

    for tag in TagList:

        # Used to add commas for multiple tags be
        if FirstTag is not True:
            SQLTagName = SQLTagName + ", "
        else: FirstTag = False

        SQLTagName = SQLTagName + "'" + tag + "'"

    SQLTagName = SQLTagName + ")"

    return SQLTagName


# Determine SQL String type and call function to build it
def SQL_Command(Purpose):
    import main
    import SQL_connect

    if Purpose == "HistTagPull":
        SQLCommand = SQL_connect.HistTagPull(TagName=main.TagName, StartTime=main.StartTime,
                                              TimeGapMinutes=main.TimeGapMinutes)
    elif Purpose == "HistTagList":
        SQLCommand = SQL_connect.HistTagList(TagSearchCriteria=main.TagSearchCriteria,
                                              DescSearchCriteria=main.DescSearchCriteria)
    else:
        return ""

    return SQLCommand


# Format SQL data for chart to use
def Plot_Data(SQLData, Taglist):
    Time_Tag = [[]]
    Value_Tag = [[]]

    # Create list of lists to add data for x/y axis
    while len(Taglist) > len(Time_Tag):
        Value_Tag.append([])
        Time_Tag.append([])

    # loop through SQL Data by row, the loop through Tagnames to get data to correct list within time and value lists
    # SQL data reports in order chronologically, not Tagname based
    for row in SQLData:
        tag = 0
        while tag < len(Taglist):
            if row['TagName'] == Taglist[tag]:
                Time_Tag[tag].append(row['DateTime'])
                Value_Tag[tag].append(row['Value'])
                tag = tag + len(Taglist)
            tag = tag + 1

    return Time_Tag, Value_Tag


# Convert Dictionary to List
def Tag_Dict_to_List(Dict):
    List = []
    for key in Dict:
        name_desc_string =  key['TagName'] + " | " + key['Description']
        List.append(name_desc_string)

    return List


# Remove description from Select List by searching for " |"
def Remove_Desc_Selected_List(List):
    TagList = []
    for item in List:
        index = item.index('|')
        TagList.append(item[:index - 1])

    return TagList


# Convert time chosen to SQL time
def Update_TimeFrame(sday,smonth,syear,shour,smin,ssec,eday,emonth,eyear,ehour,emin,esec,gapday,gaphour,gapmin):
    from datetime import datetime, timedelta

    # Calculation if given start time
    if sday and smonth and syear:
        dt_start = InputTime_to_DateTime(sday, smonth, syear, shour, smin, ssec)

        # Calculation if given start time and end time
        if eday and emonth and eyear:
            # Calculate gap between two dates
            dt_end = InputTime_to_DateTime(eday, emonth, eyear, ehour, emin, esec)
            gap = dt_end - dt_start
            gapday = gap.days
            gapsec = gap.seconds
            gaphour = int(gapsec / 3600)
            gapmin = int((gapsec - (gaphour * 3600)) / 60)
            mingap = Calc_Gap_Min(gapday,gaphour,gapmin)
            main.Time = dt_end
            main.TimeGapMinutes = abs(mingap) * -1

        # Calculation if given start time and range
        elif gapday or gaphour or gapmin:
            # Calculate end date
            mingap = Calc_Gap_Min(gapday,gaphour,gapmin)
            dt_end = dt_start + timedelta(minutes=mingap)
            eday = dt_end.day
            emonth = dt_end.month
            eyear = dt_end.year
            ehour = dt_end.hour
            emin = dt_end.minute
            esec = dt_end.second
            main.Time = dt_end
            main.TimeGapMinutes = abs(mingap) * -1

    # calculation if not given start time
    elif eday and emonth and eyear:
        dt_end = InputTime_to_DateTime(eday, emonth, eyear, ehour, emin, esec)

        # Calculation if given end time and range
        if gapday or gaphour or gapmin:
            # Calculate start date
            mingap = Calc_Gap_Min(gapday,gaphour,gapmin)
            dt_start = dt_end - timedelta(minutes=mingap)
            sday = dt_start.day
            smonth = dt_start.month
            syear = dt_start.year
            shour = dt_start.hour
            smin = dt_start.minute
            ssec = dt_start.second
            main.Time = dt_end
            main.TimeGapMinutes = abs(mingap) * -1

    else:
        print("Wrong")

    return sday,smonth,syear,shour,smin,ssec,eday,emonth,eyear,ehour,emin,esec,gapday,gaphour,gapmin


# Converts user inputs into datetime or returns "Bad Time"
def InputTime_to_DateTime(day, month, year, hour, min, sec):
    from datetime import datetime

    if len(year) > 2: year = year[-2:]
    if hour == "": hour = str(0)
    if min == "": min = str(0)
    if sec == "": sec = str(0)

    # checks if decimal value,
    if day.isdecimal() and month.isdecimal() and hour.isdecimal() and year.isdecimal() and min.isdecimal() and sec.isdecimal() \
        and len(day)<3 and len(month)<3 and len(year)<3 and len(hour)<3 and len(min)<3 and len(sec)<3 \
            and 0 < int(month) <= 12 and 0 < int(day) <= 31 and 0 <= int(hour) < 24 and 0 <= int(min) < 60 and 0 <= int(sec) < 60:

        time = '%s/%s/%s %s:%s:%s' % (day, month, year, hour, min, sec)
        dt_time = datetime.strptime(time, '%d/%m/%y %H:%M:%S')

    else:
        print("bad time")

    return dt_time


# Coverts days, hours, and mins into mins for SQL pull
def Calc_Gap_Min(day, hour, min):

    if day == "": day = 0
    if hour == "": hour = 0
    if min == "": min = 0

    day = int(day)
    hour = int(hour)
    min = int(min)

    return (day*24*60) + (hour*60) + min
