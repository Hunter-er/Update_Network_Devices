import csv
import webbrowser
import wx
from pycomm3 import LogixDriver
import sys
import os


# Used for creating EXE
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# File names
IPfile = resource_path("PFSPLCtoCameraPerLine.csv")
Imagefile = resource_path("download2.jpeg")

# Constant Variables
titletext = "PFS Updater"
headertext = "PFS UPDATE APP"
staticlinetext = "Select Line to View"
lineupdatebuttontext = "Select Line"
updatetriggerbuttontext = "Update Trigger Point"
triggerpointtext = "Trigger Point: "
errormessagetext = "  Incorrect Line Information  "
faultresetbuttontext = "Fault Reset"

# Initial values, update once lines are selected
previoustriggertext = ""
nofaultresetmessagetext = ""
noerrormessagetext = ""
PFSLineSelected = ""
TriggerPoint = ""
previoustrigger = ""
CameraIP = ""
CameraName = ""
TestValue = ""
CAM = ""
line = ""
webtitle = ""
url = ""
size = ""
pos = ""

# Frame dimensions
frameposx = 200
frameposy = 200
framesizex = 165
framesizey = 420
weboffsetx = 0
weboffsety = 0
websizew = 675
websizeh = 525
hiddenvalues = 1000


def Line_Num_to_IP(linenum):
    if linenum == "19A" or linenum == "20A" or linenum == "19a" or linenum == "20a" or \
            (str(linenum).isdigit() and 0 < int(linenum) < 200):
        if linenum == "20a": linenum = "20A"
        if linenum == "19a": linenum = "19A"

        with open(IPfile) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[2] == linenum:
                    IP_PLC = row[0]
                    Line_num = row[2]
                    IP_Cam = row[3]
                    Cam_Name = row[4]

                    return IP_PLC, Line_num, IP_Cam, Cam_Name


def Call_PFS_PLC(PLCIP, Line, CAMIP, CAMName):
    with LogixDriver(PLCIP) as plcr:
        plcr.open()
        PLCTestValue = (plcr.name + " " + str(Line))
        PLCTriggerPoint = plcr.read(CAMName + '_ENC_TARGET_READ')
        PLCPFSLineSelected = plcr.read(CAMName + '_NAME')

    return [PLCTriggerPoint, PLCPFSLineSelected, CAMIP, CAMName, PLCIP, PLCTestValue]


def Cleanup_PLC_Trigger(trig):
    return trig[1]


def Cleanup_PLC_Line(linenu):
    return linenu[1]


def Open_Browser(CAMn, linen):
    webbrowser.open(CAMn)


def Update_Trigger(UCameraName, UCameraIP, TriggerUpdate, PLCip):
    with LogixDriver(PLCip) as plcw:
        plcw.open()
        plcw.write((UCameraName + '_ENC_TARGET_WRITE', int(TriggerUpdate)))
        UpdatedTriggerPoint = plcw.read(UCameraName + '_ENC_TARGET_READ')

    return UpdatedTriggerPoint


def Fault_Reset(FaCameraName, FaPLCip):
    with LogixDriver(FaPLCip) as plcw:
        plcw.open()
        plcw.write((FaCameraName + '_FAULT_RESET', 1))


class PFSPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Title Bar
        self.statictitletxt = wx.StaticText(self, label=headertext, pos=(30, 0))

        # Area to select PFS line
        self.staticlinetxt = wx.StaticText(self, label=staticlinetext, pos=(25, 30))
        self.lineinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(20, 50))
        self.lineupdatebutton = wx.Button(self, label=lineupdatebuttontext, pos=(35, 80))
        self.lineupdatebutton.Bind(wx.EVT_BUTTON, self.OnLineButtonClick)

        # Status Message
        self.errormessagetxt = wx.StaticText(self, label=noerrormessagetext, pos=(0, 15))
        self.errormessagetxt.SetForegroundColour(wx.Colour(255, 255, 255))
        self.errormessagetxt.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.faultmessagetxt = wx.StaticText(self, label=nofaultresetmessagetext, pos=(0, 15))
        self.faultmessagetxt.SetForegroundColour(wx.Colour(0, 0, 0))
        self.faultmessagetxt.SetBackgroundColour(wx.Colour(0, 255, 0))

        # Fault Reset Button
        self.faultresetbutton = wx.Button(self, label=faultresetbuttontext, pos=(33, 240))
        self.faultresetbutton.Bind(wx.EVT_BUTTON, self.OnFaultResetClick)

        # Area to update trigger
        self.lineselectedtxt = wx.StaticText(self, label=str(PFSLineSelected), pos=(40, 220))
        self.triggerpointtxt = wx.StaticText(self, label=(triggerpointtext + str(TriggerPoint)), pos=(20, 270))
        self.triggerinput = wx.TextCtrl(self, style=wx.TE_CENTER, pos=(20, 290))
        self.triggerupdatebutton = wx.Button(self, label=updatetriggerbuttontext, pos=(10, 320))
        self.triggerupdatebutton.Bind(wx.EVT_BUTTON, self.OnTrigUpdateButtonClick)
        self.prevtrigger = wx.StaticText(self, label=(previoustriggertext + str(previoustrigger)), pos=(10, 350))

        # Test values
        self.cameraIP = wx.StaticText(self, label=str(CameraIP), pos=(40, 155 + hiddenvalues))
        self.cameraName = wx.StaticText(self, label=str(CameraName), pos=(40, 135 + hiddenvalues))
        self.plcIP = wx.StaticText(self, label=str(CameraName), pos=(40, 175 + hiddenvalues))
        self.testvalue = wx.StaticText(self, label=str(TestValue), pos=(40, 115 + hiddenvalues))

        # Image
        temp = image.ConvertToBitmap()
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp, pos=(20, 115))

    def OnLineButtonClick(self, wx_core_placeholder):
        PLCCallList = Line_Num_to_IP(self.lineinput.GetValue())

        if PLCCallList is not None:
            UpdateInfo = Call_PFS_PLC(PLCCallList[0], PLCCallList[1], PLCCallList[2], PLCCallList[3])

            OTriggerPoint = "Trigger Point:   " + str(Cleanup_PLC_Trigger(UpdateInfo[0]))
            self.triggerpointtxt.Label = OTriggerPoint

            OPFSLineSelected = str(Cleanup_PLC_Line(UpdateInfo[1]))
            self.lineselectedtxt.Label = OPFSLineSelected

            OCameraIP = str(UpdateInfo[2])
            self.cameraIP.Label = OCameraIP

            OCameraName = str(UpdateInfo[3])
            self.cameraName.Label = OCameraName

            OPLCIP = str(UpdateInfo[4])
            self.plcIP.Label = OPLCIP

            OTestValue = str(UpdateInfo[5])
            self.testvalue.Label = OTestValue

            self.errormessagetxt.Label = ""
            self.faultmessagetxt.Label = ""

            Open_Browser(OCameraIP, OPFSLineSelected)

        else:
            self.errormessagetxt.Label = errormessagetext

    def OnTrigUpdateButtonClick(self, wx_core_placeholder):
        NewTrigger = self.triggerinput.GetValue()
        TCameraIP = self.cameraIP.Label
        TCameraName = self.cameraName.Label
        TPLCIP = self.plcIP.Label

        if NewTrigger != "" and TPLCIP != "":
            UpdatedTrigger = Update_Trigger(TCameraName, TCameraIP, NewTrigger, TPLCIP)
            self.prevtrigger.Label = "Prev " + self.triggerpointtxt.Label
            self.triggerpointtxt.Label = "Trigger Point:   " + str(Cleanup_PLC_Trigger(UpdatedTrigger))

    def OnFaultResetClick(self, wx_core_placeholder):
        FCameraName = self.cameraName.Label
        FPLCIP = self.plcIP.Label
        if FCameraName is not None and FPLCIP is not None:
            Fault_Reset(FCameraName, FPLCIP)
            self.faultmessagetxt.Label = "                Fault Reset                "


class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.PFSPanelIm = None

    def ImageSetup(self):
        image1 = wx.Image(Imagefile, wx.BITMAP_TYPE_JPEG)
        self.PFSPanelIm = PFSPanel(image1)
        self.PFSPanelIm.Show()


app = wx.App()
frame = wx.Frame(None, title=titletext, size=(framesizex, framesizey), pos=(frameposx, frameposy))
image = wx.Image(Imagefile, wx.BITMAP_TYPE_JPEG)
panel = PFSPanel(frame)
frame.Show()
app.MainLoop()
