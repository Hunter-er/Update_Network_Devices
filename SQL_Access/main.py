from datetime import datetime

host = '26.147.79.29'
database = 'Runtime'
user = 'wwUser'  # Base user for queries
password = 'wwUser'  # Base user for queries

TagList = ['Utility_Main_Current_Iavg', 'ASRS2_Current_Iavg', 'TC3.PAS.PAS_ZSE4803_EXT_POS']
Time = datetime.now()
# Time = 'now'
TimeGapMinutes = -30
TagSearchCriteria = ""
DescSearchCriteria = ""
TagName = ""
StartTime = ""
count = 0
CombinedChart = False
SeperatedChart = True

FormattedTagList = []
Oneshot = True
ChartData = []

