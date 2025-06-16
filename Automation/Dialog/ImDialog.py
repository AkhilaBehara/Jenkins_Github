#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: CDNG.py
#
#   Description:  Provides some generic dialogs needed 
#
#   Author: Mohamed Elbasiony - ZF Friedrichshafen AG, initial version was delivered by SimonB - dSPACE 
#=======================================================================================================

import win32con
import win32ui
from pywin.mfc import dialog
import clr
import os
import sys
import Tkinter
import tkFileDialog

sys.path.append("")
CurrentDir = os.path.abspath(os.path.dirname(__file__))
FolderDialogPath = CurrentDir + '\\' +  'FolderDialog'

try : 
    Util_Handle = clr.AddReference(FolderDialogPath)
except :
    print ('Please make sure the FolderDialog.dll is in the same script folder %s', %FolderDialogPath)


def GetSelectionListDialogValue(Collection):
    """ GetSelectionListDialogValue(Collection)
    This function creates a Windows Forms selection list dialog. The dialog
    contains all items given in the Collection parameter and returns the selected
    item.
    """

    LDLG = Util_Handle.CreateInstance("FolderDialog.ListSelectionDialog")
    
    for curItem in Collection:
        LDLG.Text = "Select Project"
        LDLG.ListItems.Add(str(curItem))
    LDLG.Init()
    if LDLG.ShowDialog() == 1:
        return LDLG.SelectedItem
    return None


#**********************************************************************
# Command id definitions for the dialog                
# e.g ID_CLOSE         = 1000
#**********************************************************************
IDC_STATIC    = -1    # predefined constant
IDC_LIST      = 1000
IDC_STATIC_OUTPUT = 1001

#**********************************************************************
#  Dialog template for the listbox dialog                  
#**********************************************************************       

IDD_SELLISTDLG =  [
                # First the general dialog styles, see printed documentation
                # header of dialog
                #--------------------------------------------------------------------------
                # Define Dialog Header Tuple Object.
                # A tuple describing a dialog box, that can be used to create the dialog.
                #
                # DlgHeadTupObj = [BoxCaption, BoxSize, BoxStyle, BoxExtStyle, BoxFont]
                #
                #    BoxCaption     string : caption
                #                   The caption of the window.
                #    BoxSize        (int, int, int, int) : (x, y, cx, cy)
                #                   The position and size of the window.
                #    BoxStyle       int : style
                #                   The style bits for the dialog. Combination of WS_*
                #                   and DS_* constants.
                #    BoxExtStyle    int : extStyle
                #                   The extended style bits for the dialog.
                #    BoxFont        (int, string) : (fontSize, fontName)
                #                   A tuple describing the font, or None if the system
                #                   default font is to be used.
                #--------------------------------------------------------------------------
                ["Please select one item", (0, 0, 408, 110), win32con.WS_CAPTION + win32con.WS_EX_TOPMOST,
                 None, (8, "MS Sans Serif") ],
                # Then the controls
                #--------------------------------------------------------------------------
                # Define Dialog Item Tuple Objects.
                # Tuples describing controls in a dialog box.
                #
                # DlgItemTupObj = [WClass, Caption, ID, Size, Style]
                #
                #    WClass     string/int : windowClass
                #               The window class. If not a string, it must be in
                #               integer defining one of the built-in Wondows controls.
                #               If a string, it must be a pre-registered windows class
                #               name, a built-in class, or the CLSID of an OLE
                #               controls.
                #    Caption    text : caption
                #               The caption for the control, or None.
                #    ID         int : ID
                #               the child ID of this control. All children should have
                #               unique IDs. This ID can be used by GetDlgItem to
                #               retrieve the actual control object at runtime.
                #    Size       (int, int, int, int) : (x, y, cx, cy)
                #               The position and size of the control, relative to the
                #               upper left of the dialog, in dialog units.
                #    Style      int : style
                #               The window style of the control.
                #--------------------------------------------------------------------------
                # The order of the controls in this list define the tab order
                # buttons
                ["Button", "Ok"                    , win32con.IDOK, (7,90,50,14),       win32con.WS_TABSTOP        |
                                                                                        win32con.WS_VISIBLE        |
                                                                                        win32con.BS_DEFPUSHBUTTON  ],
                ["Button", "Cancel"                , win32con.IDCANCEL, (67,90,50,14),  win32con.WS_TABSTOP        |
                                                                                        win32con.WS_VISIBLE        ],
                # Static text (header)
                ["Static", ""                      , IDC_STATIC_OUTPUT, (7,7,392,15),   win32con.WS_VISIBLE       |
                                                                                        win32con.SS_LEFT          ],
                # ListBox
                ["ListBox", ""                     , IDC_LIST     , (7,22,392,70)  ,    win32con.WS_VISIBLE        |
                                                                                        win32con.WS_BORDER         |
                                                                                        win32con.LBS_NOTIFY        |
                                                                                        win32con.LBS_HASSTRINGS    |
                                                                                        win32con.WS_VSCROLL        |
                                                                                        win32con.WS_HSCROLL        ],
                ]


#**********************************************************************
#  Class SelectionListDialogDialog
#   this class is for creating a dialog with a listbox.
#**********************************************************************
class SelectionListDialog(dialog.Dialog):
    #--------------------------------------------------------------------------
    # Function: __init__
    #
    #    When a class object is called, a new class instance is created and
    #    returned. This implies a call to the class's __init__() method if
    #    it has one. Any arguments are passed on to the __init__() method.
    #--------------------------------------------------------------------------
    def __init__(self, HeaderText, SelectionList):
        self._HeaderText = HeaderText
        self._SelectionList = SelectionList
        self._Selection = ""
        dialog.Dialog.__init__(self, IDD_SELLISTDLG)
        
        #----------------------------------------------------------------------
        # HookCommand(<obHandler>, <id>) hooks a windows command handler.
        # <obHandler> will be called as the application receives command
        # notification messages with the specified <id>. Command notification
        # messages are usually sent in response to menu or toolbar commands.
        #----------------------------------------------------------------------
        # Hook to the Command Loop    
        #                Function          ID         

        # This allows to be notified when the ListBox is clicked by the user
        self.HookCommand(self.OnNotify   , IDC_LIST )

    def GetSelection(self):
        return self._Selection

    #**********************************************************************
    # Command handler functions                                           
    #**********************************************************************

    #--------------------------------------------------------------------------
    # Function:     OnNotify
    #
    #    Parameter: ID      is an integer and handled the command id.
    #               Code    is an integer and represent the command
    #                       notification code.
    #--------------------------------------------------------------------------
    def OnNotify(self, Id, Code):
        """method is called when the focus in the listbox
           changes from one item to the other"""
        #----------------------------------------------------------------------
        # Get an instance of the listbox control.
        #----------------------------------------------------------------------
        Listbox = self.GetDlgItem(IDC_LIST)
        # Get all indices from the selected items
        CurSel = Listbox.GetCurSel()
        if CurSel >=0:
            self._Selection = Listbox.GetText(Listbox.GetCurSel())
        else:
            self._Selection = ""
    
    def OnInitDialog(self):
        # Get an instance of the listbox control add the items 
        Listbox = self.GetDlgItem(IDC_LIST)
        for MyItem in self._SelectionList:
            Listbox.AddString(MyItem)

        # Set header text
        StaticText = self.GetDlgItem(IDC_STATIC_OUTPUT)
        StaticText.SetWindowText(self._HeaderText)

        # Set the focus rectage to a specified item.
        Listbox.SetCaretIndex(0)           
##        # For default the first item is selected
##        Listbox.SetSel(0, 1) # 1=TRUE
        
# ----- end of class SelectionListDialog --------------------------------------


def OpenSelectionListDialog(HeaderText, SelectionList):
    #--------------------------------------------------------------------------
    # Create the dialog box.
    #--------------------------------------------------------------------------
    Dlg = SelectionListDialog(HeaderText, SelectionList)
    #--------------------------------------------------------------------------
    # Create a modal window for the dialog box.
    #--------------------------------------------------------------------------
    if win32con.IDOK == Dlg.DoModal():
        return Dlg.GetSelection()
    else:
        return ""


def GenericFileDialog(DialogType, DialogTitle, InitialDir, FileType, FileExtension, InitialFileName=""):
    """
    Description: open a standard "file open" or "file save" dialog box 

    Inputs:      - DialogType: string, "Load" or "Save"
                 - DialogTitle: string, header of GUI
                 - InitialDir: string, initial directory
                 - FileType  : short string like "TDX" or "TestSuite"
                 - FileExtension   : without ".", e.g. "xml"
                 - InitialFileName : string, initial file name if DialogType == "Save"
    """
    OpenFlags = win32con.OFN_OVERWRITEPROMPT
    #------------------------------------------------------------------
    # CreateFileDialog(<fileopen>, <ext>, <filename>, <flags>, <filter>, <parent>)
    #      creates a file open/save/etc selection dialog box.
    #
    #       <fileopen> : is A flag indicating if the Dialog is a FileOpen or FileSave dialog.
    #       <ext>      : is the default file extension for saved files. If None, no extension is supplied.
    #       <filename> : is the initial filename that appears in the filename edit box. If None, no filename initially appears.
    #       <flags>    : are the flags for the dialog.
    #       <filter>   : is a series of string pairs that specify filters you can apply to the file.
    #                    If you specify file filters, only selected files will appear in the Files list box.
    #                    The first string in the string pair describes the filter;
    #                    the second string indicates the file extension to use.
    #                    Multiple extensions may be specified using ';' as the delimiter.
    #                    The string ends with two '|' characters.  May be None.
    #       <parent>   : is the parent or owner window of the dialog.
    #------------------------------------------------------------------
    Filter = FileType + " file (*." + FileExtension + ")|*." + FileExtension + "||"
    if DialogType.lower() == "load":
        Dialog = win32ui.CreateFileDialog(1, "", "*." + FileExtension, OpenFlags, Filter , None)
    else:
        Dialog = win32ui.CreateFileDialog(0, "", InitialFileName,      OpenFlags, Filter , None)
        
    # Set the title for the dialog.
    Dialog.SetOFNTitle(DialogTitle)
    # Set the initial directory for the dialog.
    Dialog.SetOFNInitialDir(InitialDir)
    # Create a modal window for the font dialog box.
    RetVal = Dialog.DoModal()

    # If the 'OK' button was pressed, the file name will be taken
    if win32con.IDOK == RetVal:
        # IDOK : you will get it when a dialog box is displayed normally.
        FileName = Dialog.GetPathName()
    else:
        FileName = ""
        
    return FileName
def SelectFolderDialog(initDir = "C:\\", Foldertitle = "Select Folder"):
    root = Tkinter.Tk()
    root.withdraw()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir=initDir, title=Foldertitle)
    if len(tempdir) > 0:
        print ("You chose %s" tempdir)
        DirName =  tempdir
    else:
        DirName = ""
    return DirName