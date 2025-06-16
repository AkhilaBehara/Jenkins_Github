#=======================================================================================================
# -*- coding: utf-8 -*-
#
#   Module: Logger.py
#
#   Description: This module contains helper classes for logging events happening during script execution 
#   Input :- 	  1.  
#   Conditions :- 1.  
#   Author: Mohamed Elbasiony - ZF Friedrichshafen AG, initial version was delivered by SimonB - dSPACE 
#=======================================================================================================

import time
import os
import xml.etree.cElementTree as ET
import traceback
import shutil
from Logging import XmlUtilities

class MsgColors(object):

    def __init__(self):
        self.__dict__['WARNING'] = '\033[93m'
        self.__dict__['ERROR'] = '\033[91m'
        self.__dict__['END'] = '\033[0m'
        self.__dict__['MESSAGE'] = ''
        self.__dict__['DEBUG'] = ''

    def __getitem__(self, name):
        """ Returns the correct color for severity """
        return self.__dict__[name]

class MsgSeverity(object):
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    MESSAGE = 'MESSAGE'
    DEBUG = 'DEBUG'
    
class LogMessage(object):
    def __init__(self, Msg, Origin, Severity):
        self.Msg = Msg
        self.Severity = Severity
        self.TimeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.Origin = Origin

    @classmethod
    def fromString(cls, Message, Origin = None, Severity = MsgSeverity.MESSAGE):
        """ Creates a new log message from a string with default
        severity set to message """
        if not Origin:
            Origin = "Unknown"
        retVal = cls(Message, Origin, Severity)
        print (retVal)
        return cls(Message, Origin, Severity)


    def prettyPrint(self):
        """ Method to print an error/warning/message into console """
        return MsgColors()[self.Severity] + str(self) + MsgColors()['END']
    
    def __str__(self):
        """ Method for string representation of a message """
        return ("<%s | %s" + (9 - len(str(self.Severity))) * ' ' + "| %s" + (28 - len(str(self.Origin))) * ' ' + "> %s") % (self.TimeStamp, self.Severity, self.Origin, self.Msg)
    
    def WriteXml(self, root):
        """ Method to write log message to XML """
        Message = ET.SubElement(root, "Message", TimeStamp=self.TimeStamp, Severity=self.Severity, Origin=str(self.Origin))
        Message.text = self.Msg
        

    def WriteTxt(self, fHandle):
        """ Method to write log message to TXT """
        fHandle.write(str(self) + "\n")

class Logger(object):
    global AllMsgs
    AllMsgs = list()
    global declaration
    declaration = """<?xml version="1.0" encoding="utf-8"?>
    <?xml-stylesheet type='text/xsl' href='.\Resources\log.xsl'?>\n"""


    @staticmethod
    def Log(Message):
        """ Method to log messages """
        global AllMsgs
        AllMsgs.append(Message)

    @staticmethod
    def Save(filename):
        global AllMsgs
        global declaration
        fileType = os.path.basename(filename).split('.')[1]
        if fileType not in ['txt', 'xml']:
            raise Exception("Logging file format not supported. Please choose TXT or XML.")
        if fileType == 'txt':
            fHandle = open(filename, 'w')
            for curMsg in AllMsgs:
                curMsg.WriteTxt(fHandle)
            fHandle.flush()
            fHandle.close()
        elif fileType == 'xml':
            root = ET.Element("Logging", Date = time.strftime("%m-%d-%Y"))
            for curMsg in AllMsgs:
                curMsg.WriteXml(root)
            XmlUtilities.indent(root)
            tree = ET.ElementTree(root)
            with open(filename, 'w') as output:
                output.write(declaration)
                tree.write(output, xml_declaration=False, encoding='utf-8')
            Logger.__CopyResources(filename)
    
    @staticmethod
    def __CopyResources(filename):
        ResourcesDir = os.path.join(os.path.dirname(__file__), "Resources")
        if not os.path.exists(ResourcesDir):
            Logger.Log(LogMessage.fromString("Could not create find Resources directory for XML log.", self, "WARNING"))
            return
        ResourceDest = os.path.join(os.path.dirname(filename), "Resources")
        try:
            shutil.copytree(ResourcesDir, ResourceDest)
        except:
            Logger.Log(LogMessage.fromString(traceback.format_exc(), Logger, "ERROR"))
        
            
        
        
              

class EventBase(object):
    '''
    EventBase Class for Handling events
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.handlers = set()
        
    def handle(self, handler):
        '''
        Adds a handler to the listeners
        '''
        self.handlers.add(handler)
        return self
    
    def unhandle(self, handler):
        '''
        Removes a handler from the listeners
        '''
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Could not remove handler. Handler is missing in listener collection.")
        return self
    
    def fire(self, *args, **kwargs):
        '''
        Calls the attached methods from all handlers
        '''
        for handler in self.handlers:
            handler(*args, **kwargs)
            
    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    
class LogBase(object):
    '''
    LogBase Class for Handling LogEvents
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.Log = EventBase()
        self.Log += Logger.Log
        
        
    def LogMessage(self, Msg, Origin=None):
        '''
        Method to log a normal message
        '''
        self.Log(LogMessage.fromString(Msg, str(Origin),"MESSAGE"))
        
        
    def LogError(self, Error, Origin=None):
        '''
        Method to log an error message
        '''
        self.Log(LogMessage.fromString(Error, str(Origin), "ERROR"))

        
    def LogException(self, Origin=None):
        '''
        Method to log an exception
        '''
        self.Log(LogMessage.fromString(traceback.format_exc(), str(Origin), "ERROR"))
        #self.Log(LogMessage.fromString(traceback.format_stack()[-1].rstrip('\n'), str(Origin), "ERROR"))
        
    
    def LogWarning(self, Msg, Origin=None):
        '''
        Method to log a warning message
        '''
        self.Log(LogMessage.fromString(Msg, Origin, "WARNING"))
        
    def LogDebug(self, Msg, Origin=None):
        '''
        Method to log a debug message
        '''
        self.Log(LogMessage.fromString(Msg, Origin, "DEBUG"))
        
    def LogSave(self, Filename):
        '''
        Saves the log
        '''
        Logger.Save(Filename)

        
class LogTester(LogBase):
    def __init__(self):
        LogBase.__init__(self)
        
    def __str__(self):
        return "LogTester"
        
    def Parse(self, filename = None):
        self.LogMessage("Example message log", self)
        self.LogError("Example error log", self)
        self.LogWarning("Example warning log", self)
        try:
            1/0
        except:
            self.LogException(self)
            
        if filename:
            self.Save(filename)
                