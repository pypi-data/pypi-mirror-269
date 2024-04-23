import os
from copy import deepcopy
import numpy as np
import pandas as pd
from qtpy import QtWidgets, uic
from qtpy.QtCore import QSortFilterProxyModel
from PyGFETdb.GuiDBView.GuiHelpers import PandasModel


class NormGui(QtWidgets.QMainWindow):
    def __init__(self, dfData):
        QtWidgets.QMainWindow.__init__(self)

        self.DataExp = None
        self.SelCol = None
        uipath = os.path.join(os.path.dirname(__file__), 'GuiNormalization.ui')
        uic.loadUi(uipath, self)

        self.pdAttrs = dfData.attrs
        dfData.attrs = {}
        self.dfData = deepcopy(dfData)

        self.setWindowTitle('Normalization Dialog')

        self.ButGen.clicked.connect(self.ButGen_Click)

        # includetypes = ('float', 'category', 'bool', 'datetime64[ns]', 'int')
        # catCols = list(self.dfData.select_dtypes(include=includetypes).columns)
        SelCols = ('Comments', 'FuncStep', 'Cycle')
        self.LstColumn.addItems(SelCols)

        self.LstColumn.itemSelectionChanged.connect(self.LstColumn_Changed)
        self.LstValue.itemSelectionChanged.connect(self.LstValue_Changed)

    def LstColumn_Changed(self):
        Sel = self.LstColumn.selectedItems()
        if len(Sel) == 0:
            print('Select Column')
            return
        SelCol = [s.text() for s in Sel][0]

        self.SelCol = SelCol
        self.LstValue.clear()
        self.LstValue.addItems([str(s) for s in list(self.dfData[SelCol].unique())])

    def LstValue_Changed(self):
        Sel = self.LstValue.selectedItems()
        if len(Sel) == 0:
            print('Select Value')
            return
        SelVal = [s.text() for s in Sel][0]
        self.SelVal = SelVal

        if self.dfData[self.SelCol].dtype == int or self.dfData[self.SelCol].dtype == float:
            q = "{} == {}".format(self.SelCol, SelVal)
        else:
            q = "{} == '{}'".format(self.SelCol, SelVal)
        self.dRef = self.dfData.query(q)

        self.modelData = PandasModel(self.dRef.copy())
        self.proxyData = QSortFilterProxyModel()
        self.proxyData.setSourceModel(self.modelData)
        self.TblRefValues.setModel(self.proxyData)
        self.TblRefValues.show()

    def ButGen_Click(self):
        from PyGFETdb.GuiDBView.GuiDBViewDataExplorer import DataExplorer

        equation = self.TxtEquation.text()
        sufix = self.TxtSufix.text()

        pdSeries = []
        # iterate over trts
        for nTrt, gTrt in self.dfData.groupby('Name', observed=True):
            # get reference values
            gSteps = gTrt.groupby(self.SelCol, observed=True)
            try:
                refVal = gSteps.get_group(self.SelVal).iloc[0, :]
            except:
                try:
                    refVal = gSteps.get_group(float(self.SelVal)).iloc[0, :]
                except:
                    print(nTrt, 'Not Ref val')
                    continue

            for index, r in gTrt.iterrows():
                newRow = r.copy()
                for par in self.pdAttrs['ScalarCols']:
                    val = newRow[par]
                    ref = refVal[par]
                    newRow[par + sufix] = eval(equation)
                pdSeries.append(newRow)
        dfn1 = pd.concat(pdSeries, axis=1).transpose()

        DataTypes = self.dfData.dtypes
        GainPars = np.setdiff1d(list(dfn1.keys()), list(self.dfData.keys()))
        for f in GainPars:
            DataTypes[f] = float

        dfDat = dfn1.astype(DataTypes)
        dfDat.attrs = deepcopy(self.pdAttrs)
        for f in GainPars:
            dfDat.attrs['ScalarCols'].append(f)

        self.DataExp = DataExplorer(dfDat.reset_index(drop=True),
                                    ClassQueries=None,
                                    pdAttr=dfDat.attrs)
        self.DataExp.show()
