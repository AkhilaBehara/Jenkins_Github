#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: XlsUtilities.py
#
#   Description: This module contains helper classes and functions to utilize an API to write and read from existing excel sheets , 
#   Input :- 	  1. File name containing the excel sheet
#   Conditions :- 1. the file must be not in read only mode so it can be saved 
#                 2. manual edit during the script might lead to problems with saving and closing  
#                 3. a Utilities module contians a Cell class to help working with excel as well as header 
#
#   Author: Mohamed Elbasiony - ZF Friedrichshafen AG, initial version was delivered by SimonB - dSPACE 
#=======================================================================================================


from win32com.client import DispatchEx, Dispatch
from Logging.Logger import LogBase
from ExcelUtilities.Parsing.Utilities import Cell, Header, Headers
import os
from abc import abstractmethod


#-------------------------------------------------------------------------------------------------
# XlsAccess Class
#-------------------------------------------------------------------------------------------------
class XlsAccess(LogBase):
    ## On creation, get an Excel instance, if filename is given, load the related document
    def __init__(self):
        """Constructor
        Creates a new instance of XlsAccess
        """
        LogBase.__init__(self)
        self.__Filename = None
        self.__xlWb = None
        self.__xlSh = None
        # Create event for message logging
        self.__ExcelOpenFlag = False
        self.__WorkbookOpenFlag = False

    def __del__(self):
        """Destructor
        Cleanup objects
        """
        self.Close(0)
        self.__xlApl.Quit()
        self.__xlApl = None
        del self.__xlApl

    def __str__(self):
        return "XlsAccess"
#-------------------------------------------------------------------------------------------------
# Public methods
#-------------------------------------------------------------------------------------------------
    def OpenWorkbook(self,Filename):
        """OpenWorkbook()
        Opens the selected excel file.

        - Excel is opened and the given file is loaded. When closing the file
          Excel is also closed.
        """
        try:
            if not os.path.isabs(Filename):
                Filename = os.path.abspath(Filename)
            self.__Filename = Filename
            self.LogDebug("Creating new Excel instance...", self)
            self.__xlApl = DispatchEx("Excel.Application")
            self.__ExcelOpenFlag = True
            self.__xlApl.Visible = True
            self.LogDebug("New Excel instance successfully opened.", self)
            # Load the workbook if it is not opened
            self.LogDebug("Opening workbook %s..." % self.__Filename, self)
            self.__xlWb = self.__xlApl.Workbooks.Open(self.__Filename)
            self.__WorkbookOpenFlag = True
            self.LogDebug("Workbook %s is now opened." % self.__Filename, self)
        except:
            self.LogException(self)

    def Add_Worksheet(self,Sheet=None):
        if (Sheet in self.GetSheetNames()):
            self.__xlApl.DisplayAlerts = False
            self.__xlApl.Worksheets(Sheet).Delete()
            self.__xlApl.DisplayAlerts = True
            ws = self.__xlApl.Worksheets.Add()
            ws.Name = Sheet
        else:
            ws = self.__xlApl.Worksheets.Add()
            ws.Name = Sheet
    def Save(self, Filename = None):
        """Save([Filename])
        Saves the currently opened excel workbook.
        Depending on the Filename parameter the workbook will be saved as
        new file or the existing file will be overwritten

        - If Filename != None:
          File is saved as Filename

        - If Filename == None
          Existing file is overwritten
        """
        if (Filename):
            self.__Filename = Filename
            self.__xlWb.SaveAs(Filename)
        else:
            self.__xlWb.Save()


    def IsExcelStillOpened(self):
        """IsExcelStillOpened
        Checks if Excel is still opened.
        """
        try:
            self.__xlApl.Sheets
            return True
        except:
            return False


    def Close(self, SaveChanges=0):
        """Close([SaveChanges])
        Closes the workbook. Save changes flag indicates whether to
        save or not to save the workbook before closing
        """
##        print self.__WorkbookOpenFlag
##        print self.__ExcelOpenFlag
        if  self.__WorkbookOpenFlag:
            if self.__xlWb != None:
                self.__xlWb.Close(SaveChanges)
        if  self.__ExcelOpenFlag:
            if self.__xlApl != None:
                self.__xlApl.Visible = False
                self.__xlApl.Quit()
        self.__ExcelOpenFlag = False
        self.__WorkbookOpenFlag = False
        # delete the COM Application object to free the task manager
        # del self.__xlApl
    def Show(self):
        """Show()
        Makes excel application visible
        """
        self.__xlApl.Visible = True

    def KillExcelInstance(self):
        del self.__xlApl
        
    def Hide(self):
        """Hide()
        Hides excel application
        """
        self.__xlApl.Visible = False


    def GetValuesFromSheet(self, Sheet="Sheet1"):
        """GetValues(Sheet)
        Returns the values from a sheet of an opened workbook.
        Values are returned as tuple
        """
        if (Sheet in self.GetSheetNames()):
            self.__xlSh = self.__xlWb.Sheets(Sheet)
            return self.__xlSh.UsedRange.Value
        else:
            self.LogError("Could not find '%s'-Sheet in '%s'" % (Sheet, self.__xlWb.Name), self)
            return None


    def GetCellValue(self, RowIndex, ColIndex):
        """GetCellValue(RowIndex, ColIndex)
        Returns the value of a single cell. Cell is given by
        row and column index
        """
        return self.GetValue(Cell(ColIndex, RowIndex))

    def GetValuesAsListOfDictFromSheet_KeyCol(self, Sheet="Sheet1"):
        """GetValuesAsListOfDictFromSheet_KeyCol
        Returns the a list of dictionatries, each dictionary represent a column
        where the key is the first column and the values taken from the corresponding column
        """
        keys = []
        Columns_values = []
        ListOfDic= []
        tempDict = {}
        SheetContent = self.GetValuesFromSheet(Sheet)
        if SheetContent != None:
            for row in SheetContent :
                keys.append(row[0])
                Columns_values.append(row[0:])
            Columns_values_T = map(list, zip(*Columns_values)) 

            for OneColumnValue in Columns_values_T:     
                if len(keys) == len(OneColumnValue):
                    for idx, key in enumerate(keys):
                        tempDict[key] = OneColumnValue[idx]
                ListOfDic.append(tempDict)
##                Header = OneColumnValue[0]
##                DicOfDic[Header] = tempDict
                tempDict = {}
        else:
            self.LogError("Could not find used range '%s'-Sheet" % Sheet, self)
        return ListOfDic, keys
    def GetValuesAsListOfDictFromSheet_KeyRow(self, Sheet="Sheet1"):
        """GetValuesAsListOfDictFromSheet_KeyRow
        Returns  a list of dictionatries, each dictionary represent a row
        where the key is cells in the first row and the values taken from the corresponding row
        """
        keys = []
        Columns_values = []
        tempDict = {}
        ListOfDic = []
        SheetContent = self.GetValuesFromSheet(Sheet)
        if SheetContent != None:
            keys = SheetContent[0] # first row 
            Row_values = SheetContent[1:]

            for OneRowValue in Row_values:     
                if len(keys) == len(OneRowValue):
                    for idx, key in enumerate(keys):
                        tempDict[key] = OneRowValue[idx]
##                Header = OneRowValue[0]
##                DicOfDic[Header] = tempDict
                ListOfDic.append(tempDict)
                tempDict = {}
        else:
            self.LogError("Could not find used range '%s'-Sheet" % Sheet, self)
        return ListOfDic, keys
    
    def SetValue(self,Cell, Sheet=None):
        """SetValue(Cell, Sheet = None)
        Sets a value in a given sheet within an opened workbook.
        Cell is indexed by column and row
        """
        # Two possibilities
        # 1) colIndex is a digit, then transform to corresponding letter
        # 2) colIndex is alpha, no transformation needed

##        if (Sheet):
##            sh = self.__xlWb.Sheets(Sheet)
##        else:
##            sh = self.__xlWb.ActiveSheet
        sh = self.__xlWb.ActiveSheet
        R= Cell.Row 
        C= Cell.ColIndex
        V= Cell.Value

        sh.Cells(R,C).Value = V
        sh.Rows(R).RowHeight = RowHeight = 64
      
    def Set_List_Values(self, Cell, List, Sheet=None):
        sh = self.__xlWb.ActiveSheet

        """SetValue(ColIndex, RowIndex, Value, Sheet = None)
        Sets a value in a given sheet within an opened workbook.
        Cell is indexed by column and row
        """
        # Two possibilities
        # 1) colIndex is a digit, then transform to corresponding letter
        # 2) colIndex is alpha, no transformation needed
        Cell_Index_alpha = Cell[0]
        Cell_Index_digit = int(Cell[1])

        for i in List:
            sh.Range(Cell_Index_alpha + str(Cell_Index_digit)).Value = i
            sh.Range(Cell_Index_alpha + str(Cell_Index_digit)).Font.Name = "Calibri"
            sh.Range(Cell_Index_alpha + str(Cell_Index_digit)).Font.Size = 12
            Cell_Index_digit = Cell_Index_digit+1
            
    def Set_Column_Header(self, Cell, Column_Name, Column_Index=None, Font_Name=None, Font_Size=None, RowHeight=None, ColumnWidth=None,Font_Bold=None, Interior_ColorIndex=None, Sheet=None):

        sh = self.__xlWb.ActiveSheet
        sh.Range(Cell).Value = Column_Name
        sh.Range(Cell).Font.Name = Font_Name
        sh.Range(Cell).Font.Size = Font_Size
        sh.Rows(1).RowHeight = RowHeight
        sh.Columns(Column_Index).ColumnWidth = ColumnWidth
        sh.Range(Cell).Font.Bold = Font_Bold
        sh.Range(Cell).Interior.ColorIndex = Interior_ColorIndex

    def SetSheet(self, Sheetname):
        """SetSheet(Sheetname)
        Sets a given sheet as active sheet.
        """
        Sheetnames = self.GetSheetNames()
        if Sheetname in Sheetnames:
            self.__xlSh = self.__xlWb.Sheets[Sheetname]
            self.__xlApl.Sheets[Sheetname].Activate()
        else:
            self.LogWarning("Workbook %s does not contain a sheet named %s" % (self.__xlWb.Name, Sheetname), self)
        return self.__xlSh

    def CopyFormat(self, StartColIndex, StartRowIndex, EndColIndex, EndRowIndex, DestStartColIndex, DestStartRowIndex, DestEndColIndex, DestEndRowIndex, Sheet = None):
        """CopyFormat(StartColIndex, StartRowIndex, EndColIndex, EndRowIndex, DestStartColIndex, DestStartRowIndex, DestEndColIndex, DestEndRowIndex, [Sheet])
        Copies the format of a range to another range.
        """
        StartColIndex = self.__TransformDigitToLetter(StartColIndex)
        EndColIndex = self.__TransformDigitToLetter(EndColIndex)
        DestStartColIndex = self.__TransformDigitToLetter(DestStartColIndex)
        DestEndColIndex = self.__TransformDigitToLetter(DestEndColIndex)
        StartRange = StartColIndex + str(StartRowIndex) + ":" + EndColIndex + str(EndRowIndex)
        DestRange = DestStartColIndex + str(DestStartRowIndex) + ":" + DestEndColIndex + str(DestEndRowIndex)
        self.SetSheet(Sheet)
        try:
            self.__xlSh.Range(StartRange).Select()
            self.__xlApl.Selection.Copy()
            self.__xlSh.Range(DestRange).Select()
            self.__xlApl.Selection.PasteSpecial(-4122, -4142, None, None)
            self.__xlApl.CutCopyMode = False
        except:
            pass


    def AutoFitColumn(self, ColIndex):
        ColIndex = self.__TransformDigitToLetter(ColIndex)
        self.__xlSh.Range(ColIndex + "1").EntireColumn.AutoFit()


    def GetSheetNames(self):
        'Returns the name of all sheets as a list'
        sh = self.__xlWb.Sheets
        self.__sheetNames = []
        for x in sh:
            self.__sheetNames.append(x.Name)
        return self.__sheetNames

    def GetHyperlink(self, RowIndex, ColIndex):
        """  GetHyperlink(RowIndex, ColIndex)
        Returns the hyperlink object in the requested row and
        column index. If no hyperlink is present, None is returned
        """
        pass


    def GetHyperlinks(self, Sheet=None):
        """GetHyperlinkValue([Sheet])
        Returns all present hyperlinks from an Excel sheet
        """
        if (Sheet):
            sh = self.__xlWb.Sheets(Sheet)
        else:
            sh = self.__xlWb.ActiveSheet
        return sh.Hyperlinks
        #sh.Hyperlinks.Add(sh.Range(Column + str(RowIndex)), Address, "", Tooltip, DisplayText)


    def SetHyperlink(self, ColIndex, RowIndex, Address, Tooltip, DisplayText, Sheet=None):
        """SetHyperlink(ColIndex, RowIndex, Address, Tooltip, DisplayText, [Sheet])
        Sets a hyperlink in the given column and row.

        - ColIndex   : Index of cell column
        - RowIndex   : Index of cell row
        - Address    : Hyperlink address to navigate to
        - Tooltip    : Tooltip that is displayed with a mouse over
        - DisplayText: The text that is displayed for the address
        - Sheet      : Optional Parameter. Otherwise the preselected sheet is used
        """
        Column = self.__TransformDigitToLetter(ColIndex)
        if (Sheet):
            sh = self.__xlWb.Sheets(Sheet)
        else:
            sh = self.__xlWb.ActiveSheet
        sh.Hyperlinks.Add(sh.Range(Column + str(RowIndex)), Address, "", Tooltip, DisplayText)


def GetExampleExcelFile(Excelfile):
    """ This function demonstrates how to use
    the class XlsAccess """
    # Create new instance with excel file as param
    Excel = XlsAccess(Excelfile)
    # Open the workbook
    Excel.OpenWorkbook()
    # Get Sheet Names
    print ("Sheets in Excel File: %s",str(Excel.GetSheetNames()))
    values = Excel.GetValues("Tabelle1")
    # Values are tuple in tuple objects (e.g.: ((Header1, Header2, Header3), (Content1, Content2, Content3), (Content1, Content2, Content3)))

    # Check occurrence of specific headers with parsing utilitites
    exptectedHeader1 = Parsing.Utilities.Header("MyExpectedHeader1")

    # Search for header in values
    exptectedHeader1.Find(values)
    if (exptectedHeader1.IsValid()):
        print ("Header %s was found on index %i.",(expectedHeader1.Value, exptectedHeader1.Index))
    else:
        print ("Header %s was not found.", expectedHeader1.Value)
