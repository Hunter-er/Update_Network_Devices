# Sequence for Pulling data
def PullSQLTags():
    import Format
    import main

    AllTags = Start_SQL_Call("HistTagList")
    main.FormattedTagList = Format.Tag_Dict_to_List(AllTags)


# Starts SQL Call
def Start_SQL_Call(Purpose):
    import Format
    import main

    if Purpose == "HistTagPull":
        main.TagName = Format.SQL_Tag(main.TagList)
        main.StartTime = Format.SQL_Date(main.Time)

    SQL_Command_string = Format.SQL_Command(Purpose=Purpose)
    SQLData = HistConnect(SQL_Command=SQL_Command_string)

    return SQLData


# Connects to Historian and Runs script
def HistConnect(SQL_Command):
    import pymssql
    import main


    try:
        conn = pymssql.connect(
            host=main.host,
            user=main.user,
            password=main.password,
            database=main.database
        )
        cursor = conn.cursor(as_dict=True)
        cursor.execute(SQL_Command)
        data = cursor.fetchall()
        cursor.close()

    except pymssql.Error as e:
        print(f"Error: {e}")

    if data != "":
        return data
    else: return ""


# Build SQL command for historian data pull
def HistTagPull(TimeGapMinutes, StartTime, TagName):
    HistTagPull_string = '''
                SET NOCOUNT ON
                DECLARE @StartDate DateTime
                DECLARE @EndDate DateTime
                SET @StartDate = DateAdd(mi,%s,%s)
                SET @EndDate = %s
                SET NOCOUNT OFF
                SELECT * FROM (
                SELECT History.TagName, DateTime, Value, StartDateTime
                FROM History
                WHERE History.TagName IN %s
                AND DateTime >= @StartDate
                AND DateTime <= @EndDate) temp WHERE temp.StartDateTime >= @StartDate
                ''' % (TimeGapMinutes, StartTime, StartTime, TagName)

    return HistTagPull_string


# Build SQL command for site tag list
def HistTagList(TagSearchCriteria, DescSearchCriteria):
    HistTagList_string = "SELECT [TagName], [Description] FROM dbo._Tag"

    if TagSearchCriteria != "" and DescSearchCriteria != "":
        HistTagList_string = (HistTagList_string + " WHERE TagName like '%" + TagSearchCriteria +
                              "%' OR Description like '%" + DescSearchCriteria + "%';")
    else:
        if TagSearchCriteria != "":
            HistTagList_string = HistTagList_string + " WHERE TagName like '%" + TagSearchCriteria + "%';"
        if DescSearchCriteria != "":
            HistTagList_string = HistTagList_string + " WHERE Description like '%" + DescSearchCriteria + "%';"

    return HistTagList_string
