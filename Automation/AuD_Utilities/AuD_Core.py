#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: AuD.py
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
import os
from dspace.com import Enums
from pywintypes import com_error
import exceptions

#-------------------------------------------------------------------------------------------------
# CDNGAccess Class
#-------------------------------------------------------------------------------------------------
class AuDAccess(LogBase):
    ## On creation, get an Excel instance, if filename is given, load the related document
    def __init__(self):
        """Constructor(Filename)
        Creates a new instance of CDNGAccess
        """
        LogBase.__init__(self)
        self.AuDApplication = None
        self.Enums = None
        self.LogDebug("Creating new AuD instance...", self)
        self.ActiveProject = None

    def __str__(self):
        return "AuDAccess"

    def __FindItem(self, Root, ItemName):

        if ItemName in Root.SubBlocks.Names:
            return Root.SubBlocks.Item(ItemName)
        for curName in Root.SubBlocks.Names:
            retVal = self.__FindItem(Root.SubBlocks.Item(curName),ItemName)
            if retVal:
                return retVal
#-------------------------------------------------------------------------------------------------
# Public methods
#-------------------------------------------------------------------------------------------------
    def GetAllSequences(self,Recursive_Node =None) : 
        self.FoundItemList = []
        self.GetSequenceList(Recursive_Node)
        return self.FoundItemList
        
        
    
    def  GetSequenceList(self,Recursive_Node) :
        if hasattr(Recursive_Node, "SubBlocks"): # check that is folder or sequence
            if (Recursive_Node.SubBlocks.Count == 0) & (Recursive_Node.Type==self.Enums.ElementType.adSequence):
                self.FoundItemList.append(Recursive_Node.Name)    # in this part where TCs are found they can be captured for further work 
            elif Recursive_Node.SubBlocks.Count > 0 :
                for Child in Recursive_Node.SubBlocks.Names :
                        retVal = self.GetSequenceList(Recursive_Node.SubBlocks.Item(Child))
            else :
                self.LogWarning("The following node is empty %s" % Recursive_Node.Name, self)

    def GetFolder(self, ProjectName, FolderName = None):

        ProjectRoot = self.AuDApplication.Projects.Item(ProjectName)
        if FolderName  : 
            retVal = self.__FindItem(ProjectRoot, FolderName)
            return retVal
        else :
            return ProjectRoot
        
    def Ajay(self):
        pass
    def GetLibrarySequence(self, LibraryName, SeqName):
        if LibraryName not in self.AuDApplication.Libraries.Names:
            print ("Error: Could not find %s library in AutomationDesk.", LibraryName)
            return
        Library = self.AuDApplication.Libraries.Item(LibraryName)
        retVal = self.__FindItem(Library, SeqName)
        return retVal
    
    def Start(self):
        self.AuDApplication = Dispatch("AutomationDesk.TAM")
        self.LogDebug("Openining AuD Application...", self)
        self.Enums = Enums(self.AuDApplication)
        
    def OpenProject(self, ProjectFileName):
        """
        """
        try:
            return self.AuDApplication.Projects.Open(ProjectFileName,self.Enums.FileOptions.adOverWrite)
            
        except :
            self.LogException(self)
    def GetActiveProject(self):
        """
        """
        try:
            self.ActiveProject = self.AuDApplication.Projects.ActiveProject
            return self.ActiveProject
        except :
            self.LogException(self)

    def Save(self, Filename = None):
        """
        """
        self.ActiveProject.Save()
    def Close(self):
        """ 
        """
        try: 
            self.AuDApplication.Quit() # a flag can be added after start and close app
        except com_error:
            pass
    def CloseProject(self,ProjectName):
        """ 
        """
        try: 
            self.AuDApplication.Projects.Item(ProjectName).Close() 
        except com_error:
            return None 
    def Show(self):
        """Show()
        Makes excel application visible
        """
        self.AuDApplication.Visible= True
        self.LogDebug("Show AuD Application...", self)
        
    def Hide(self):
        """Hide()
        Hides excel application
        """
        self.AuDApplication.Visible= False
        self.LogDebug("Hide AuD Application...", self)


def ExampleOfAuDClass():
    """ This function demonstrates how to use
    the class CDNGAccess """

    elf = AuDAccess() # create a class 
    elf.Start() # statr connectin with CDNG
    elf.Show()
    Proj = elf.OpenProject(r"C:\Local Data\SandBox\Teams_SytemTesting\2430_Projects\VW_MQB_A0\AD_Prj\VW_MQBA0_ENG10_TestSpec_MiscFunctions.adp.zip")
    Proj = elf.GetActiveProject()
    RootFolder = elf.GetFolder(Proj.Name)
    SeqList = elf.GetAllSequences(RootFolder)
    print (SeqList)
    elf.CloseProject(Proj.Name)


if __name__ == '__main__':
    ExampleOfAuDClass()  