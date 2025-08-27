import wx
import main
import Format
import SQL_connect
import sys
import os
import Chart


# Used for creating EXE
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Imagefile = ""
#Imagefile = resource_path("RSBLogo.jpeg")

FrameTitle = main.host + "/" + main.user + "/" + main.database

# Window positioning
x_window = 1200
y_window = 800
x_tagwin = 1200
y_tagwin = 550
x_tagpos = 0
y_tagpos = 0
x_filterwin = 200
y_filterwin = 210
x_filterpos = 0
y_filterpos = 550
x_selectionwin = 590
y_selectionwin = 210
x_selectionpos = 610
y_selectionpos = 550
x_imagewin = 410
y_imagewin = 210
x_imagepos = 200
y_imagepos = 550

# Text and variables
hosttext = "Server: "
databasetext = "Database: "
quickfiletext = "Quick File Run:"
filtertext1 = "Filter 1: "
filtertext2 = "Filter 2: "
filtertext3 = "Filter 3: "
filtertext4 = "Filter 4: "
filtertext5 = "Filter 5: "
filterbuttontext = "Filter"
serverbuttontext = "GO"
quickfilebuttontext = "Run"
notfound = 'No items found in search'
TagList = []
SelectedList = []


class HistFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(x_window, y_window), title=FrameTitle)

        self.TagPanel = TagPanel(self)
        self.FilterPanel = FilterPanel(self)
        self.SelectionPanel = SelectionPanel(self)
        self.ImagePanel = ImagePanel(self)

        TagPanel.Show(self)
        FilterPanel.Show(self)
        SelectionPanel.Show(self)
        ImagePanel.Show(self)


class TagPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(x_tagwin,y_tagwin), pos=(x_tagpos, y_tagpos))

        # Server Select
        self.statichosttxt = wx.StaticText(self, label=hosttext, pos=(10, 10))
        self.selectserverinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(50, 5))

        self.serverbutton = wx.Button(self, label=serverbuttontext, pos=(167, 7))
        self.serverbutton.SetSize((40, 20))
        self.serverbutton.Bind(wx.EVT_BUTTON, self.UpdateServer)

        # Database Select
        # self.statichosttxt = wx.StaticText(self, label=databasetext, pos=(180, 10))
        # self.selectserverinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(235, 5))

        # Quick File Run
        self.staticquicktxt = wx.StaticText(self, label=quickfiletext, pos=(310, 10))
        self.quickfileinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(400, 5))

        self.quickfilebutton = wx.Button(self, label=quickfilebuttontext, pos=(520, 7))
        self.quickfilebutton.SetSize((40, 20))
        self.quickfilebutton.Bind(wx.EVT_BUTTON, self.QuickFileRun)

        # List of available tags
        self.list_tags = wx.ListBox(self, pos=(10, 30), size=(600, 500), choices=TagList)

        # List of selected tags
        self.list_selected = wx.ListBox(self, pos=(700, 30), size=(475, 500),
                                        choices=SelectedList)

        # Button for adding selected tags
        addremfont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.tagaddbutton = wx.Button(self, label=">>", pos=(617, 200))
        self.tagaddbutton.SetSize((76, 76))
        self.tagaddbutton.SetFont(addremfont)
        self.tagaddbutton.Bind(wx.EVT_BUTTON, self.OnAddTagClick)
        # Button for removing selected tags
        self.tagremovebutton = wx.Button(self, label="<<", pos=(617, 300))
        self.tagremovebutton.SetSize((76, 76))
        self.tagremovebutton.SetFont(addremfont)
        self.tagremovebutton.Bind(wx.EVT_BUTTON, self.OnRemoveTagClick)


    # Selects new server, no input defaults to host in main
    def UpdateServer(self, fakearg):
        FilterPanel = self.GetParent().FilterPanel
        FilterPanel.filterbutton.Disable()

        # if no input default to main.host variable
        if self.selectserverinput.GetValue() != "":
            main.host = self.selectserverinput.GetValue()

        AllTags = SQL_connect.Start_SQL_Call("HistTagList")
        main.FormattedTagList = Format.Tag_Dict_to_List(AllTags)
        TagList = main.FormattedTagList

        self.list_tags.Set(TagList)
        FilterPanel.filterbutton.Enable()

    # Quick file run
    def QuickFileRun(self, fakearg):
        print("quick file run")


    def OnAddTagClick(self, fakearg):
        selection = self.list_tags.GetSelection()
        if selection != wx.NOT_FOUND:
            item = self.list_tags.GetString(selection)
            self.list_selected.Append(item)
            self.list_tags.Delete(selection)


    def OnRemoveTagClick(self, fakearg):
        selection = self.list_selected.GetSelection()
        if selection != wx.NOT_FOUND:
            item = self.list_selected.GetString(selection)
            self.list_tags.Append(item)
            self.list_selected.Delete(selection)


class FilterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(x_filterwin, y_filterwin), pos=(x_filterpos, y_filterpos))

        # Filter Pane
        self.staticfilter1txt = wx.StaticText(self, label=filtertext1, pos=(10, 5))
        self.selectfilter1input = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(60, 0))
        self.staticfilter2txt = wx.StaticText(self, label=filtertext2, pos=(10, 35))
        self.selectfilter2input = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(60, 30))
        self.staticfilter3txt = wx.StaticText(self, label=filtertext3, pos=(10, 65))
        self.selectfilter3input = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(60, 60))
        self.staticfilter4txt = wx.StaticText(self, label=filtertext4, pos=(10, 95))
        self.selectfilter4input = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(60, 90))
        self.staticfilter5txt = wx.StaticText(self, label=filtertext5, pos=(10, 125))
        self.selectfilter5input = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(60, 120))

        self.filterbutton = wx.Button(self, label=filterbuttontext, pos=(70, 150))
        self.filterbutton.Bind(wx.EVT_BUTTON, self.OnFilterClick)
        self.filterbutton.Disable()


    def OnFilterClick(self, fakearg):
        filter1 = self.selectfilter1input.GetValue().lower()
        filter2 = self.selectfilter2input.GetValue().lower()
        filter3 = self.selectfilter3input.GetValue().lower()
        filter4 = self.selectfilter4input.GetValue().lower()
        filter5 = self.selectfilter5input.GetValue().lower()

        if filter1 != "" or filter2 != "" or filter3 != "" or filter4 != "" or filter5 != "":
            TagList = self.UpdateFilterList(filter1, filter2, filter3, filter4, filter5)
        else:
            TagList = main.FormattedTagList

        TagPanel = self.GetParent().TagPanel
        TagPanel.list_tags.Set(TagList)


    def UpdateFilterList(self, filteritem1, filteritem2, filteritem3, filteritem4, filteritem5):
        newlist = []
        for tag in main.FormattedTagList:
            if ((filteritem1 in tag.lower()) and (filteritem2 in tag.lower()) and (filteritem3 in tag.lower())
                    and (filteritem4 in tag.lower()) and (filteritem5 in tag.lower())):
                newlist.append(tag)
        if newlist == []:
            newlist = [notfound]
        return newlist


class SelectionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(x_selectionwin, y_selectionwin), pos=(x_selectionpos, y_selectionpos))

        # Check boxes
        self.senddatatocsvcheckbox = wx.CheckBox(self, label='Export Data to CSV', pos=(10, 10))
        self.createsinglechartcheckbox = wx.CheckBox(self, label='Create Single Chart', pos=(10, 30))
        self.createstackedchartcheckbox = wx.CheckBox(self, label='Create Stacked Chart', pos=(10, 50))

        # Start Time
        self.staticdatetxt = wx.StaticText(self, label='Start Date:', pos=(200, 10))
        # self.selectdateinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(375, 5))
        # self.selectdateinput.SetSize(150,25)
        self.selectmonthinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(260, 5))
        self.selectmonthinput.SetSize(25,25)
        self.selectdayinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(290, 5))
        self.selectdayinput.SetSize(25,25)
        self.selectyearinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(320, 5))
        self.selectyearinput.SetSize(40, 25)
        self.selecthourinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(385, 5))
        self.selecthourinput.SetSize(25, 25)
        self.selectminuteinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(415, 5))
        self.selectminuteinput.SetSize(25, 25)
        self.selectsecondinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(445, 5))
        self.selectsecondinput.SetSize(25, 25)

        self.staticmonthtxt = wx.StaticText(self, label=' DD', pos=(290, 30))
        self.staticdaytxt = wx.StaticText(self, label='MM', pos=(260, 30))
        self.staticyeartxt = wx.StaticText(self, label='  YYYY', pos=(320, 30))
        self.statichourtxt = wx.StaticText(self, label='  hh', pos=(385, 30))
        self.staticminutetxt = wx.StaticText(self, label='mm', pos=(415, 30))
        self.staticsecondtxt = wx.StaticText(self, label='   ss', pos=(445, 30))

        # Clear Start Time Button
        self.clearstarttimebutton = wx.Button(self, label='Clear Start', pos=(485, 5))
        self.clearstarttimebutton.Bind(wx.EVT_BUTTON, self.OnClearStartTimeButton)

        # Time Range Selection
        self.statictimegaptxt = wx.StaticText(self, label='Time Range:', pos=(200, 60))
        #self.selecttimegapinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(300, 65))

        self.gapdaysinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(275, 55))
        self.gapdaysinput.SetSize(50, 25)
        self.gaphoursinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(330, 55))
        self.gaphoursinput.SetSize(50, 25)
        self.gapminutesinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(385, 55))
        self.gapminutesinput.SetSize(50, 25)

        self.staticgapdaystxt = wx.StaticText(self, label='    Days', pos=(275, 80))
        self.staticgaphourstxt = wx.StaticText(self, label='   Hours', pos=(330, 80))
        self.staticgapminutestxt = wx.StaticText(self, label=' Minutes', pos=(385, 80))

        # Clear Time Range Button
        self.clearrangetimebutton = wx.Button(self, label='Clear Range', pos=(485, 55))
        self.clearrangetimebutton.Bind(wx.EVT_BUTTON, self.OnClearRangeTimeButton)

        # End Date
        self.staticdatetxtend = wx.StaticText(self, label='End Date:', pos=(200, 110))
        # self.selectdateinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(375, 5))
        # self.selectdateinput.SetSize(150,25)
        self.selectmonthinputend = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(260, 105))
        self.selectmonthinputend.SetSize(25, 25)
        self.selectdayinputend = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(290, 105))
        self.selectdayinputend.SetSize(25, 25)
        self.selectyearinputend = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(320, 105))
        self.selectyearinputend.SetSize(40, 25)
        self.selecthourinputend = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(385, 105))
        self.selecthourinputend.SetSize(25, 25)
        self.selectminuteinputend = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(415, 105))
        self.selectminuteinputend.SetSize(25, 25)
        self.selectsecondinputend = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(445, 105))
        self.selectsecondinputend.SetSize(25, 25)

        self.staticmonthtxtend = wx.StaticText(self, label=' DD', pos=(290, 130))
        self.staticdaytxtend = wx.StaticText(self, label='MM', pos=(260, 130))
        self.staticyeartxtend = wx.StaticText(self, label='  YYYY', pos=(320, 130))
        self.statichourtxtend = wx.StaticText(self, label='  hh', pos=(385, 130))
        self.staticminutetxtend = wx.StaticText(self, label='mm', pos=(415, 130))
        self.staticsecondtxtend = wx.StaticText(self, label='   ss', pos=(445, 130))

        # Clear End Time Button
        self.clearendtimebutton = wx.Button(self, label='Clear End', pos=(485, 105))
        self.clearendtimebutton.Bind(wx.EVT_BUTTON, self.OnClearEndTimeButton)

        # Verify Time Button
        self.verifytimebutton = wx.Button(self, label='Update Time', pos=(300, 170))
        self.verifytimebutton.Bind(wx.EVT_BUTTON, self.OnVerifyTimeButtonClick)

        # Filename for CSV
        self.staticfilenametxt = wx.StaticText(self, label='CSV Data Filename:', pos=(10, 100))
        self.selectfilenameinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(10, 120))
        self.selectfilenameinput.SetSize(150, 25)

        # Create Report Button
        self.createreportbutton = wx.Button(self, label='Create Report', pos=(450, 170))
        self.createreportbutton.Bind(wx.EVT_BUTTON, self.OnCreateReportButtonClick)


    def OnClearStartTimeButton(self, fakearg):
        self.selectmonthinput.Label = ""
        self.selectdayinput.Label = ""
        self.selectyearinput.Label = ""
        self.selecthourinput.Label = ""
        self.selectminuteinput.Label = ""
        self.selectsecondinput.Label = ""

    def OnClearRangeTimeButton(self, fakearg):
        self.gapdaysinput.Label = ""
        self.gaphoursinput.Label = ""
        self.gapminutesinput.Label = ""

    def OnClearEndTimeButton(self, fakearg):
        self.selectmonthinputend.Label = ""
        self.selectdayinputend.Label = ""
        self.selectyearinputend.Label = ""
        self.selecthourinputend.Label = ""
        self.selectminuteinputend.Label = ""
        self.selectsecondinputend.Label = ""


    def OnVerifyTimeButtonClick(self, fakearg):
        smonth =  self.selectmonthinput.GetValue()
        sday = self.selectdayinput.GetValue()
        syear = self.selectyearinput.GetValue()
        shour = self.selecthourinput.GetValue()
        smin = self.selectminuteinput.GetValue()
        ssec = self.selectsecondinput.GetValue()
        emonth = self.selectmonthinputend.GetValue()
        eday = self.selectdayinputend.GetValue()
        eyear = self.selectyearinputend.GetValue()
        ehour = self.selecthourinputend.GetValue()
        emin = self.selectminuteinputend.GetValue()
        esec = self.selectsecondinputend.GetValue()
        gapday = self.gapdaysinput.GetValue()
        gaphour = self.gaphoursinput.GetValue()
        gapmin = self.gapminutesinput.GetValue()

        newvalues = Format.Update_TimeFrame(sday,smonth,syear,shour,smin,ssec,eday,emonth,eyear,ehour,emin,
                                            esec,gapday,gaphour,gapmin)

        sday = newvalues[0]
        smonth = newvalues[1]
        syear = newvalues[2]
        shour = newvalues[3]
        smin = newvalues[4]
        ssec = newvalues[5]
        eday = newvalues[6]
        emonth = newvalues[7]
        eyear = newvalues[8]
        ehour = newvalues[9]
        emin = newvalues[10]
        esec = newvalues[11]
        gapday = newvalues[12]
        gaphour = newvalues[13]
        gapmin = newvalues[14]

        self.selectmonthinput.Label = str(smonth)
        self.selectdayinput.Label = str(sday)
        self.selectyearinput.Label = str(syear)
        self.selecthourinput.Label = str(shour)
        self.selectminuteinput.Label = str(smin)
        self.selectsecondinput.Label = str(ssec)
        self.selectmonthinputend.Label = str(emonth)
        self.selectdayinputend.Label = str(eday)
        self.selectyearinputend.Label = str(eyear)
        self.selecthourinputend.Label = str(ehour)
        self.selectminuteinputend.Label = str(emin)
        self.selectsecondinputend.Label = str(esec)
        self.gapdaysinput.Label = str(gapday)
        self.gaphoursinput.Label = str(gaphour)
        self.gapminutesinput.Label = str(gapmin)


    def OnCreateReportButtonClick(self, fakearg):
        CreateStackedChart = False; CreateSingleChart = False; ExportData = False
        if self.createsinglechartcheckbox.GetValue() == True: CreateSingleChart = True # Create single chart
        if self.createstackedchartcheckbox.GetValue() == True: CreateStackedChart = True # Create stacked chart
        if self.senddatatocsvcheckbox.GetValue() == True: ExportData = True # Export data to CSV

        TagPanel = self.GetParent().TagPanel
        SelectedList = TagPanel.list_selected.GetStrings()

        # If items in list, then format tag names (remove descriptions) and chart data
        if SelectedList != []:
            FormattedSelectedList = Format.Remove_Desc_Selected_List(SelectedList)
            main.TagList = FormattedSelectedList
            DataPull = SQL_connect.Start_SQL_Call(Purpose="HistTagPull")
            ChartData = Format.Plot_Data(SQLData=DataPull, Taglist=FormattedSelectedList)

            if (CreateStackedChart or CreateSingleChart):
                Chart.Create_Plot(ChartData=ChartData, Taglist=FormattedSelectedList, CombinedChart=CreateSingleChart,
                            SeperatedChart=CreateStackedChart)

            if ExportData:
                FileName = self.selectfilenameinput.GetValue()
                if FileName != "":
                    Chart.Export_to_CSV(Data=ChartData, Tags=FormattedSelectedList, FileName=FileName)


class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(x_imagewin, y_imagewin), pos=(x_imagepos, y_imagepos))

        # Image/Logo
        if Imagefile != "":

            image = wx.Image(Imagefile, wx.BITMAP_TYPE_JPEG)
            temp = image.ConvertToBitmap()

            imagewidth = temp.GetWidth()
            imageheight = temp.GetHeight()
            image_x = int((x_imagewin - imagewidth) / 2)
            image_y = int((y_imagewin - imageheight) / 2)

            self.bmp = wx.StaticBitmap(parent=self, bitmap=temp, pos=(image_x, image_y))


app = wx.App()
window = HistFrame(None)
window.Show(True)
app.MainLoop()
