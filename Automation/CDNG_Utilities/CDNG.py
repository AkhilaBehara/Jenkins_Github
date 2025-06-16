#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: CDNG.py
#
#   Description: This module contains helper classes and functions to utilize an API to ControlDeskNG 
#   Input :- 	  1.  
#   Conditions :- 1. 
#                 2. 
#                 3. 
#
#   Author: Mohamed Elbasiony - ZF Friedrichshafen AG, initial version was delivered by SimonB - dSPACE 
#=======================================================================================================


from win32com.client import DispatchEx, Dispatch
from Logging.Logger import LogBase
from  ExcelUtilities import XlsUtilities
import os
from dspace.com import Enums
from pywintypes import com_error
import exceptions

#-------------------------------------------------------------------------------------------------
# CDNGAccess Class
#-------------------------------------------------------------------------------------------------
class CDNGAccess(LogBase):
    ## On creation, get an Excel instance, if filename is given, load the related document
    def __init__(self):
        """Constructor(Filename)
        Creates a new instance of CDNGAccess
        """
        LogBase.__init__(self)
        self.ControlDeskApplication = None
        self.Enums = None
        self.ActiveProject = None
        self.ActiveExperiment = None
        self.LogDebug("Creating new CDNG instance...", self)
        self.XCP  = None

    def __str__(self):
        return "CDNGAccess"
#-------------------------------------------------------------------------------------------------
# Public methods
#-------------------------------------------------------------------------------------------------

    def Start(self):
        self.ControlDeskApplication = Dispatch("ControlDeskNG.Application.12")
        self.LogDebug("Openining CDNG Application...", self)
        self.Enums = Enums(self.ControlDeskApplication)
        
    def OpenProjectAndActivateExperiment(self, ProjectFileName, ExperimentIdx = 0 ):
        """
        """
        try:
            if not os.path.isabs(ProjectFileName):
                ProjectFileName = os.path.abspath(ProjectFileName)
            self.LogDebug("Open project %s..." %ProjectFileName, self)
            self.ActiveProject = self.ControlDeskApplication.OpenProject(ProjectFileName)
            try:
                self.ActiveExperiment = self.ActiveProject.Experiments.Item(ExperimentIdx)
                self.ActiveExperiment.Activate()
                self.LogDebug("Activate Experiment %s..." %self.ActiveExperiment.Name, self)
            except :
                self.LogException(self)
        except :
            self.LogException(self)
    def GetActiveProjectAndExperiment(self):
        """
        """
        try:
            self.ActiveProject = self.ControlDeskApplication.ActiveProject
            self.ActiveExperiment = self.ControlDeskApplication.ActiveExperiment
##            self.ControlDeskApplication.
        except :
            self.LogException(self)


    def Save(self, Filename = None):
        """
        """
        self.ActiveProject.Save()
    def Close(self, SaveChanges=False):
        """ 
        """
        try: 
            self.ControlDeskApplication.Quit(SaveChanges) # a flag can be added after start and close app
        except com_error:
            pass

    def Show(self):
        """Show()
        Makes excel application visible
        """
        self.ControlDeskApplication.MainWindow.Visible= True
        self.LogDebug("Show CDNG Application...", self)
        
    def Hide(self):
        """Hide()
        Hides excel application
        """
        self.ControlDeskApplication.MainWindow.Visible= False
        self.LogDebug("Hide CDNG Application...", self)


    def AddXCPPlatform(self):
        """
        """
        if self.ActiveProject <> None :
            self.XCP = self.ActiveExperiment.Platforms.Add(self.Enums.PlatformType.XCPonCAN)
            return self.XCP
            
        else:
            self.LogError("No active experiment fount",self)
            return None


    def GetPlatfrom(self, PlatformName):
        """
        """
        if self.ActiveProject <> None :
            try:
                Platform = self.ActiveProject.Platforms.Item(PlatformName)
                return Platform
            except:
                self.LogError("Platform (%s) was not found"%PlatformName,self)
                return None
            
        else:
            self.LogError("No active experiment was fount",self)
            return None
    def AddUserFunction(self,FunctionName,BatchFile = None):
        if BatchFile <> None:
            if not os.path.isabs(BatchFile):
                BatchFile = os.path.abspath(BatchFile)
            Directory =  os.path.dirname(BatchFile)
            if not self.ControlDeskApplication.UserFunctions.Contains(FunctionName):
                Fun = self.ControlDeskApplication.UserFunctions.Add(FunctionName)
                Fun.Command = BatchFile
                Fun.InitialDirectory = Directory
                return Fun
            else :
                self.LogWarning("Function with same name was found, AddUserFunction is aborted ",self)
                return None        
        else:
            self.LogError("Batch file was provided",self)
            return None


def ExampleOfCDNGClass():
    """ This function demonstrates how to use
    the class CDNGAccess """

    elf = CDNGAccess() # create a class 
    elf.Start() # statr connectin with CDNG
    print ("Stop")
    elf.AddUserFunction("NewFun11", r"D:\SteerPrj\Core\03_SystemTest\TestAutomation\AD_Utilities\Libraries\Python\AddPathtoEnvVar.bat") # create a usedefined function 
##    elf.OpenProjectAndActivateExperiment(r"C:\Users\elbasiom\Documents\dSPACE\ControlDeskNG\5.6\CalDemo\CalDemo.CDP", 1)
##    elf.GetActiveProjectAndExperiment() # get handle of the active project and experiment 
##    XCPCom = elf.AddXCPPlatform() # add an empty XCP Device 
##    XC_D = XCPDevice(XCPCom) # create an object for parsing xcp device setting 
##    XC_D.GetAttFromExcel("GEM") # get the setting for excel sheet 
##    XC_D.SetAttToXCPCom() # set the required attribute in CDNG 
##    elf.Close()

if __name__ == '__main__':
    ExampleOfCDNGClass()  