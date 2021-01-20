import pandas as pd
import os

fileName = "D:/Programmieren/PycharmProjects/CSV2LaTeX/test.csv"
endline = "H"
index = True
sheetname = ""

class Table():


    def __init__(self, fileName, endline, index, sheetname):
        '''
        Initializes the members the class holds. Also sets index and multiSheet to their default.
        '''
        self.fileName = fileName
        self.fileType = os.path.splitext(self.fileName)[-1].lower()
        self.endline = endline
        self.index = index
        self.fileContent = str
        self.sheetname = sheetname

    def getContent(self):
        '''
        Uses pandas to create a DataFrame
        '''
        if not self.sheetname:
            if self.fileType == ".csv":
                df = pd.read_csv(self.fileName, delimiter=";")
            if self.fileType == ".xlsx":
                df = pd.read_excel(self.fileName)
            return df
        else:
            df = pd.read_excel(self.fileName, sheet_name=self.sheetname)
            return df

    def convert2Latex(self):
        '''
        Uses pandas to create a DataFrame
        '''

        df = self.getContent()
        columns = df.columns
        header = " & ".join(columns) + f" \\\ {self.endline}\n"
        data = []

        for index, row in df.iterrows():
            row_data = []
            if self.index:
                row_data.append(str(index))
            for column in columns:

                # if float, round (2)
                try:
                    field = round(float(row[column]), 2)
                    if 0 == field % 1:
                        field = int(field)

                except:
                    field = row[column]
                row_data.append(str(field))
            data.append(" & ".join(row_data) + f" \\\ {self.endline}")
        self.fileContent = header + "\n".join(data)

    def getFileContent(self):
        return self.fileContent


table = Table(fileName, endline, index, sheetname)
table.convert2Latex()
print(table.getFileContent())