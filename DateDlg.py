#!/usr/bin/env python
import time
import wx
import os, sys
#
class DateDialog(wx.Dialog):   # To be used as a flexible template for various dialogs
    def __init__(self, parent, title, caption, type, config): # type is in set ['MDY',YMD','DMY']
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(DateDialog, self).__init__(parent, wx.ID_ANY, title, style=style)
        # M-D-Y
        #
        self.type = type.upper()
        self.config = config
        self.wdays =                     {'Weekday':'%A','Wdy':'%a','Wd':'%a','w':'%w'}
        self.wday_idx = 0         # = 'Weekday' 0=Sunday
        self.wday_max = len(self.wdays) -1
        self.wday_delims =               {'/':'/','_':'_','-':'-',' ':' ','|':'|',',':', ','.':'.'}
        self.wday_delim_idx = 0   # = '/'
        self.wday_delim_max = len(self.wday_delims) -1
        self.months=                     {'Month':'%B','Mon':'%b','mm':'%m','m':'^%m'}
        self.month_idx = 2        # = 'mm'
        self.month_max = len(self.months) -1     
        self.month_delims=               {'/':'/','_':'_','-':'-',' ':' ','|':'|',',':', ','.':'.'}
        self.month_delim_idx = 0  # = '/'
        self.month_delim_max = len(self.month_delims) -1        
        self.doms  =                     {'dd':'%d','d':'^%d'}
        self.dom_idx = 0          # = 'dd'
        self.dom_max = len(self.doms) -1      
        self.dom_delims  =               {'/':'/','_':'_','-':'-',' ':' ','|':'|',',':', ','.':'.'}
        self.dom_delim_idx = 0    # = '/'
        self.dom_delim_max = len(self.dom_delims)  -1      
        self.years =                     {'yyyy':'%Y','yy':'%y','y':'^%y'}
        self.year_idx = 1         # = 'yy'
        self.year_max = len(self.years) -1 
        self.year_delims =               {'/':'/','_':'_','-':'-',' ':' ','|':'|',',':', ','.':'.'}
        self.year_delim_idx = 3   # = ' '
        self.year_delim_max = len(self.year_delims) -1         
                
        # Construct all the Date and Time fields
        self.DateTime_Title = wx.StaticText(self, -1,"Time Formatter", size=(200, -1))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.DateTime_Title.SetFont(font)
        self.buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        self.reset = wx.Button(self, id=-1, label='Reset', size=(75, 23))
        self.reset.Bind(wx.EVT_BUTTON, self.onReset)
        self.config_date    = ""
        self.example        = wx.TextCtrl(self, value=self.config_date, size=(200, -1))
        self.check_wday     = wx.CheckBox(self, wx.ID_ANY, label="")
        self.check_wday.SetValue(True)
        self.wday           = wx.TextCtrl(self, value='Weekday', size=(70,-1))
        self.wday_sb        = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)
        self.wday_delim     = wx.TextCtrl(self, value=',',  size=(20,-1))
        self.wday_delim_sb  = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)
        self.month          = wx.TextCtrl(self, value='mm', size=(50,-1))
        self.month_sb       = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)
        self.month_delim    = wx.TextCtrl(self, value='/',  size=(20,-1))
        self.month_delim_sb = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)            
        self.dom            = wx.TextCtrl(self, value='dd', size=(30,-1))
        self.dom_sb         = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)
        self.dom_delim      = wx.TextCtrl(self, value='/',  size=(20,-1))
        self.dom_delim_sb   = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)
        self.year           = wx.TextCtrl(self, value='yy', size=(40,-1))
        self.year_sb        = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)
        self.year_delim     = wx.TextCtrl(self, value='/',  size=(20,-1))
        self.year_delim_sb  = wx.SpinButton(self,wx.ID_ANY, style=wx.SP_VERTICAL|wx.SP_WRAP)

        # Set event Bindings
        self.Bind(wx.EVT_CHECKBOX,  self.OnCheck,               self.check_wday) 
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_wday,         self.wday_sb )
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_wday_delim,   self.wday_delim_sb )	
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_month,        self.month_sb )	
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_month_delim,  self.month_delim_sb )	
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_dom,          self.dom_sb )
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_dom_delim,    self.dom_delim_sb )
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_year,         self.year_sb )
        self.Bind(wx.EVT_SPIN_UP,   self.OnSpinUp_year_delim,   self.year_delim_sb )	
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_wday,       self.wday_sb )
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_wday_delim, self.wday_delim_sb )	
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_month,      self.month_sb )	
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_month_delim,self.month_delim_sb )	
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_dom,        self.dom_sb )
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_dom_delim,  self.dom_delim_sb )
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_year,       self.year_sb )
        self.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown_year_delim, self.year_delim_sb )	
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.wday_sb )
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.wday_delim_sb )	
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.month_sb )	
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.month_delim_sb )	
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.dom_sb )
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.dom_delim_sb )
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.year_sb )
        self.Bind(wx.EVT_SPIN,      self.OnSpin,                self.year_delim_sb )

	
        
        if   (self.type == 'MDY'):
            self.changeDateFormat("CWMDY")    # Should build "[v]+Weekday+MM+DD+YY"
           
        elif (self.type == 'YMD'):
            self.changeDateFormat("CWYMD")    # Should build "[v]+Weekday+YY+MM+DD"
           
        elif (self.type == 'DMY'):
            self.changeDateFormat("CWDMY")    # Should build "[v]+Weekday+DD+MM+YY"
    
    def onReset(self,event):
        self.wday.SetValue('Weekday')
        self.wday_idx=0
        self.wday_delim.SetValue(',')
        self.wday_idx=0
        if   (self.type == 'MDY'):
            self.config['MDY']='%A, %m/%d/%y '
            self.month.SetValue('mm')
            self.month_idx=2
            self.month_delim.SetValue('/')
            self.month_delim_idx=0
            self.dom.SetValue('dd')
            self.dom_idx=0
            self.dom_delim.SetValue('/')
            self.dom_delim_idx=0            
            self.year.SetValue('yy')
            self.year_idx=1
            self.year_delim.SetValue(' ')
            self.year_delim_idx=3            
           
        elif (self.type == 'YMD'):
            self.config['YMD']='%A, %y/%m/%d '
            self.year.SetValue('yy')
            self.year_idx=1
            self.year_delim.SetValue('/')
            self.year_delim_idx=0                                    
            self.month.SetValue('mm')
            self.month_idx=2
            self.month_delim.SetValue('/')
            self.month_delim_idx=0
            self.dom.SetValue('dd')
            self.dom_idx=0
            self.dom_delim.SetValue(' ')
            self.dom_delim_idx=3            
           
        elif (self.type == 'DMY'):
            self.config['DMY']='%A, %d/%m/%y '
            self.dom.SetValue('dd')
            self.dom_idx=0
            self.dom_delim.SetValue('/')
            self.dom_delim_idx=0                        
            self.month.SetValue('mm')
            self.month_idx=2
            self.month_delim.SetValue('/')
            self.month_delim_idx=0
            self.year.SetValue('yy')
            self.year_idx=1
            self.year_delim.SetValue(' ')
            self.year_delim_idx=3                        
   
        e = wx.EVT_SPIN
        self.OnSpin(e)
        self.Show()    
        
    #----------------------------------------------------------------------
    def changeDateFormat(self, date_format):
        """
        date_format could equal any of the following:
        CWMDY, CWYMD, or CWDMY or HmS
        """
        self.date_dict = {"C":[self.check_wday],
                          "W":[self.wday, self.wday_sb, self.wday_delim, self.wday_delim_sb],
                          "M":[self.month,self.month_sb,self.month_delim,self.month_delim_sb],
                          "D":[self.dom,  self.dom_sb,  self.dom_delim,  self.dom_delim_sb],
                          "Y":[self.year, self.year_sb, self.year_delim, self.year_delim_sb]}

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        for char in date_format:
           for widget in self.date_dict[char]:
              hsizer.Add(widget, 0, wx.ALL, 0)
              
        self.Layout()         
        vsizer.Add(hsizer, 0, wx.ALL, 0)
        h2sizer = wx.BoxSizer(wx.HORIZONTAL)
        h2sizer.Add(self.example, 0, wx.ALL, 0)
        h2sizer.Add(self.DateTime_Title, 0, wx.ALL, 0)
        vsizer.Add(h2sizer, 0 , wx.ALL, 0)
        h3sizer = wx.BoxSizer(wx.HORIZONTAL) 
        h3sizer.Add(self.buttons,0, wx.ALL, 10)
        h3sizer.Add(self.reset,0,wx.ALL, 10)
        vsizer.Add(h3sizer, 0 ,wx.ALL, 0)
        self.SetSizer(vsizer)
        self.Fit()
 
        if (self.type == "MDY"):
            self.DateTime_Title.SetLabel("         [Weekday]  MDY ")
            self.year_delim.SetValue(" ")
            self.year_delim.idx = 3
        elif (self.type == "DMY"):
            self.DateTime_Title.SetLabel("         [Weekday]  DMY ")
            self.year_delim.SetValue(" ")
            self.year_delim.idx = 3
        elif (self.type == "YMD"):
            self.DateTime_Title.SetLabel("         [Weekday]  YMD ")
            self.dom_delim.SetValue(" ")
            self.dom_delim.idx = 3 

        e = wx.EVT_SPIN
        self.OnSpin(e)
        self.Show()   

    # Below handles Up Arrow Events    
    def OnSpinUp_wday(self, event):
        self.wday_idx = self.wday_idx + 1
        if (self.wday_idx > self.wday_max):
            self.wday_idx = 0
        dForms=self.wdays.keys()
        self.wday.SetValue(dForms[self.wday_idx])
        
    def OnSpinUp_wday_delim(self, event):        
        self.wday_delim_idx = self.wday_delim_idx + 1
        if (self.wday_delim_idx > self.wday_delim_max):
            self.wday_delim_idx = 0        
        dForms=self.wday_delims.keys()
        self.wday_delim.SetValue(dForms[self.wday_delim_idx]) 
        
    def OnSpinUp_month(self, event):        
        self.month_idx = self.month_idx + 1
        if (self.month_idx > self.month_max):
            self.month_idx = 0        
        dForms=self.months.keys()
        self.month.SetValue(dForms[self.month_idx])    
        
    def OnSpinUp_month_delim(self, event):        
        self.month_delim_idx = self.month_delim_idx + 1 
        if (self.month_delim_idx > self.month_delim_max):
            self.month_delim_idx = 0        
        dForms=self.month_delims.keys()
        self.month_delim.SetValue(dForms[self.month_delim_idx]) 
        
    def OnSpinUp_dom(self, event):        
        self.dom_idx = self.dom_idx + 1
        if (self.dom_idx > self.dom_max):
            self.dom_idx = 0       
        dForms=self.doms.keys()
        self.dom.SetValue(dForms[self.dom_idx]) 
        
    def OnSpinUp_dom_delim(self, event):        
        self.dom_delim_idx = self.dom_delim_idx + 1 
        if (self.dom_delim_idx > self.dom_delim_max):
            self.dom_delim_idx = 0       
        dForms=self.dom_delims.keys()
        self.dom_delim.SetValue(dForms[self.dom_delim_idx])  
        
    def OnSpinUp_year(self, event):        
        self.year_idx = self.year_idx + 1  
        if (self.year_idx > self.year_max):
            self.year_idx = 0
        dForms=self.years.keys()
        self.year.SetValue(dForms[self.year_idx]) 
        
    def OnSpinUp_year_delim(self, event):
        self.year_delim_idx = self.year_delim_idx + 1 
        if (self.year_delim_idx > self.year_delim_max):
            self.year_delim_idx = 0
        dForms=self.year_delims.keys()
        self.year_delim.SetValue(dForms[self.year_delim_idx])  
       
     # This handles Down Arrow events
    def OnSpinDown_wday(self, event):
        self.wday_idx = self.wday_idx - 1
        if (self.wday_idx < 0):
            self.wday_idx = self.wday_max
        dForms=self.wdays.keys()
        self.wday.SetValue(dForms[self.wday_idx])
        
    def OnSpinDown_wday_delim(self, event):
        self.wday_delim_idx = self.wday_delim_idx - 1
        if (self.wday_delim_idx < 0):
            self.wday_delim_idx = self.wday_delim_max
        dForms=self.wday_delims.keys()
        self.wday_delim.SetValue(dForms[self.wday_delim_idx]) 
        
    def OnSpinDown_month(self, event):
        self.month_idx = self.month_idx - 1
        if (self.month_idx < 0):
            self.month_idx = self.month_max
        dForms=self.months.keys()
        self.month.SetValue(dForms[self.month_idx])
        
    def OnSpinDown_month_delim(self, event):
        self.month_delim_idx = self.month_delim_idx - 1
        if (self.month_delim_idx < 0):
            self.month_delim_idx = self.month_delim_max 
        dForms=self.month_delims.keys()
        self.month_delim.SetValue(dForms[self.month_delim_idx])
        
    def OnSpinDown_dom(self, event):
        self.dom_idx = self.dom_idx - 1
        if (self.dom_idx < 0):
            self.dom_idx = self.dom_max
        dForms=self.doms.keys()
        self.dom.SetValue(dForms[self.dom_idx])
        
    def OnSpinDown_dom_delim(self, event):
        self.dom_delim_idx = self.dom_delim_idx - 1
        if (self.dom_delim_idx < 0):
            self.dom_delim_idx = self.dom_delim_max
        dForms=self.dom_delims.keys()
        self.dom_delim.SetValue(dForms[self.dom_delim_idx])
        
    def OnSpinDown_year(self, event):
        self.year_idx = self.year_idx - 1
        if (self.year_idx < 0):
            self.year_idx = self.year_max
        dForms=self.years.keys()
        self.year.SetValue(dForms[self.year_idx])
        
    def OnSpinDown_year_delim(self, event):
        self.year_delim_idx = self.year_delim_idx - 1
        if (self.year_delim_idx < 0):
            self.year_delim_idx = self.year_delim_max
        dForms=self.year_delims.keys()
        self.year_delim.SetValue(dForms[self.year_delim_idx]) 
        
    def OnSpin(self, event):
        if (self.type == "MDY"):
           config_DATE = \
           self.months[self.month.GetValue()]             + \           self.month_delims[self.month_delim.GetValue()] + \
           self.doms[self.dom.GetValue()]                 + \
           self.dom_delims[self.dom_delim.GetValue()]     + \
           self.years[self.year.GetValue()]               + \
           self.year_delims[self.year_delim.GetValue()]

        elif (self.type == "YMD"):
           config_DATE = \
           self.years[self.year.GetValue()]               + \
           self.year_delims[self.year_delim.GetValue()]   + \
           self.months[self.month.GetValue()]             + \           self.month_delims[self.month_delim.GetValue()] + \
           self.doms[self.dom.GetValue()]                 + \
           self.dom_delims[self.dom_delim.GetValue()]
 
        elif (self.type == "DMY"):
           config_DATE = \
           self.doms[self.dom.GetValue()]                 + \
           self.dom_delims[self.dom_delim.GetValue()]     + \
           self.months[self.month.GetValue()]             + \           self.month_delims[self.month_delim.GetValue()] + \
           self.years[self.year.GetValue()]               + \
           self.year_delims[self.year_delim.GetValue()]
           
        if (self.check_wday.IsChecked()):                        #Add the Weekday if user has checked the box
           config_DATE = self.wdays[self.wday.GetValue()] + \
           self.wday_delims[self.wday_delim.GetValue()]   + \
           config_DATE
           
        if  (self.type == "MDY"):              # Set Saved Config if default
           if (config_DATE == '%A, %m/%d/%y '):
               config_DATE = self.config['MDY']
        if  (self.type == "YMD"):
           if (config_DATE == '%A, %y/%m/%d '):
               config_DATE = self.config['YMD']
        if  (self.type == "DMY"):
           if (config_DATE == '%A, %d/%m/%y '):
               config_DATE = self.config['DMY']
        
        self.config_Date = config_DATE
        #Use strftime to format the date/time field according to its formatting rules (See strftime reference)
        self.config_date = time.strftime(config_DATE, time.localtime()).replace('^0','').replace('^','')
        if (self.check_wday.IsChecked()):
            if (self.wday.GetValue() == 'Wd'):                  #Allow for 2-char Weekday Abbrev.
                   self.config_date=self.config_date[:2] + self.config_date[3:]
        self.example.SetValue(self.config_date)
        self.Show()
        
    def OnCheck(self,event):
        if (self.check_wday.IsChecked()):
            self.wday.Enable(True)
            self.wday_delim.Enable(True)
            self.wday_sb.Enable(True)
            self.wday_delim_sb.Enable(True)
        else:    
            self.wday.Enable(False)
            self.wday_delim.Enable(False)
            self.wday_sb.Enable(False)
            self.wday_delim_sb.Enable(False)
        e = wx.EVT_SPIN
        self.OnSpin(e)
        self.Show()
        
if __name__ == "__main__":
    app = wx.App(False)
    dialog = DateTimeDialog(None, "Test", "This is a test", sys.argv[1]), ""
    dialog.ShowModal()
    dialog.Destroy()
    app.MainLoop()