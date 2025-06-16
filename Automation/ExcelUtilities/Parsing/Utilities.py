#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: XlsUtilities.py
#
#   Description: This module contains helper classes for XlsUtilities such as Cell, Range(to be added), Headers ? 
#   Input :- 	  1.  
#   Conditions :- 1.  

#
#   Author: Mohamed Elbasiony - ZF Friedrichshafen AG, initial version was delivered by SimonB - dSPACE 
#=======================================================================================================

from Logging.Logger import LogBase



class Cell(LogBase):
    """a cell can be created by using either only letter or letter and number for column and row values"""
    
    Templist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
        "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    global ColLetters
    ColLetters = ['']
    ColLetters.extend(Templist)
    for firstLetter in Templist:
        for secondLetter in Templist:
            ColLetters.append(firstLetter + secondLetter)
    ColLetters = ColLetters[:257]

    def __init__(self, ColIndex, RowIndex, Value = None):
        self.Column = Cell.TransformDigitToLetter(ColIndex)
        self.ColIndex = ColIndex
        self.Row = RowIndex
        self.Value = Value

    def __str__(self):
        return str(self.Column) + str(self.Row)

    def __repr__(self):
        return str(self)

    @staticmethod
    def TransformDigitToLetter(ColIndex):
        """TransformDigitToLetter(ColumnIndex)
        Returns the column letter for a column index
        """
        global ColLetters
        if (str(ColIndex).isdigit()):
            return ColLetters[ColIndex]
        return ColIndex

class Header(LogBase):
    def __init__(self, Value, Parent = None):
        """Header(Value)
        Initializes a new header object with the expected ValueError
        """
        LogBase.__init__(self)
        self.Parent = Parent
        self.Value = Value
        self.Cell = None
        self.SubHeader = list()
        self.StartIndex = 0
        self.StopIndex = 0
        self.Level = 0
        if self.Parent != None:
            self.Level = self.Parent.Level + 1


    def __str__(self):
        return "%s = %s" % (str(self.Cell), self.Value)


    def AddSubHeader(self, Value):
        """AddSubHeader(Value)
        Appends a new header object with expected value
        to the subheaders
        """
        SubHeader = Header(Value, self)
        self.SubHeader.append(SubHeader)
        return SubHeader

    def GetSubHeader(self, Value):
        """GetSubHeader(Value)
        Looks into the collection of subheaders for
        a header with the associated value. Values are lowered
        in advance to avoid case-sensitivity
        """
        for subHeader in self.SubHeader:
            if subHeader.Value.lower() == Value.lower():
                return subHeader
        return None

    def Find(self, Values):
        """Find(Values)
        Try to find the expected header with all Subheader
        in values from excel
        """
        headerFound = False
        # If we are in a subheader narrow the search range by start column
        # of parent cell
        startCol = 0
        if self.Parent:
            startCol = self.Parent.Cell.ColIndex
        for rowIndex, row in enumerate(Values):
            for columnIndex, column in enumerate(row[startCol:]):
                try:
                    if column != None and not headerFound:
                        if self.Value.lower() in str(column).lower():
                            self.Cell = Cell(columnIndex + startCol, rowIndex, column)
                            self.StartIndex = columnIndex
                            headerFound = True
                    elif headerFound and (column == None or self.Value.lower() not in str(column).lower()):
                        self.StopIndex = columnIndex
                        break
                except UnicodeEncodeError:
                    pass
        if headerFound:
            for subHeader in self.SubHeader:
                subHeader.Find(Values[self.Cell.Row + 1:])

    def IsValid(self):
        if self.Cell == None:
            return False
        for subHeader in self.SubHeader:
            return subHeader.IsValid()
        return True

    def GetAllHeaders(self, flatHeaderList):
        """GetAllHeaders(FlatHeaderList)
        Returns a flat list of all headers
        """
        flatHeaderList.append(self)
        for subHeader in self.SubHeader:
            subHeader.GetAllHeaders(flatHeaderList)



class Headers(LogBase):
    def __init__(self, Name="Header Group"):
        LogBase.__init__(self)
        self.Name = Name
        self.Headers = list()
        self.__LastHeader = None

    def __iter__(self):
        return iter(self.Headers)

    def AddHeader(self, Value):
        """AddHeader(Value)
        Adds a header object with the expected value
        """
        self.__LastHeader = Header(Value)
        self.Headers.append(self.__LastHeader)
        return self.__LastHeader

    def GetHeader(self, Value):
        """GetHeader(Value)
        Returns the main header with the associated value.
        Lowers values in advance to avoid case-sensitivity
        """
        for curHeader in self.Headers:
            if curHeader.Value.lower() == Value.lower():
                return curHeader
        return None

    def GetHeadersFlat(self):
        """GetHeadersFlat()
        Returns a flat list of all header, sub header, sub sub headers, ....
        """
        FlatHeaders = list()
        for curHeader in self.Headers:
            curHeader.GetAllHeaders(FlatHeaders)
        return FlatHeaders
