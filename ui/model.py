# model.py
# This is the model part of the Model-View-Controller

import pandas as pd
import os
import numpy as np

class Model:

    def __init__(self):
        '''
        Initializes the members the class holds. Also sets index and multiSheet to their default.
        '''

        self.fileName = None
        self.fileContent = str
        self.index = False
        self.sheetName = str
        self.multiSheet = False
        self.fileType = ".xslx"
        self.delimiter = str
        self.hlineAll = str
        self.hlineOutside = str
        self.roundBy = None

    def isValid(self, fileName):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try:
            file = open(fileName, 'r')
            file.close()
            return True
        except:
            return False

    def setFileName(self, fileName):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  O
        '''
        if self.isValid(fileName):
            self.fileName = fileName
        else:
            self.fileName = ""

    def setFileType(self):
        '''
        Sets if the file type of the given file.
        '''
        self.fileType = os.path.splitext(self.fileName)[-1].lower()

    def activateMultiSheet(self):
        '''
        Sets if the index should get used or not
        '''
        self.multiSheet = True

    def setMultiSheet(self, sheetname):
        '''
        Sets the name of the Sheet that is gonna be used for the LaTeX converter.
        '''
        self.sheetName = sheetname

    def setIndex(self, index):
        '''
        Sets if the index should get used or not.
        '''
        self.index = index

    def setEndline(self, endline):
        '''
        sets the endline, which will be behind every line of the LaTeX Code.
        '''
        self.endline = endline
        
    def setHlineAll(self, hlineAll):
        '''
        sets the hline option, which will be behind every row of the LaTeX Code.
        '''
        self.hlineAll = hlineAll

    def setHlineOutside(self, hlineOutside):
        '''
        sets the hline option, which will be after header and the last row of the LaTeX Code.
        '''
        self.hlineOutside = hlineOutside

    def makeTable(self):
        '''
        Creates a Table object with the given data and sets the fileContent variable
        to the output LaTeX String.
        '''
        self.table = Table(self.fileName, self.fileType, self.endline, self.index, self.sheetName, self.delimiter, self.hlineAll, self.hlineOutside, self.roundBy)
        self.table.convert2Latex()
        self.fileContent = self.table.fileContent

    def getFileName(self):
        '''
        Returns the name of the file name member.
        '''
        return self.fileName

    def getFileContent(self):
        '''
        Returns the contents of the file if it exists, otherwise
        returns an empty string.
        '''
        return self.fileContent

    def setDelimiter(self, delimiter):
        '''
        sets the delimiter for csv, otherwise
        sets default ';' .
        '''
        self.delimiter = delimiter

    def setRoundBy(self, roundBy):
        '''
        sets if and how much numbers get rounded
        '''
        if roundBy == "Dont round":
            self.roundBy = False
        else:
            self.roundBy = int(roundBy)


class Table():


    def __init__(self, fileName, fileType, endline, index, sheetname, delimiter, hlineAll, hlineOutside, roundBy):
        '''
        Initializes the members the class holds. Also sets index and multiSheet to their default.
        '''
        self.fileName = fileName
        self.fileType = fileType
        self.endline = endline
        self.index = index
        self.fileContent = str
        self.sheetname = sheetname
        self.delimiter = delimiter
        self.hlineAll = hlineAll
        self.hlineOutside = hlineOutside
        self.roundBy = roundBy

    def getContent(self):
        '''
        Uses pandas to create a DataFrame
        '''
        read_excel_filetypes = [".xlsx", ".xls", ".csv", ".xlsm", ".xlsb", ".odf", ".ods"]
        if self.fileType == ".csv":
            df = pd.read_csv(self.fileName, delimiter=self.delimiter)
            return df
        if self.fileType in read_excel_filetypes:
            if not self.sheetname:
                df = pd.read_excel(self.fileName)
            if self.sheetname:
                df = pd.read_excel(self.fileName, sheet_name=self.sheetname)
        df1 = df.replace(np.nan, '', regex=True )
        return df1

    def convert2Latex(self):
        '''
        Uses pandas to create a DataFrame
        '''

        df = self.getContent()
        columns = df.columns

        header = " & ".join(str(columns)) + f" \\\ {self.endline}\n"

        if self.hlineAll or self.hlineOutside:
            header += "\hline\n"
        data = []

        for index, row in df.iterrows():
            row_data = []
            if self.index:
                row_data.append(str(index))
            for column in columns:
                if self.roundBy:
                    try:
                        field = round(float(row[column]), self.roundBy)
                        if 0 == field % 1:
                            field = int(field)
                    except:
                        field = row[column]
                else:
                    field = row[column]
                row_data.append(str(field))
            data.append(" & ".join(row_data) + f" \\\ {self.endline}")
            if self.hlineAll:
                data.append("\\hline")
        self.fileContent = header + "\n".join(data)
        if self.hlineOutside and not self.hlineAll:
            self.fileContent += "\n\\hline"
