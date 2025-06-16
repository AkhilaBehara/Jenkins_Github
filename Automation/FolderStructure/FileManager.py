#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: FolderStructure.py
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
from os import  path
from dspace.com import Enums
from pywintypes import com_error
try:
    import exceptions
except ImportError:
    import builtins as exceptions
import  shutil



#-------------------------------------------------------------------------------------------------
# CDNGAccess Class
#-------------------------------------------------------------------------------------------------
class Node(LogBase):
    ## On creation, get an Excel instance, if filename is given, load the related document
    def __init__(self,NodePath = None):
        """Constructor(Filename)
        Creates a new instance of CDNGAccess
        """
        LogBase.__init__(self)
        self.Parent = None
        self.Childerens = None
        self.SetPath(NodePath)
        self.SetType()
        self.Attribute = "Header"
        self.ListofChilderenPath = []
        self.getChilderens()
        
        
    def __str__(self):
        return "Root"
#-------------------------------------------------------------------------------------------------
# Public methods
#-------------------------------------------------------------------------------------------------
    def SetPath(self, NodePath = None):
        """
        """
        if  NodePath:
            self.Path= path.abspath(NodePath)
            self.Path = path.normpath(self.Path)
            
        else :
            self.Path = None

    def GetPath(self):
        """
        """
        return self.Path
    def SetType(self):
        if path.isfile(self.Path):
            self.Type = "File"
        if path.isdir(self.Path):
            self.Type = "Folder"
        else:
            self.Type = "Link"
        
    def getChilderens(self):
        
        if  path.isabs(self.Path):
            if self.Type == "Folder" :
                self.Childerens = os.listdir(self.Path)
                if self.Childerens:
                    for Childeren in self.Childerens:
                        ChildernPath = path.join(self.Path,Childeren)
                        self.ListofChilderenPath.append(ChildernPath)
    def InsertChild(self,FolderName):
        
        dirName = os.path.join(self.Path ,FolderName)
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
        return  dirName            
            
    def RemoveChild(self,FolderName):
        
        dirName = os.path.join(self.Path ,FolderName)
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            print("Directory " , dirName ,  " removed ")
        else:    
            print("Directory " , dirName ,  " doesnot exist")
                     
class FFManager(LogBase):

    def __init__(self,Node = None):
        self.MainNode = Node
        self.FoundItemList = []
        self.RestFlag = 1
        
                        
    def  FindItem(self,Recursive_Node,ItemName) : 
##    """ return list of files
##    """
        for s in Recursive_Node.ListofChilderenPath:
            if ItemName in s :
                return s
            
        for Child in Recursive_Node.ListofChilderenPath :
            ChildNode = Node(Child)
            retVal = self.FindItem(ChildNode,ItemName)
            if retVal:
                return retVal
            
    def  FindItemList(self,Recursive_Node,ItemName) :

        self.FoundItemList = []
        self.__FindList(Recursive_Node,ItemName)
        

    def  __FindList(self,Recursive_Node,ItemName) :
        for Child in Recursive_Node.ListofChilderenPath :
            if ItemName in Child :
                self.FoundItemList.append(Child)
            else: 
                ChildNode = Node(Child)
                retVal = self.__FindList(ChildNode,ItemName)



    def ReplaceTextinFiles(self,Folder,SearchText,ReplacementText,AllowedExtentions):
        for filename in os.listdir(Folder):
                FileExt = filename.split(".")[1]
                if FileExt in allowedExtentions:
    ##                print filename
                    try  : 
                        ReadFile = open(Folder+ "\\" + filename, "r")
                        RLines = ReadFile.readlines()
                        WLines = []   
                        for line in RLines:    
                            NewLine = line.replace(SearchText, ReplacementText) # a dot has been added to ensure only library is being changed
                            WLines.append(NewLine)
                    finally :
                        ReadFile.close()
                    try:
                        WriteFile = open(Folder+ "\\" + filename, "w+")
                        WriteFile.writelines(WLines)
                    finally : 
                        WriteFile.close()
    
    def RenameFile(self,old_file_name, new_file_name): 
        if not os.path.exists(new_file_name):
             os.rename(old_file_name, new_file_name) 
        else:    
            print("The file already exists")
    

def ExampleOfRoot():
    """ This function demonstrates how to use
    the class CDNGAccess """

    elf = Node(r"D:\HiLUsers\ElbasioM")# create a class
    return elf


if __name__ == '__main__':
    Node1 = ExampleOfRoot()
    FF = FFManager(Node1)
##    print FF.FindItem(Node1,".current")
    FF.FindItemList(Node1,".adp.zip")
    print (FF.FoundItemList)

