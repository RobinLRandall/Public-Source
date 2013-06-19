#!/usr/bin/env python
#########################################################
#  Author: Robin Randall
#    File: Notepad--.py
#    Date: 05/09/2013
#  Copyright (C) 2013, Robin Randall, All Rights Reserved
#  Internet Credits: Noel Rappin
#                    Robin Dunn  (wxPython in Action, 2006)
#                    Sharma vivek
#########################################################
import  wx
import  wx.html
from    wx.html import HtmlEasyPrinting
import  wx.lib.docview
from    wx.lib.wordwrap  import wordwrap
import  re, sys, os, codecs, string
import  time
import  shutil
from    DateDlg  import DateDialog
# This is the main frame where all the widgets are added       
class MyFrame(wx.Frame):
    def __init__(self):
        global frame
        wx.Frame.__init__(self, None, -1, "Untitled Notepad--", size=(600, 400) )
        self.sizeH = 250  # For Toolbar size
        self.log= open("Notepad--.log",'w+')
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.shellName='frame'
        # Setup icon on title bar
        _icon = wx.Icon("C:\\K\\notepad--.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(_icon)
        self.config_Dates= {'MDY':'%A, %m/%d/%y ', 'YMD':'%A, %y/%m/%y ', 'DMY':'%A, %d/%m/%y '}
        #============================================================================
        # Create Edit Area
        self.edit_ctrl = wx.TextCtrl(self, wx.ID_ANY,
             style=wx.TE_MULTILINE|wx.TE_RICH2|wx.SUNKEN_BORDER|wx.HSCROLL|wx.ALWAYS_SHOW_SB)
	sizer.Add(self.edit_ctrl, 1, wx.ALL|wx.EXPAND)
        self.curFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.edit_ctrl.SetMinSize((700, 400))     
        self.edit_ctrl.SetValue('.'*200)
        self.edit_ctrl.SetValue('') 
        self.fcurClr=self.edit_ctrl.GetForegroundColour()
        self.bcurClr=self.edit_ctrl.GetBackgroundColour()
        self.edit_ctrl.SetFont(self.curFont)
        #Set colors
        self.colors()
        self.iconized = False
        #Find Initialize
	self.findDlg = None
	self.findData = wx.FindReplaceData(flags=1)  # Defaults:(*) Down direction set
	#                                  flag =2  when set    [ ] Whole Word only = String search
 	#                                  flag =4  when set    [ ] Match Case      = IGNORECASE       
        #============================================================================
        # Menu Bar
        self.bar=False
        # Shortcuts
        self.OPSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_open,         id=self.OPSC)
        self.SVSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_save,         id=self.SVSC)
        self.SASC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_save  ,       id=self.SASC)
        self.RNSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_rename  ,     id=self.RNSC)	
        self.PSSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_pageSetup,    id=self.PSSC)	
        self.PPSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_printPreview, id=self.PPSC)	
        self.PRSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_print,        id=self.PRSC)	
        self.EXSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.file_exit,         id=self.EXSC)
	self.RDSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.edit_redo,         id=self.RDSC)
	self.DLSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.edit_delete,       id=self.DLSC)	
	self.FDSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.OnShowFind,        id=self.FDSC)
	self.FNSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.OnShowFind,        id=self.FNSC)	
	self.RPSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.OnShowFindReplace, id=self.RPSC)
	self.GTSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.edit_goto,         id=self.GTSC)
	self.SLSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.edit_selectAll,    id=self.SLSC)
	self.TDSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.edit_date_MDY,     id=self.TDSC)
	self.WWSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.format_wordWrap,   id=self.WWSC)
	self.FTSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.format_font,       id=self.FTSC)
	self.SBSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.view_statusBar,   id=self.SBSC)
	self.HTSC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.help_topics,       id=self.HTSC)
	self.HASC = wx.NewId()
	self.Bind(wx.EVT_MENU, self.help_about,        id=self.HASC)
	
	self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('O'),    self.OPSC ),
	                                      (wx.ACCEL_CTRL, ord('S'),    self.SVSC ),
	                                      (wx.ACCEL_CTRL, ord('E'),    self.SASC ),
	                                      (wx.ACCEL_CTRL, ord('R'),    self.RNSC ),	                                      
                                              (wx.ACCEL_NORMAL, wx.WXK_F7, self.PSSC ),
                                              (wx.ACCEL_NORMAL, wx.WXK_F8, self.PPSC ),
	                                      (wx.ACCEL_CTRL, ord('P'),    self.PRSC ),
	                                      (wx.ACCEL_CTRL, ord('Q'),    self.EXSC ),
                                              (wx.ACCEL_CTRL, ord('Y'),    self.RDSC ),
                                              (wx.ACCEL_NORMAL, wx.WXK_DELETE, self.DLSC ),                                           
                                              (wx.ACCEL_CTRL, ord('F'),    self.FDSC ),
                                              (wx.ACCEL_NORMAL, wx.WXK_F3, self.FNSC ),
                                              (wx.ACCEL_CTRL, ord('H'),    self.RPSC ),
                                              (wx.ACCEL_CTRL, ord('G'),    self.GTSC ),
                                              (wx.ACCEL_CTRL, ord('A'),    self.SLSC ),
                                              (wx.ACCEL_NORMAL, wx.WXK_F5, self.TDSC ),
                                              (wx.ACCEL_CTRL, ord('W'),    self.WWSC ),
                                              (wx.ACCEL_CTRL, ord('T'),    self.FTSC ),
                                              (wx.ACCEL_CTRL, ord('U'),    self.SBSC ),
                                              (wx.ACCEL_CTRL, ord('I'),    self.HTSC ),                                                                        (wx.ACCEL_CTRL, ord('B'),    self.HASC )])
	self.SetAcceleratorTable(self.accel_tbl)
	#-----------------------------------------------------------------------
        self.frame_menubar = wx.MenuBar()
        self.File = wx.Menu()
        self.New = wx.MenuItem(self.File,    wx.NewId(),  "&New\tCtrl+N", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.New) 
        self.Open = wx.MenuItem(self.File,   wx.NewId(),  "&Open...\tCtrl+O", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.Open)
        self.Save = wx.MenuItem(self.File,   wx.NewId(),  "&Save\tCtrl+S", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.Save)      
        self.SaveAs = wx.MenuItem(self.File, wx.NewId(),  "Sav&e As...\tCtrl+E", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.SaveAs)
        self.Rename = wx.MenuItem(self.File, wx.NewId(),  "&Rename...\tCtrl+R", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.Rename)        
        #-----------------------------------------------------------------------
        self.File.AppendSeparator()
        self.PageSetup = wx.MenuItem(self.File,    wx.NewId(), "Page Setup...\tF7", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.PageSetup) 
        self.PrintPreview = wx.MenuItem(self.File, wx.NewId(), "Print Preview...\tF8", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.PrintPreview)         
        self.Print = wx.MenuItem(self.File,        wx.NewId(), "&Print...\tCtrl+P", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.Print)        
        #-----------------------------------------------------------------------
        self.File.AppendSeparator()        
        self.File_1 = wx.MenuItem(self.File,         wx.NewId(), "1.", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.File_1)
        self.File_2 = wx.MenuItem(self.File,         wx.NewId(), "2.", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.File_2)
        self.File_3 = wx.MenuItem(self.File,         wx.NewId(), "3.", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.File_3)
        self.File_4 = wx.MenuItem(self.File,         wx.NewId(), "4.", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.File_4)        
        #-----------------------------------------------------------------------       
        self.File.AppendSeparator()
        self.Exit = wx.MenuItem(self.File,         wx.NewId(), "Exit\tCtrl+Q", "", wx.ITEM_NORMAL)
        self.File.AppendItem(self.Exit)
        self.frame_menubar.Append(self.File, "&File")
        #=======================================================================
        self.Edit = wx.Menu()
        self.Undo = wx.MenuItem(self.Edit,         wx.NewId(), "Undo\tCtrl+Z", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.Undo)
        self.Redo = wx.MenuItem(self.Edit,         wx.NewId(), "Redo\tCtrl+Y", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.Redo)        
        #-----------------------------------------------------------------------
        self.Edit.AppendSeparator()
        self.Cut = wx.MenuItem(self.Edit,    wx.NewId(),       "Cut\tCtrl+X", "", wx.ITEM_NORMAL)
        self.Cut.Enable(True)        
        self.Edit.AppendItem(self.Cut)
        self.Copy = wx.MenuItem(self.Edit,   wx.NewId(),       "&Copy\tCtrl+C", "", wx.ITEM_NORMAL)
        self.Copy.Enable(True)
        self.Edit.AppendItem(self.Copy)
        self.Paste = wx.MenuItem(self.Edit,  wx.NewId(),       "Paste\tCtrl+V", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.Paste)
        self.Delete = wx.MenuItem(self.Edit, wx.NewId(),       "Delete\tDel", "", wx.ITEM_NORMAL)
        self.Delete.Enable(True)        
        self.Edit.AppendItem(self.Delete) 
        #-----------------------------------------------------------------------
        self.Edit.AppendSeparator()
        self.Find = wx.MenuItem(self.Edit,     wx.NewId(),     "&Find...\tCtrl+F", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.Find)
        self.Find.Enable(True)
        self.FindNext = wx.MenuItem(self.Edit, wx.NewId(),     "Find Next\tF3", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.FindNext)
        self.FindNext.Enable(True)        
        self.Replace = wx.MenuItem(self.Edit,  wx.NewId(),     "Replace...\tCtrl+H", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.Replace)
        self.Replace.Enable(True)        
        self.GoTo = wx.MenuItem(self.Edit,     wx.NewId(),     "&Go To...\tCtrl+G", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.GoTo)
        #-----------------------------------------------------------------------
        self.Edit.AppendSeparator()
        self.SelectAll = wx.MenuItem(self.Edit, wx.NewId(),    "Select &All\tCtrl+A", "", wx.ITEM_NORMAL)
        self.Edit.AppendItem(self.SelectAll)
        self.TimeDate = wx.Menu()
        #self.Edit.AppendItem(self.TimeDate)
        # sub menu TimeDate
	self.Date_MDY =  wx.MenuItem(self.TimeDate, wx.NewId(), "MDY  ","", wx.ITEM_NORMAL)        
	self.TimeDate.AppendItem(self.Date_MDY)
	self.Date_YMD =  wx.MenuItem(self.TimeDate, wx.NewId(), "YMD  ","", wx.ITEM_NORMAL)
	self.TimeDate.AppendItem(self.Date_YMD)	
	self.Date_DMY =  wx.MenuItem(self.TimeDate, wx.NewId(), "DMY  ","", wx.ITEM_NORMAL)
	self.TimeDate.AppendItem(self.Date_DMY)	
	self.Time24 = wx.MenuItem(self.TimeDate, wx.NewId(), "Time24H ","", wx.ITEM_NORMAL)
	self.TimeDate.AppendItem(self.Time24)
	self.Time12 = wx.MenuItem(self.TimeDate, wx.NewId(), "Time12H ","", wx.ITEM_NORMAL)
	self.TimeDate.AppendItem(self.Time12)
	self.Edit.AppendMenu(13,"Date/Time\tF5",self.TimeDate)  
        self.frame_menubar.Append(self.Edit, "&Edit")
        #=======================================================================
        self.Format = wx.Menu()
        self.WordWrap = wx.MenuItem(self.Format, wx.NewId(),   "Word &Wrap\tCtrl+W", "", wx.ITEM_CHECK)
        self.Format.AppendItem(self.WordWrap)
        self.Font_ = wx.MenuItem(self.Format,    wx.NewId(),   "Fon&t...\tCtrl+T", "", wx.ITEM_NORMAL)
        self.Format.AppendItem(self.Font_)
        self.LineNos = wx.MenuItem(self.Format,  wx.NewId(),   '&Show Line Nos\tCtrl+Shift+L',"", wx.ITEM_CHECK)
        self.Format.AppendItem(self.LineNos)  
        self.Convert = wx.Menu()
        self.ToUpper=self.Convert.Append(-1,'To Upper Case')        
        self.ToLower=self.Convert.Append(-1,'To Lower Case')        
        self.Format.AppendMenu(-1, "Convert", self.Convert, "")          
        self.frame_menubar.Append(self.Format, "&Format") 
        #=======================================================================
        self.View = wx.Menu()
        self.Toolbar = self.CreateToolBar()
	self.toolBar = wx.MenuItem(self.View,     wx.NewId(),     "&Toolbar\tCtrl+L", "", wx.ITEM_CHECK)
	# To Do ... Refactor bitmaps
	bmp = wx.Image('FNEW.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tnew = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "New", "New")
	bmp = wx.Image('fileopen.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.topen = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Open", "Open")
	bmp = wx.Image('filesave.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tsave = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Save", "Save")
	self.Toolbar.AddSeparator()
	bmp = wx.Image('fileprint.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tprint = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Print", "Print")
	bmp = wx.Image('printpreview.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tprintpre = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Preview", "Preview")
	self.Toolbar.AddSeparator()
	bmp = wx.Image('editcut.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tcut = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Cut", "Cut")
	bmp = wx.Image('editcopy.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tcopy = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Copy", "Copy")
	bmp = wx.Image('editpaste.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tpaste = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Paste", "Paste")
	self.Toolbar.AddSeparator()	
	bmp = wx.Image('editundo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tundo = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Undo", "Undo")	
	bmp = wx.Image('editredo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.tredo = self.Toolbar.AddSimpleTool(wx.NewId(), bmp, "Redo", "Redo")	
	bmp = wx.Image('editredo.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	self.Toolbar.Realize()
	_,self.toolbarH = self.Toolbar.GetSize()
	self.View.AppendItem(self.toolBar)
        self.toolBar.Check()
        self.statusBar = wx.MenuItem(self.View, wx.NewId(),   "Stat&us Bar\Ctrl+U", "", wx.ITEM_CHECK)
        self.View.AppendItem( self.statusBar)
        self.statusBar.Check()
        self.frame_menubar.Append(self.View, "&View")
        #=======================================================================
        self.Help = wx.Menu()
        self.Topics = wx.MenuItem(self.Help, wx.NewId(),  "Help Top&ics\tCtrl+I", "", wx.ITEM_NORMAL)
        self.Help.AppendItem(self.Topics)
        self.Help.AppendSeparator()
        self.About = wx.MenuItem(self.Help,  wx.NewId(),  "A&bout Notepad\tCtrl+B", "", wx.ITEM_NORMAL)
        self.Help.AppendItem(self.About)
        self.frame_menubar.Append(self.Help, "&Help")
        self.SetMenuBar(self.frame_menubar)           ###########  END OF MENU BAR
        #======================================================================= 
        # Status Bar
        self.Statusbar = self.CreateStatusBar() 
        self.Statusbar.SetFieldsCount(2)
        self.Statusbar.SetStatusWidths([-80, -20])
        stats="  Ln "+str(1)+", Col "+str(1) 
        self.Statusbar.SetStatusText(stats, 1)
        #self.__set_properties()
        self.__do_layout()
        self.data = wx.PageSetupDialogData(wx.PrintData()) 
        #========================================================================
        # Bindings
        self.Bind(wx.EVT_MENU,  self.file_new,           self.New)        
        self.Bind(wx.EVT_MENU,  self.file_open,          self.Open)
        self.Bind(wx.EVT_MENU,  self.file_save,          self.Save)
        self.Bind(wx.EVT_MENU,  self.file_save,          self.SaveAs) 
        self.Bind(wx.EVT_MENU,  self.file_rename,        self.Rename)         
        self.Bind(wx.EVT_MENU,  self.file_pageSetup,     self.PageSetup) 
        self.Bind(wx.EVT_MENU,  self.file_printPreview,  self.PrintPreview)
        self.Bind(wx.EVT_MENU,  self.file_print,         self.Print)  
        self.Bind(wx.EVT_MENU,  self.file_file_1,        self.File_1)          
        self.Bind(wx.EVT_MENU,  self.file_file_2,        self.File_2)          
        self.Bind(wx.EVT_MENU,  self.file_file_3,        self.File_3)          
        self.Bind(wx.EVT_MENU,  self.file_file_4,        self.File_4)          
        self.Bind(wx.EVT_MENU,  self.file_exit,          self.Exit)
        self.Bind(wx.EVT_CLOSE, self.file_exit)
        # Edit Menu
        self.Bind(wx.EVT_MENU, self.edit_undo,            self.Undo)
        self.Bind(wx.EVT_MENU, self.edit_redo,            self.Redo)
        self.Bind(wx.EVT_MENU, self.edit_cut,             self.Cut)
        self.Bind(wx.EVT_MENU, self.edit_copy,            self.Copy)
        self.Bind(wx.EVT_MENU, self.edit_paste,           self.Paste)        
        self.Bind(wx.EVT_MENU, self.edit_delete,          self.Delete)
        self.Bind(wx.EVT_MENU, self.edit_goto,            self.GoTo)
        self.Bind(wx.EVT_MENU, self.edit_selectAll,       self.SelectAll)
        self.Bind(wx.EVT_MENU, self.edit_date_MDY,        self.Date_MDY)
        self.Bind(wx.EVT_MENU, self.edit_date_YMD,        self.Date_YMD)
        self.Bind(wx.EVT_MENU, self.edit_date_DMY,        self.Date_DMY)
        self.Bind(wx.EVT_MENU, self.edit_time24,          self.Time24)
        self.Bind(wx.EVT_MENU, self.edit_time12,          self.Time12)
        # Find Menu
        self.Bind(wx.EVT_MENU, self.OnShowFind,         self.Find)
        self.Bind(wx.EVT_MENU, self.OnShowFind,         self.FindNext)
        self.Bind(wx.EVT_MENU, self.OnShowFindReplace,  self.Replace)
        self.Bind(wx.EVT_MENU, self.OnShowLineNumbers,  self.LineNos)
        # Update UI
	self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu,  self.Find)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu,  self.FindNext)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateMenu,  self.Replace)
        # Format Menu
        self.Bind(wx.EVT_MENU, self.format_wordWrap, self.WordWrap)
        self.Bind(wx.EVT_MENU, self.format_font,     self.Font_)
        self.Bind(wx.EVT_MENU, self.format_toUpper, self.ToUpper)
        self.Bind(wx.EVT_MENU, self.format_toLower, self.ToLower)
        # View Menu
        self.Bind(wx.EVT_MENU, self.view_toolBar,       self.toolBar)
        self.Bind(wx.EVT_TOOL, self.file_new,           self.tnew)        
	self.Bind(wx.EVT_TOOL, self.file_open,          self.topen)
        self.Bind(wx.EVT_TOOL, self.file_save,          self.tsave)
        self.Bind(wx.EVT_TOOL, self.file_print,         self.tprint)
        self.Bind(wx.EVT_TOOL, self.file_printPreview,  self.tprintpre)
        self.Bind(wx.EVT_MENU, self.edit_cut,           self.tcut)
	self.Bind(wx.EVT_MENU, self.edit_copy,          self.tcopy)
        self.Bind(wx.EVT_MENU, self.edit_paste,         self.tpaste) 
	self.Bind(wx.EVT_MENU, self.edit_undo,          self.tundo)
	self.Bind(wx.EVT_MENU, self.edit_redo,          self.tredo)	
        self.Bind(wx.EVT_MENU, self.view_statusBar, self.statusBar)
        # Help Menu
        self.Bind(wx.EVT_MENU, self.help_topics,     self.Topics)        
        self.Bind(wx.EVT_MENU, self.help_about,      self.About)
        #
        self.edit_ctrl.Bind(wx.EVT_LEFT_UP,          self.OnLeftUp)
        self.edit_ctrl.Bind(wx.EVT_TEXT,             self.edit_select)  # for Selection      
        self.edit_ctrl.Bind(wx.EVT_CHAR,             self.OnKeyDown)    # for Status bar
        # File initialize
        self.filename=""
        # Printing initialize
        FONTSIZE = 10
        self.pdata = wx.PrintData()
	self.pdata.SetPaperId(wx.PAPER_LETTER)
	self.pdata.SetOrientation(wx.PORTRAIT)
        self.margins = (wx.Point(15,15), wx.Point(15,15))
        #Replace "Printer()" with below:
        self.html_printer =  wx.html.HtmlEasyPrinting("Printing", self)
        self.html_print = Printer()
        #Size up and Show
        self.Centre()
        self.SetSizer(sizer)
        self.Show() 
        
    def OnShowLineNumbers(self, event):
      if self.LineNos.IsChecked():
        value=self.edit_ctrl.GetValue()
        array=value.splitlines()
        newValue=""
        i=0
        for line in array[:] :
            LN=i+1
            line= '%5d %s' %  (LN, array[i])
            newValue = newValue + line+'\n'
            i += 1
        self.edit_ctrl.SetValue(newValue) 
      else:  
        value=self.edit_ctrl.GetValue()
        array=value.splitlines()
        newValue=""
        i=0
        for line in array[:] :
            line= line[6:]
            newValue = newValue + line+'\n'
            i += 1
        self.edit_ctrl.SetValue(newValue)        

    def edit_select(self, event):
        #  print "edit_select"
           self.Cut.Enable(True)
           self.Copy.Enable(True)
           self.Delete.Enable(True)
        
    def OnResetStatusBar(self, x, y):
           stats="  Ln "+str(y+1)+", Col "+str(x+1) 
           self.Statusbar.SetStatusText(stats, 1)
           self.Statusbar.Show()
        
    def OnLeftUp(self, event):
        if self.Statusbar.IsShown():
           (x, y) =  self.edit_ctrl.PositionToXY(self.edit_ctrl.GetInsertionPoint())
           self.OnResetStatusBar(x, y)
        if self.LineNos.IsChecked():
           (x, y) =  self.edit_ctrl.PositionToXY(self.edit_ctrl.GetInsertionPoint())
           if x<6 : 
              x=5
              y=-1
           self.OnResetStatusBar(x-6, y)
        self.Show()
        #event.Skip()    
        
    def OnKeyDown(self, event):
        #print "Key got pressed"
        key = event.GetKeyCode()
        if self.Statusbar.IsShown():
           (x, y) =  self.edit_ctrl.PositionToXY(self.edit_ctrl.GetInsertionPoint())
           if (key == 13):
               x=1      # 1
               y=y+1    # +1 
               self.OnResetStatusBar(x, y)  
        if (self.LineNos.IsChecked()):
           if (key == 13):
               (x, y) =  self.edit_ctrl.PositionToXY(self.edit_ctrl.GetInsertionPoint())
               value=self.edit_ctrl.GetValue()
               array=value.splitlines()
               array[y]="      "+array[y]
               value="\n".join(array)  
               self.edit_ctrl.SetValue(value)  
               pos=self.edit_ctrl.XYToPosition(x+6, y)
               self.edit_ctrl.SetInsertionPoint(pos)
        self.Show()
        event.Skip()

    def colors(self):
        self.SetBackgroundColour(wx.NullColor)  # Sets canvas to WHITE (from grey)
        self.SetForegroundColour(wx.BLACK)  # Makes sure BLACK is Text colour
        self.fcurClr=self.edit_ctrl.GetForegroundColour()
        self.bcurClr=self.edit_ctrl.GetBackgroundColour()
        
    # Sets some initial properties of the frame
    def __set_properties(self):
        self.SetTitle("Untitled Notepad--")
        self.frame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frame_statusbar_fields = ["frame_statusbar"]
        for i in range(len(frame_statusbar_fields)):
            self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)

    # Performs layout of frame
    def __do_layout(self):
         sizer_1 = wx.BoxSizer(wx.VERTICAL)
         self.SetAutoLayout(True)
         self.SetSizer(sizer_1)   
        #sizer_1.Fit(self)           # Either of these seem to cause wx.Size
        #sizer_1.SetSizeHints(self)  # to minimize. Also "self.Fit()"
         self.Layout()
        
    # From the menu File/New clears the editing area and allows user to start over    
    def file_new(self, event): 
        # Editing Area
        wx.TextCtrl.Clear(self.edit_ctrl)
        (x, y) =  self.edit_ctrl.PositionToXY(self.edit_ctrl.GetInsertionPoint())
        self.OnResetStatusBar(x, y)  
        self.edit_ctrl.SetFocus() 
        self.Show()

    # From the menu File/Files uses dialog to open file previously used
    def file_file_1(self, event):
            self.filename = self.File_1.GetItemLabel()[3:]
            if (self.filename > ""):
               self.file_files(event)
               
    def file_file_2(self, event):
            self.filename = self.File_2.GetItemLabel()[3:]
            if (self.filename > ""):
               self.file_files(event)
               
    def file_file_3(self, event):
            self.filename = self.File_3.GetItemLabel()[3:]
            if (self.filename > ""):
               self.file_files(event)
               
    def file_file_4(self, event):
            self.filename = self.File_4.GetItemLabel()[3:]
            if (self.filename > ""):
               self.file_files(event)

    # From the files menu uses one of the stored files and opens it immediately
    def file_files(self, event):
                self.edit_ctrl.LoadFile(self.filename)
                self.SetTitle(self.filename +" - Notepad--") 
                NumLines=self.edit_ctrl.GetNumberOfLines()
                maxLength=NumLines*19
                self.edit_ctrl.SetMinSize((1000, maxLength))                
                self.edit_ctrl.SetFocus()
    
    # From the menu File/Open uses windows dialog to open a file selected by the user        
    def file_open(self, event):
            filters = 'Text files (*.txt)|*.txt|All files (*.*)|*.*'
            dialog = wx.FileDialog ( None, message = 'Open something...', wildcard = filters, style = wx.OPEN | wx.MULTIPLE )
            dialog.SetFilename(self.filename)
            if  dialog.ShowModal() == wx.ID_OK:
                self.filename = dialog.GetPath()
                self.edit_ctrl.LoadFile(self.filename)
                self.SetTitle(self.filename +" - Notepad--") 
                NumLines=self.edit_ctrl.GetNumberOfLines()
                maxLength=NumLines*19
                self.edit_ctrl.SetMinSize((1000, maxLength))                
                self.edit_ctrl.SetFocus()
                # Manage array of files
                if (    (self.File_1.GetItemLabel()[3:] == self.filename )
                    or  (self.File_2.GetItemLabel()[3:] == self.filename )
                    or  (self.File_3.GetItemLabel()[3:] == self.filename )
                    or  (self.File_4.GetItemLabel()[3:] == self.filename )):
                    pass
                else:
                    self.File_4.SetItemLabel("4. "+self.File_3.GetItemLabel()[3:])                   
                    self.File_3.SetItemLabel("3. "+self.File_2.GetItemLabel()[3:])
                    self.File_2.SetItemLabel("2. "+self.File_1.GetItemLabel()[3:])
                    self.File_1.SetItemLabel("1. "+self.filename)
                self.Show()
            else:
                #print 'Nothing was selected.'
                dialog.Destroy()
            dialog.Destroy()
            
    # From the File/Save menu lets user save a file using windows dialog
    def file_save(self, event): 
            dialog = wx.FileDialog ( None, defaultFile="*.txt",style = wx.SAVE| wx.OVERWRITE_PROMPT )
            # Show dialog & get input
            if dialog.ShowModal() == wx.ID_OK:
                file_path = dialog.GetPath()
                file = open(file_path,'w')
                file_content = self.edit_ctrl.GetValue()
                file.write(file_content)
                # Manage array of files
                if (    (self.File_1.GetItemLabel()[3:] == self.filename )
                    or  (self.File_2.GetItemLabel()[3:] == self.filename )
                    or  (self.File_3.GetItemLabel()[3:] == self.filename )
                    or  (self.File_4.GetItemLabel()[3:] == self.filename )):
                    pass
                else:
                    self.File_4.SetItemLabel("4. "+self.File_3.GetItemLabel()[3:])                   
                    self.File_3.SetItemLabel("3. "+self.File_2.GetItemLabel()[3:])
                    self.File_2.SetItemLabel("2. "+self.File_1.GetItemLabel()[3:])
                    self.File_1.SetItemLabel("1. "+self.filename)
                self.File_1.SetItemLabel("1. "+file_path)                
            self.SetStatusText("Your file has been saved")        
            dialog.Destroy()
            
    # From the File/Rename menu lets user rename/move a file using input dialog            
    def file_rename(self, event):
        dialog = InputDialog(self,"Rename/Move: "+self.filename,"Enter New Name:")
        dialog.SetSize((400, -1))
        dialog.input.SetInitialSize((350, -1))
        #dialog.input.SetValue(self.filename)   #This seems to change the Keyboard to Hebrew
        dialog.input.SetFocus()
        try:
            if dialog.ShowModal() == wx.ID_OK:      
                rename = dialog.GetValue()
                rename = rename[string.rfind(rename,'\\')+1:]
                os.system("RENAME "+self.filename+" "+rename)
                self.filename = \
                   self.filename[:string.rfind(self.filename,'\\')+1]+rename
                self.File_1.SetItemLabel("1. "+self.filename)
                self.SetTitle(self.filename +" - Notepad--") 
        finally:
            dialog.Destroy()    
         
    def GetHtmlText(self,text):
	"Simple conversion of text.  Use a more powerful version"
	text = '<pre>' + text + '</pre>' # Preserve spacing
	html_text = text.replace('\n\n','<P>')     # Paragraphs
	html_text = text.replace('\n', '<BR>')     # Line breaks
        return html_text 
        
    # From the Menu "File/Page Setup" allows user to make changes in printer settings
    def file_pageSetup(self, event):
        self.html_printer.PageSetup()
        
    # From the Menu "File/Print Preview" shows how text prints before printing
    def file_printPreview(self, event):
        global frame
        text = self.edit_ctrl.GetValue()
        doc_name= self.filename
        self.html_printer.PreviewText(self.GetHtmlText(text), doc_name)

    # From the Menu "File/Print"  actually prints the text to the printer     
    def file_print(self, event):
        global frame
        text = self.edit_ctrl.GetValue()
        doc_name=self.filename
        self.html_print.Print(self.GetHtmlText(text), doc_name)    

    def GetErrorText():
       "Put your error text logic here.  See Python Cookbook for a useful example of error text."
       return "Some error occurred."
        
    # From the Menu File/Exit closes the app (same as [X] in upper right of frame)   
    def file_exit(self, event):
        alert = wx.MessageDialog(self, "The text in the Untitled file has changed.\n"
                                      +"\nDo you want to save the changes?",
                'Question', wx.YES_NO|wx.NO_DEFAULT |wx.CANCEL|wx.ICON_EXCLAMATION)
        response = alert.ShowModal()
        alert.Destroy()  
        if response == wx.ID_YES:
	    #print "The user clicked the 'YES' button."
	    if (self.filename > ""):
	       file = open(self.filename,'w')
	       file_content = self.edit_ctrl.GetValue()
               file.write(file_content)
            else:
               self.filename='Untitled.txt'
	       file = open(self.filename,'w')
	       file_content = self.edit_ctrl.GetValue()
               file.write(file_content)
        else:
            #print "The user clicked the 'NO' button."
            pass
        self.Destroy() 
            
        #alert = wx.MessageDialog(self, "Do you really want to quit")
        #response = alert.ShowModal()
        #alert.Destroy()
        #if response == wx.ID_OK:
            #print "The user clicked the 'OK' button."
            #self.Destroy()            
        #else:
            #print "The user clicked the 'Cancel' button."
            #event.Skip()

    # From the Menu Edit/Undo brings the app to a state before the last event
    def edit_undo(self, event):
        if self.edit_ctrl.CanUndo():
           self.edit_ctrl.Undo()
           #self.edit_select(self)
        else:
           #print "Can NOT Undo"
           event.Skip()
              
    # From the Menu Edit/Redo brings the app to a state before the last Undo
    def edit_redo(self, event):
        if self.edit_ctrl.CanRedo():
           self.edit_ctrl.Redo()
           #self.edit_select(self)
        else:
           #print "Can NOT Redo"
           event.Skip()
           
    # From the Menu Edit/Cut deletes the selected text from the frame and places it
    # on the clipboard
    def edit_cut(self, event):
        if self.edit_ctrl.CanCut():
           self.edit_ctrl.Cut()
           #self.edit_select(self)           
        else:
           event.Skip()
   
    # From the Menu Edit/Copy copies the selected text and places it on the clipboard
    def edit_copy(self, event):
        if self.edit_ctrl.CanCopy():    
           self.edit_ctrl.Copy()
        else:
           event.Skip()

    # From the Menu Edit/Paste copies the content (text) from the clipboard to the frame
    def edit_paste(self, event):
        if self.edit_ctrl.CanPaste():      
           self.edit_ctrl.Paste()
           #self.edit_select(self)
        else:
           event.Skip()

    # From the Menu Edit/Delete deletes the selected text from the frame and places it
    # on the clipboard
    def edit_delete(self, event):
        if self.edit_ctrl.CanCut():        
           self.edit_ctrl.Cut()
           #self.edit_select(self)
        else:
           event.Skip()  
           
    def BindFindEvents(self, win):
        win.Bind(wx.EVT_FIND, self.OnFind)
        win.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        win.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)           
           
    def EnableButtons(self):
        self.Find.Enable(True)
        self.FindNext.Enable(True)
        self.Replace.Enable(True)

    def DisableButtons(self):
        self.Find.Enable(False)
        self.FindNext.Enable(False)        
        self.Replace.Enable(False)           

    # From the Menu Edit/Find will find the next occurance of a text string
    # and highlight it
    def OnShowFind(self, event):
        self.b=0
        self.offset=0
        self.to=0
        self.DisableButtons()
        self.edit_ctrl.SetFocus()
        dlg = wx.FindReplaceDialog(self, self.findData, "Find")
        self.BindFindEvents(dlg)
        dlg.Show(True)

    # From the Menu Edit/Replace will replace the next occurrance of a text string
    # with the replacement test string
    def OnShowFindReplace(self, event):
        self.b=0
        self.offset=0
        self.to=0
        self.DisableButtons()
        dlg = wx.FindReplaceDialog(self, self.findData, "Find & Replace", wx.FR_REPLACEDIALOG)
        self.BindFindEvents(dlg)
        dlg.Show(True)

    def OnFind(self, event):
        #print repr(event.GetFindString()), repr(self.findData.GetFindString())
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }
        et = event.GetEventType()
        if et in map:
            eventType = map[et]
        else:
            eventType = "**Unknown Event Type**"
        e = event.GetFlags() # for wx.FR_MATCHCASE, wx.FR_WHOLEWORD, wx.FR_DOWN

        if et in [wx.wxEVT_COMMAND_FIND, wx.wxEVT_COMMAND_FIND_NEXT]:
            replaceText=""
            self.b = self.offset + self.to
            searchText = event.GetFindString()
            self.to = len(searchText)
            fieldText = self.edit_ctrl.GetValue()
            if (e == (e & ~wx.FR_MATCHCASE)):          # Actually  is IGNORECASE
               searchText = searchText.lower() 
               fieldText  =  fieldText.lower() 
            endText = fieldText[self.b :]
            self.offset = endText.find(searchText)
            regexText=""
            if (e ==(e & ~wx.FR_WHOLEWORD)):           # Actually is a NOT WHOLEWORD ONLY
               regexText = searchText
            else:   
               regexText = r'\b'+ searchText + r'\b'
            if (e == (e & ~wx.FR_MATCHCASE)):            
               M=re.search(regexText, endText, re.IGNORECASE)
            else:
               M=re.search(regexText, endText)         #  MATCHES CASE  
               
            if M:
               self.offset = max(self.offset, M.start())
            if ((self.offset != -1)  and (self.offset == M.start())): 
               self.offset += self.b
               # find apparently doesn't count newlines in its total 
               # Trick here is the extra '\r' in Windows
               self.offset += fieldText.count('\r\n', 0, self.offset) 
               self.edit_ctrl.SetSelection(self.offset, self.offset + self.to) 
               self.edit_ctrl.SetFocus()
            else:
               wx.Bell()
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE, wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
          searchText = event.GetFindString()
          replaceText = event.GetReplaceString()
          if (replaceText =="" ):
                dlg = wx.MessageDialog(self, "Please enter a Replacement Text.",
                              "Replace with", wx.OK | wx.ICON_INFORMATION)
                click=dlg.ShowModal()
                if (click == wx.ID_OK):
                    replaceText = event.GetReplaceString()
                dlg.Destroy()
          else:     
            fieldText = self.edit_ctrl.GetValue()
            self.to = len(searchText)
            wholeText = self.edit_ctrl.GetValue()
            if (e == (e & ~wx.FR_MATCHCASE)):              # That is IGNORECASE
               searchText = event.GetFindString().lower() 
               fieldText = self.edit_ctrl.GetValue().lower()
            endText=fieldText[self.b :]
            self.offset = endText.find(searchText) 
            regexText=searchText
            if (e ==(e & ~wx.FR_WHOLEWORD)):               # Actually is a NOT WHOLEWORD ONLY 
	       regexText = searchText
	    else:   
	       regexText = r'\b'+searchText+ r'\b'
            if (e == (e & ~wx.FR_MATCHCASE)):            
               M=re.search(regexText, endText, re.I)       #  IGNORES CASE
            else:
               M=re.search(regexText, endText)             #  MATCHES CASE  

            if M:
               self.offset = max(self.offset, M.start())
            if ((self.offset != -1)  and (self.offset == M.start())): 
               self.offset += self.b
               self.offset += fieldText.count('\r\n', 0, self.offset) 
               fieldText = wholeText[0:self.offset] + replaceText + wholeText[self.offset + self.to:]
               self.edit_ctrl.SetValue(fieldText)
               
               if et in [wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
                   text = self.edit_ctrl.GetValue()
                   if (e == (e & ~wx.FR_MATCHCASE)):        # That is IGNORECASE
                      newText=re.sub(regexText, replaceText, text, 0 ,re.I) #Replaces All
                   else:
                      newText=re.sub(regexText, replaceText, text, 0)
                   self.edit_ctrl.SetValue(newText)
               else:
                   self.edit_ctrl.SetFocus()
            else:
                 self.edit_ctrl.SetFocus()
        else:
            self.edit_ctrl.SetFocus()
        #print("%s -- Find text: %s  %s  Flags: %d  \n" %
        #              (eventType, event.GetFindString(), replaceText, event.GetFlags()))


    def OnFindClose(self, event):
        self.log.write("FindReplaceDialog closing...\n")
        event.GetDialog().Destroy()
        self.b=0
	self.offset=0
        self.to=0
        self.EnableButtons()

    # From the Menu "Edit/Go To" will go to the line number entered
    def edit_goto(self, event):
        """Get response from the user using a dialog box."""
        dialog = InputDialog(None,'GoTo Line Number',"Enter Line Number to Go To:")
        dialog.SetMinSize((50, -1))
        dialog.input.SetFocus()
        NumLines=self.edit_ctrl.GetNumberOfLines()
        line=str(NumLines)
        try:
            if dialog.ShowModal() == wx.ID_OK:      
                line = dialog.GetValue()
                goto = min(NumLines, int(line) )
                line = str(goto)
        finally:
            dialog.Destroy()

        M = re.search(r'^\d+$',line)                #Number must be numeric
        if M :    
            x=0
            y=long(line)
            self.edit_ctrl.SetFocus()
            pos=self.edit_ctrl.XYToPosition(x, y-1) 
            self.edit_ctrl.SetInsertionPoint(pos)
            self.OnResetStatusBar(x, y-1)
        else:
           line="0"
        return line

    # From the Menu "Edit/Select All" selects the entire contents of the frame
    # and highlights it
    def edit_selectAll(self, event):
        #if self.edit_ctrl.CanUndo():
           self.edit_ctrl.SelectAll()

    # MDY From the Menu Edit/Time/Date will insert today's current Time and Date in the frame
    def edit_date_MDY(self, event):
        """Get response from the user using a dialog box."""
        dialog = DateDialog(None,'Select a Date Format',"Select a Date Format:",'MDY',self.config_Dates)
        try:
            if dialog.ShowModal() == wx.ID_OK:  
               self.edit_ctrl.WriteText(dialog.example.GetValue()) # places date on canvas
               self.config_Dates['MDY']=dialog.config_Date
               #print self.config_Dates['MDY']
        finally:
            dialog.Destroy()
    # YMD        
    def edit_date_YMD(self, event):
        """Get response from the user using a dialog box."""
        dialog = DateDialog(None,'Select a Date Format',"Select a Date Format:",'YMD',self.config_Dates)
        try:
            if dialog.ShowModal() == wx.ID_OK:  
               self.edit_ctrl.WriteText(dialog.example.GetValue()) # places date on canvas
               self.config_Dates['YMD']=dialog.config_Date 
               #print self.config_Dates['YMD']
        finally:
            dialog.Destroy()
    # DMY         
    def edit_date_DMY(self, event):
        """Get response from the user using a dialog box."""
        dialog = DateDialog(None,'Select a Date Format',"Select a Date Format:",'DMY',self.config_Dates)
        try:
            if dialog.ShowModal() == wx.ID_OK:  
               self.edit_ctrl.WriteText(dialog.example.GetValue()) # places date on canvas
               self.config_Dates['DMY']=dialog.config_Date
               #print self.config_Dates['DMY']
        finally:
            dialog.Destroy()
            
    # Time 24Hr       
    def edit_time24(self, event):

           timeStamp = time.strftime("%H:%M:%S ", time.localtime()).lstrip("0")
           self.edit_ctrl.WriteText(timeStamp)

    # Time 12Hr        
    def edit_time12(self, event):

           timeStamp = time.strftime("%I:%M:%S %p ", time.localtime()).lstrip("0")
           self.edit_ctrl.WriteText(timeStamp)

    # From the Menu "Format/Word Wrap" toggles between delimiting lines by linefeeds
    # and inserting linefeeds at the screen widths if a word does not fit
    def format_wordWrap(self, event):
            '''Turn wrapping on or off in the text control'''
            global frame

            if self.WordWrap.IsChecked():
                self.oldcontents=self.edit_ctrl.GetValue()
                sz = frame.GetSize()
                contents=self.edit_ctrl.GetValue()
                array=contents.splitlines()
                self.maxLength=0
                for line in array[:]:
                  self.maxLength=max(self.maxLength,len(line))
                contents=self.wrap(contents, sz.width/10)
                self.edit_ctrl.SetValue(contents)
                self.OnResetStatusBar(0, 0)
                self.Show
       
            else:            
                self.edit_ctrl.SetValue(self.oldcontents)
                self.OnResetStatusBar(0, 0)
                self.Show()
                
    def wrap(self,text, width):
       """
       A word-wrap function that preserves existing line breaks
       and most spaces in the text. Expects that existing line
       breaks are linux style newlines (\n).
       """
       def func(line, word):
          nextword = word.split("\n", 1)[0]
          n = len(line) - line.rfind('\n') - 1 + len(nextword)
          if n >= width:
            sep = "\n"
          else:
            sep = " "
          return '%s%s%s' % (line, sep, word)
          
       text = text.split(" ")
       while len(text) > 1:
          text[0] = func(text.pop(0), text[0])
       return text[0]

    # From the Menu Format/Font allows user to select a custom font for thr Notepad
    def format_font(self, event):
	self.curFont = self.edit_ctrl.GetFont()
        self.curFClr  = wx.BLACK
        
        data = wx.FontData()
	data.EnableEffects(True)
	data.SetColour(self.curFClr)
	data.SetInitialFont(self.curFont)
        dialog = wx.FontDialog(self, data)
	if dialog.ShowModal() == wx.ID_OK:
	    data = dialog.GetFontData()
	    font = data.GetChosenFont()
	    style= font.GetStyleString()
	    colour = data.GetColour()
	    fontSize = font.GetPointSize()
	    #print 'You selected: "%s", %d points\n' % (font.GetFaceName(), font.GetPointSize())
            self.curFont = font
            self.curPointSize = fontSize
            self.curFont.SetPointSize(self.curPointSize)
            self.edit_ctrl.SetFont(self.curFont)
            self.curFClr = colour
            self.edit_ctrl.SetForegroundColour(self.curFClr)            
            self.curPointSize = fontSize
            self.curFont.SetPointSize(self.curPointSize)
            self.edit_ctrl.SetStyle(0, 0, style=(wx.TextAttr(wx.RED)))
        dialog.Destroy()
        
# From the Menu "Format/Convert/To Upper" allows user to UpperCase a selection of characters
    def format_toUpper(self, event):  
        if self.edit_ctrl.CanCut():    
           (f, t) = self.edit_ctrl.GetSelection()
           str = self.edit_ctrl.GetStringSelection().upper()
	   self.edit_ctrl.Replace(f,t,str)
           self.edit_ctrl.SetSelection(f, t)
        else:
           event.Skip()        
        
# From the Menu "Format/Convert/To Lower" allows user to LowerCase a selection of characters
    def format_toLower(self, event):
        if self.edit_ctrl.CanCut():
           (f, t) = self.edit_ctrl.GetSelection()
           str = self.edit_ctrl.GetStringSelection().lower()
	   self.edit_ctrl.Replace(f,t,str)
           self.edit_ctrl.SetSelection(f, t)
        else:
           event.Skip()        
        
    def OnUpdateMenu(self, event):
        """Update menu items based on current status and context."""
        v = self.edit_ctrl.GetValue()
	self.edit_ctrl.SetFont(self.curFont)
        self.edit_ctrl.SetForegroundColour(self.fcurClr)
        self.edit_ctrl.SetBackgroundColour(self.bcurClr)
        win = wx.Window.FindFocus()
        id = event.GetId()
        event.Enable(True)
        try:
           x=0
           #if id == self.LineNos:
           #    event.Check(win.lineNumbers)     
           #else:
           #    event.Enable(False)
        except AttributeError:
                # This menu option is not supported in the current context.
                event.Enable(False)
                
    # From the Menu "View/Toolbar" toggles between showing and hiding the Toolbar
    def view_toolBar(self, event):
        if self.toolBar.IsChecked():
             self.sizeH+=self.toolbarH            
             self.Toolbar.Show()
        else:
             self.sizeH-=self.toolbarH 
             self.Toolbar.Hide()
        self.SetSize((-1,self.sizeH))         
                
    # From the Menu "View/Status Bar" toggles between showing and hiding the Status Bar
    def view_statusBar(self, event):
        if self.Statusbar.IsShown():
           event.Skip
           #print "Hide Status Bar"        
           self.Statusbar.Hide()
           #evt = wx.SizeEvent(self.GetSize()) 
           #self.GetEventHandler().ProcessEvent( evt) 
           self.Show()
        else:
           # Status Bar Not Shown
           event.Skip
           #print "Show Status Bar"
           (x, y) =  self.edit_ctrl.PositionToXY(self.edit_ctrl.GetInsertionPoint())
           self.OnResetStatusBar(x, y)
    
    # Future enhancement will display a .chm Help file        
    #def help(self, evt):
         #helpFile = os.path.join('docs', 'Notepad--.chm')
         #os.startfile(helpFile) 
       
    # From the Menu Help/Topics asks if user wishes to see Help Topics       
    def help_topics(self,event): 
        text="<b>Notepad--</b> Version "+VERSION+" <br>\
<pre>       Help Topics:<br>\
               File commands<br>\
               Edit commands<br>\
               Format commands<br>\
               View commands<br>\
               Help commands<pr></pre>"
        frm = MyHtmlFrame(None,'Topics', text)
        frm.Show()
    
    # From the Menu Help/About shows Version number and Copyright info for app         
    def help_about(self,event):
        text="<b>Notepad--</b> Version "+VERSION+" <br> \
                     Copyright 2013, Robin Randall All rights reserved"
        frm = MyHtmlFrame(None,'About Notepad--', text)
        frm.Show()
        
    def OnClose(self, event):  # Overrides wxFrame builtin "Close" event action
        self.file_exit(event)
        
class Printer(HtmlEasyPrinting):
         def __init__(self):
             global frame
             HtmlEasyPrinting.__init__(self,name="Printing", parentWindow=None)

         def PreviewText(self, text, doc_name):
             self.SetHeader(doc_name)
             HtmlEasyPrinting.PreviewText(self, text)    
    
         def Print(self, text, doc_name):
             self.SetHeader(doc_name)
             self.PrintText(text, doc_name)

# This class is used in Help/About and other similar needs
class MyHtmlFrame(wx.Frame):
    def __init__(self,parent, title, text ):
        wx.Frame.__init__(self, parent, -1, title)
        html = wx.html.HtmlWindow(self)
        _icon = wx.Icon("C:\\K\\notepad--.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(_icon)
        html.SetPage(text)
                     
class InputDialog(wx.Dialog):   # To be used as a flexible template for various input dialogs
    def __init__(self, parent, title, caption):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(InputDialog, self).__init__(parent, wx.ID_ANY, title, style=style)
        text = wx.StaticText(self, wx.ID_ANY, caption)
        input = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_RICH2|wx.SUNKEN_BORDER)
        input.SetInitialSize((50, wx.ID_ANY))
        buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        input.SetMinSize((50,-1))
        sizer.Add(text, 0, wx.ALL, 5)
        sizer.Add(input, 1, wx.ALIGN_LEFT|wx.ALL, 10)
        sizer.Add(buttons, 0,wx.ALL, 10)
        self.SetSizerAndFit(sizer)
        self.input = input
        
    def SetValue(self, value):
        self.input.SetValue(value)
        
    def GetValue(self):
        return self.input.GetValue() 
        
        
class MyNotepad(wx.App):
    def OnInit(self):
        global frame
        provider = wx.SimpleHelpProvider()
        wx.HelpProvider.Set(provider)
        wx.InitAllImageHandlers()
        win_id= wx.NewId()
        frame = MyFrame()
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyNotepad(False)
    CRU='(C) 2013'
    VERSION="2.0" 
    print ("Notepad-- %s Ver."% CRU + VERSION)
    timeStamp = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
    print timeStamp
    app.MainLoop()
